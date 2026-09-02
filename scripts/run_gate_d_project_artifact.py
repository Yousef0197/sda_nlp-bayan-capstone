#!/usr/bin/env python3
"""Run Bayan Gate D on the trained bilingual topic-classification artifact.

This script intentionally measures a PROJECT_ARTIFACT. It trains the same
multilingual DistilBERT topic head used by Notebook 03 on the frozen course
training split, evaluates the fixed bilingual validation split, exports ONNX,
attempts dynamic INT8, applies a budget declared in source before measurement,
exercises the FastAPI contract, and writes small auditable reports only.
Large model artifacts stay in a temporary directory and are never committed.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import random
import tempfile
import time
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import onnx
import onnxruntime as ort
import psutil
import torch
import torch.nn as nn
from fastapi import FastAPI
from fastapi.testclient import TestClient
from onnxruntime.quantization import QuantType, quantize_dynamic
from pydantic import BaseModel, Field
from torch.optim import AdamW
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from bayan.benchmarking import (
    artifact_size_mb,
    assess_budget,
    benchmark_callable,
    quality_tax,
)
from bayan.preprocessing import build_text_record
from bayan.serving import ServingManifest, build_prediction_response, run_canaries

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sample" / "bayan_day2_classification.csv"
VALIDATION_PATH = ROOT / "data" / "sample" / "bayan_day4_validation.csv"
REPORT_PATH = ROOT / "reports" / "t10_project_artifact_benchmark.json"
SUMMARY_PATH = ROOT / "PROJECT_SUMMARY.json"
SAMPLE_DIR = ROOT / "sample_outputs"

MODEL_ID = "distilbert/distilbert-base-multilingual-cased"
PREPROCESSING_VERSION = "ar-en-v1"
SEED = 42
MAX_LENGTH = 64
BATCH_SIZE = 4
NUM_EPOCHS = 12
LEARNING_RATE = 1e-4
WARMUP = 5
REPETITIONS = 30

# Declared before candidate measurement, as required by the Gate D contract.
PERFORMANCE_BUDGET = {
    "max_p95_ms": 1000.0,
    "min_throughput_items_s": 0.1,
    "max_quality_tax": 0.05,
    "target_device": "cpu",
}
BUDGET_PROVENANCE = "STUDENT_DEFINED_BEFORE_MEASUREMENT"
ARTEFACT_ROLE = "PROJECT_ARTIFACT"
RESULT_LABEL = "MEASURED"


class ClassifyRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)
    language: str = "auto"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_directory(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        with item.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    return digest.hexdigest()


def macro_f1(y_true: list[str], y_pred: list[str]) -> float:
    labels = sorted(set(y_true) | set(y_pred))
    scores: list[float] = []
    for label in labels:
        tp = sum(t == label and p == label for t, p in zip(y_true, y_pred))
        fp = sum(t != label and p == label for t, p in zip(y_true, y_pred))
        fn = sum(t == label and p != label for t, p in zip(y_true, y_pred))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        score = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        scores.append(score)
    return float(sum(scores) / len(scores)) if scores else 0.0


def load_rows() -> list[dict[str, str]]:
    with DATA_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"example_id", "split", "language", "text", "topic"}
    assert rows and required.issubset(rows[0]), rows[0].keys() if rows else None
    return rows


def prepare_text(row: dict[str, str]) -> str:
    return build_text_record(row["text"], language=row["language"]).model_text


def batches(rows: list[dict[str, str]], *, shuffle: bool) -> list[list[dict[str, str]]]:
    ordered = list(rows)
    if shuffle:
        random.shuffle(ordered)
    return [ordered[i : i + BATCH_SIZE] for i in range(0, len(ordered), BATCH_SIZE)]


def predict_pytorch(
    model: torch.nn.Module,
    tokenizer,
    rows: list[dict[str, str]],
    id2label: dict[int, str],
) -> tuple[np.ndarray, list[str]]:
    model.eval()
    all_logits: list[np.ndarray] = []
    with torch.inference_mode():
        for batch in batches(rows, shuffle=False):
            encoded = tokenizer(
                [prepare_text(row) for row in batch],
                padding=True,
                truncation=True,
                max_length=MAX_LENGTH,
                return_tensors="pt",
            )
            logits = model(**encoded).logits.detach().cpu().numpy()
            all_logits.append(logits)
    merged = np.concatenate(all_logits, axis=0)
    labels = [id2label[int(index)] for index in merged.argmax(axis=1)]
    return merged, labels


class LogitsWrapper(nn.Module):
    def __init__(self, model: torch.nn.Module) -> None:
        super().__init__()
        self.model = model

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        return self.model(input_ids=input_ids, attention_mask=attention_mask).logits


def build_ort_predictor(session: ort.InferenceSession, tokenizer):
    input_names = {item.name for item in session.get_inputs()}

    def predict(rows: list[dict[str, str]]) -> np.ndarray:
        all_logits: list[np.ndarray] = []
        for batch in batches(rows, shuffle=False):
            encoded = tokenizer(
                [prepare_text(row) for row in batch],
                padding=True,
                truncation=True,
                max_length=MAX_LENGTH,
                return_tensors="np",
            )
            feed = {
                name: encoded[name].astype(np.int64)
                for name in ("input_ids", "attention_mask")
                if name in input_names
            }
            outputs = session.run(None, feed)
            all_logits.append(np.asarray(outputs[0]))
        return np.concatenate(all_logits, axis=0)

    return predict


def benchmark_pytorch(model, tokenizer, benchmark_rows):
    encoded = tokenizer(
        [prepare_text(row) for row in benchmark_rows],
        padding=True,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )

    def call():
        with torch.inference_mode():
            return model(**encoded).logits

    return benchmark_callable(
        call,
        warmup=WARMUP,
        repetitions=REPETITIONS,
        items_per_call=len(benchmark_rows),
        memory_reader=lambda: psutil.Process().memory_info().rss,
    )


def benchmark_ort(session: ort.InferenceSession, tokenizer, benchmark_rows):
    input_names = {item.name for item in session.get_inputs()}
    encoded = tokenizer(
        [prepare_text(row) for row in benchmark_rows],
        padding=True,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="np",
    )
    feed = {
        name: encoded[name].astype(np.int64)
        for name in ("input_ids", "attention_mask")
        if name in input_names
    }

    def call():
        return session.run(None, feed)

    return benchmark_callable(
        call,
        warmup=WARMUP,
        repetitions=REPETITIONS,
        items_per_call=len(benchmark_rows),
        memory_reader=lambda: psutil.Process().memory_info().rss,
    )


def train_project_artifact(rows, workdir: Path):
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.set_num_threads(max(1, min(4, os.cpu_count() or 1)))

    train_rows = [row for row in rows if row["split"] == "train"]
    validation_rows = [row for row in rows if row["split"] == "validation"]
    labels = sorted({row["topic"] for row in rows})
    label2id = {label: index for index, label in enumerate(labels)}
    id2label = {index: label for label, index in label2id.items()}

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_ID,
        num_labels=len(labels),
        label2id=label2id,
        id2label=id2label,
    )
    for parameter in model.base_model.parameters():
        parameter.requires_grad = False

    trainable_parameters = [p for p in model.parameters() if p.requires_grad]
    assert trainable_parameters
    optimizer = AdamW(trainable_parameters, lr=LEARNING_RATE)

    best_validation_f1 = -1.0
    best_epoch = 0
    best_state: dict[str, torch.Tensor] | None = None
    epoch_history = []

    for epoch in range(1, NUM_EPOCHS + 1):
        model.train()
        epoch_losses = []
        for batch in batches(train_rows, shuffle=True):
            encoded = tokenizer(
                [prepare_text(row) for row in batch],
                padding=True,
                truncation=True,
                max_length=MAX_LENGTH,
                return_tensors="pt",
            )
            target = torch.tensor([label2id[row["topic"]] for row in batch], dtype=torch.long)
            optimizer.zero_grad(set_to_none=True)
            output = model(**encoded, labels=target)
            output.loss.backward()
            optimizer.step()
            epoch_losses.append(float(output.loss.detach().cpu()))

        _, validation_predictions = predict_pytorch(model, tokenizer, validation_rows, id2label)
        validation_truth = [row["topic"] for row in validation_rows]
        validation_f1 = macro_f1(validation_truth, validation_predictions)
        epoch_history.append(
            {
                "epoch": epoch,
                "mean_loss": float(np.mean(epoch_losses)),
                "validation_macro_f1": validation_f1,
            }
        )
        if validation_f1 > best_validation_f1:
            best_validation_f1 = validation_f1
            best_epoch = epoch
            best_state = {
                name: parameter.detach().cpu().clone()
                for name, parameter in model.named_parameters()
                if parameter.requires_grad
            }

    assert best_state is not None
    with torch.no_grad():
        for name, parameter in model.named_parameters():
            if name in best_state:
                parameter.copy_(best_state[name])
    model.eval()

    checkpoint_dir = workdir / "project_model"
    model.save_pretrained(checkpoint_dir)
    tokenizer.save_pretrained(checkpoint_dir)
    checkpoint_sha256 = sha256_directory(checkpoint_dir)

    return {
        "model": model,
        "tokenizer": tokenizer,
        "train_rows": train_rows,
        "validation_rows": validation_rows,
        "labels": labels,
        "label2id": label2id,
        "id2label": id2label,
        "best_epoch": best_epoch,
        "best_validation_f1": best_validation_f1,
        "epoch_history": epoch_history,
        "checkpoint_dir": checkpoint_dir,
        "checkpoint_sha256": checkpoint_sha256,
        "base_revision": getattr(model.config, "_commit_hash", None),
    }


def export_onnx(model, tokenizer, workdir: Path) -> Path:
    onnx_path = workdir / "bayan_topic_fp32.onnx"
    example = tokenizer(
        ["الخدمة الإلكترونية واضحة", "The online service is clear"],
        padding=True,
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )
    wrapper = LogitsWrapper(model).eval()
    with torch.inference_mode():
        torch.onnx.export(
            wrapper,
            (example["input_ids"], example["attention_mask"]),
            onnx_path,
            input_names=["input_ids", "attention_mask"],
            output_names=["logits"],
            dynamic_axes={
                "input_ids": {0: "batch", 1: "sequence"},
                "attention_mask": {0: "batch", 1: "sequence"},
                "logits": {0: "batch"},
            },
            opset_version=17,
            dynamo=False,
        )
    checked = onnx.load(onnx_path)
    onnx.checker.check_model(checked)
    return onnx_path


def build_api(selected_predict, tokenizer, id2label, manifest):
    app = FastAPI(title="Bayan Gate D API", version="1.0")

    @app.get("/health")
    def health():
        return {"status": "ok", "artefact_role": ARTEFACT_ROLE}

    @app.post("/v1/classify")
    def classify(payload: ClassifyRequest):
        language = payload.language
        if language == "auto":
            language = "ar" if any("\u0600" <= ch <= "\u06ff" for ch in payload.text) else "en"
        row = {"text": payload.text, "language": language}
        logits = selected_predict([row])
        scores = np.asarray(logits[0], dtype=np.float64)
        shifted = scores - scores.max()
        probs = np.exp(shifted) / np.exp(shifted).sum()
        index = int(probs.argmax())
        return build_prediction_response(
            request_id=str(uuid.uuid4()),
            text=payload.text,
            language=language,
            label=id2label[index],
            confidence=float(probs[index]),
            latency_ms=0.0,
            manifest=manifest,
        )

    return app


def main() -> int:
    started = time.perf_counter()
    rows = load_rows()
    source_validation = [row for row in rows if row["split"] == "validation"]
    with VALIDATION_PATH.open(encoding="utf-8", newline="") as handle:
        gate_rows = list(csv.DictReader(handle))
    assert gate_rows and {"example_id", "split", "language", "text", "label"}.issubset(gate_rows[0])
    validation_rows = [
        {
            "example_id": row["example_id"],
            "split": row["split"],
            "language": row["language"],
            "text": row["text"],
            "topic": row["label"],
        }
        for row in gate_rows
    ]
    source_signature = {
        (row["example_id"], row["language"], row["text"], row["topic"])
        for row in source_validation
    }
    gate_signature = {
        (row["example_id"], row["language"], row["text"], row["topic"])
        for row in validation_rows
    }
    assert gate_signature == source_signature
    assert len(validation_rows) == 8
    assert Counter(row["language"] for row in validation_rows) == {"ar": 4, "en": 4}

    with tempfile.TemporaryDirectory(prefix="bayan-gate-d-") as temp:
        workdir = Path(temp)
        trained = train_project_artifact(rows, workdir)
        model = trained["model"]
        tokenizer = trained["tokenizer"]
        id2label = trained["id2label"]

        fp32_logits, fp32_labels = predict_pytorch(model, tokenizer, validation_rows, id2label)
        y_true = [row["topic"] for row in validation_rows]
        fp32_quality = macro_f1(y_true, fp32_labels)

        onnx_path = export_onnx(model, tokenizer, workdir)
        fp32_session = ort.InferenceSession(
            str(onnx_path),
            providers=["CPUExecutionProvider"],
        )
        onnx_predict = build_ort_predictor(fp32_session, tokenizer)
        onnx_logits = onnx_predict(validation_rows)
        onnx_labels = [id2label[int(index)] for index in onnx_logits.argmax(axis=1)]
        onnx_quality = macro_f1(y_true, onnx_labels)
        onnx_tax = max(0.0, quality_tax(fp32_quality, onnx_quality))
        onnx_parity = {
            "prediction_agreement": float(np.mean(np.array(fp32_labels) == np.array(onnx_labels))),
            "max_abs_logit_diff": float(np.max(np.abs(fp32_logits - onnx_logits))),
        }
        assert onnx_parity["prediction_agreement"] == 1.0, onnx_parity

        benchmark_rows = validation_rows[:BATCH_SIZE]
        pytorch_benchmark = benchmark_pytorch(model, tokenizer, benchmark_rows)
        onnx_benchmark = benchmark_ort(fp32_session, tokenizer, benchmark_rows)

        candidates = {
            "pytorch_fp32": {
                "status": "PASS",
                "benchmark": pytorch_benchmark,
                "quality": fp32_quality,
                "artifact_size_mb": artifact_size_mb(trained["checkpoint_dir"]),
            },
            "onnx_fp32": {
                "status": "PASS",
                "benchmark": onnx_benchmark,
                "quality": onnx_quality,
                "quality_tax": onnx_tax,
                "parity": onnx_parity,
                "artifact_size_mb": artifact_size_mb(onnx_path),
                "sha256": sha256_file(onnx_path),
            },
        }

        selected_name = "onnx_fp32"
        selected_predict = onnx_predict
        selected_quality = onnx_quality
        selected_tax = onnx_tax
        selected_benchmark = onnx_benchmark
        selected_artifact_path = onnx_path
        int8_status = "NOT_SELECTED"

        int8_path = workdir / "bayan_topic_int8.onnx"
        try:
            quantize_dynamic(
                model_input=str(onnx_path),
                model_output=str(int8_path),
                weight_type=QuantType.QInt8,
            )
            int8_model = onnx.load(int8_path)
            onnx.checker.check_model(int8_model)
            int8_session = ort.InferenceSession(
                str(int8_path),
                providers=["CPUExecutionProvider"],
            )
            int8_predict = build_ort_predictor(int8_session, tokenizer)
            int8_logits = int8_predict(validation_rows)
            int8_labels = [id2label[int(index)] for index in int8_logits.argmax(axis=1)]
            int8_quality = macro_f1(y_true, int8_labels)
            int8_tax = max(0.0, quality_tax(fp32_quality, int8_quality))
            int8_benchmark = benchmark_ort(int8_session, tokenizer, benchmark_rows)
            int8_assessment_raw = assess_budget(
                int8_benchmark,
                quality_tax_value=int8_tax,
                max_p95_ms=PERFORMANCE_BUDGET["max_p95_ms"],
                max_quality_tax=PERFORMANCE_BUDGET["max_quality_tax"],
                min_throughput_items_s=PERFORMANCE_BUDGET["min_throughput_items_s"],
            )
            candidates["onnx_int8"] = {
                "status": "PASS" if int8_assessment_raw["budget_met"] else "REJECT",
                "benchmark": int8_benchmark,
                "quality": int8_quality,
                "quality_tax": int8_tax,
                "parity": {
                    "prediction_agreement": float(
                        np.mean(np.array(fp32_labels) == np.array(int8_labels))
                    ),
                    "max_abs_logit_diff": float(np.max(np.abs(fp32_logits - int8_logits))),
                },
                "artifact_size_mb": artifact_size_mb(int8_path),
                "sha256": sha256_file(int8_path),
                "budget": int8_assessment_raw,
            }
            if int8_assessment_raw["budget_met"] and int8_benchmark["p95_ms"] <= onnx_benchmark["p95_ms"]:
                selected_name = "onnx_int8"
                selected_predict = int8_predict
                selected_quality = int8_quality
                selected_tax = int8_tax
                selected_benchmark = int8_benchmark
                selected_artifact_path = int8_path
                int8_status = "SELECTED"
            else:
                int8_status = "MEASURED_NOT_SELECTED"
        except Exception as exc:
            candidates["onnx_int8"] = {
                "status": "UNAVAILABLE",
                "reason": f"{type(exc).__name__}: {exc}",
            }
            int8_status = "UNAVAILABLE"

        selected_assessment_raw = assess_budget(
            selected_benchmark,
            quality_tax_value=selected_tax,
            max_p95_ms=PERFORMANCE_BUDGET["max_p95_ms"],
            max_quality_tax=PERFORMANCE_BUDGET["max_quality_tax"],
            min_throughput_items_s=PERFORMANCE_BUDGET["min_throughput_items_s"],
        )
        selected_assessment = {
            "status": "PASS" if selected_assessment_raw["budget_met"] else "FAIL",
            **selected_assessment_raw,
        }
        if not selected_assessment_raw["budget_met"]:
            raise RuntimeError(f"Gate D budget failed: {selected_assessment}")

        manifest = ServingManifest(
            model_id=MODEL_ID,
            model_version=trained["checkpoint_sha256"][:12],
            preprocessing_version=PREPROCESSING_VERSION,
            runtime=selected_name,
            label_map=id2label,
            artifact_sha256=sha256_file(selected_artifact_path),
        )
        app = build_api(selected_predict, tokenizer, id2label, manifest)
        client = TestClient(app)

        health = client.get("/health")
        assert health.status_code == 200 and health.json()["status"] == "ok"

        ar_response = client.post(
            "/v1/classify",
            json={"text": "تعذر تسجيل الدخول إلى البوابة", "language": "ar"},
        )
        en_response = client.post(
            "/v1/classify",
            json={"text": "The bus did not arrive on time", "language": "en"},
        )
        invalid_response = client.post(
            "/v1/classify",
            json={"text": "", "language": "en"},
        )
        assert ar_response.status_code == 200
        assert en_response.status_code == 200
        assert invalid_response.status_code == 422

        def canary_predict(text: str, language: str):
            response = client.post(
                "/v1/classify",
                json={"text": text, "language": language},
            )
            assert response.status_code == 200
            return response.json()

        canaries = run_canaries(
            canary_predict,
            [
                {
                    "name": "arabic-digital-service",
                    "text": "تعذر تسجيل الدخول إلى البوابة",
                    "language": "ar",
                    "expected_label": "digital_service",
                },
                {
                    "name": "english-transport",
                    "text": "The bus did not arrive on time",
                    "language": "en",
                    "expected_label": "transport",
                },
            ],
        )

        SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
        ar_sample = {
            "status": "PASS",
            "http_status": ar_response.status_code,
            "request": {"text": "تعذر تسجيل الدخول إلى البوابة", "language": "ar"},
            "response": ar_response.json(),
        }
        en_sample = {
            "status": "PASS",
            "http_status": en_response.status_code,
            "request": {"text": "The bus did not arrive on time", "language": "en"},
            "response": en_response.json(),
        }
        invalid_sample = {
            "status": "PASS",
            "http_status": invalid_response.status_code,
            "request": {"text": "", "language": "en"},
            "error_type": "request_validation_error",
        }
        (SAMPLE_DIR / "ar_classification.json").write_text(
            json.dumps(ar_sample, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (SAMPLE_DIR / "en_classification.json").write_text(
            json.dumps(en_sample, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (SAMPLE_DIR / "invalid_input.json").write_text(
            json.dumps(invalid_sample, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        report = {
            "gate_d_status": "PASS",
            "result_label": RESULT_LABEL,
            "artefact_role": ARTEFACT_ROLE,
            "budget_provenance": BUDGET_PROVENANCE,
            "measured_at_utc": datetime.now(timezone.utc).isoformat(),
            "environment": {
                "platform": platform.platform(),
                "python": platform.python_version(),
                "torch": torch.__version__,
                "onnx": onnx.__version__,
                "onnxruntime": ort.__version__,
                "cpu_count": os.cpu_count(),
                "torch_threads": torch.get_num_threads(),
                "accelerator": "CPU",
            },
            "model": {
                "id": MODEL_ID,
                "base_revision": trained["base_revision"],
                "training_mode": "partial_finetune_cpu_frozen_base",
                "seed": SEED,
                "epochs_run": NUM_EPOCHS,
                "selected_epoch": trained["best_epoch"],
                "checkpoint_sha256": trained["checkpoint_sha256"],
                "label_map": {str(index): label for index, label in id2label.items()},
            },
            "preprocessing_version": PREPROCESSING_VERSION,
            "workload": {
                "path": str(VALIDATION_PATH.relative_to(ROOT)),
                "sha256": sha256_file(VALIDATION_PATH),
                "source_path": str(DATA_PATH.relative_to(ROOT)),
                "source_sha256": sha256_file(DATA_PATH),
                "split": "validation",
                "total_count": len(validation_rows),
                "arabic_count": sum(row["language"] == "ar" for row in validation_rows),
                "english_count": sum(row["language"] == "en" for row in validation_rows),
                "batch_size": BATCH_SIZE,
                "max_length": MAX_LENGTH,
            },
            "budget": PERFORMANCE_BUDGET,
            "training": {
                "learning_rate": LEARNING_RATE,
                "history": trained["epoch_history"],
                "best_validation_macro_f1": trained["best_validation_f1"],
            },
            "candidates": candidates,
            "selected_runtime": {
                "name": selected_name,
                "artifact_sha256": sha256_file(selected_artifact_path),
                "artifact_size_mb": artifact_size_mb(selected_artifact_path),
                "int8_status": int8_status,
                "rollback": "pytorch_fp32_checkpoint",
            },
            "quality": {
                "metric": "macro_f1_validation_full_workload",
                "fp32": fp32_quality,
                "selected": selected_quality,
                "quality_tax": selected_tax,
            },
            "budget_assessment": selected_assessment,
            "api": {
                "health_status": health.status_code,
                "arabic_status": ar_response.status_code,
                "english_status": en_response.status_code,
                "invalid_input_status": invalid_response.status_code,
            },
            "canaries": canaries,
            "elapsed_s": time.perf_counter() - started,
        }

        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    summary["benchmark_mode"] = "PROJECT_ARTIFACT"
    summary["gate_d"] = {
        "status": "PASS",
        "artefact_role": "PROJECT_ARTIFACT",
        "result_label": "MEASURED",
        "evidence": "reports/t10_project_artifact_benchmark.json",
        "model_id": MODEL_ID,
        "preprocessing_version": PREPROCESSING_VERSION,
        "budget_provenance": BUDGET_PROVENANCE,
        "quality_metric": "macro_f1_validation_full_workload",
    }
    SUMMARY_PATH.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("GATE_D_PROJECT_ARTIFACT=PASS")
    print(f"REPORT={REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
