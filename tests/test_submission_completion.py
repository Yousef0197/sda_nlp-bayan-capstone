from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_student_profile_is_finalized() -> None:
    text = _read("STUDENT_PROFILE.md")
    forbidden = ("In progress", "Work in progress", "Pending final submission")
    assert not any(token in text for token in forbidden)
    assert text.count("- [x]") >= 4
    assert "Yousef Al-Mutiri" in text
    assert re.search(r"Date:\s*2026-\d{2}-\d{2}", text)


def test_submission_safe_sample_outputs_exist() -> None:
    expected = {
        "sample_outputs/ar_classification.json",
        "sample_outputs/en_classification.json",
        "sample_outputs/invalid_input.json",
    }
    for relative in expected:
        path = ROOT / relative
        assert path.is_file(), relative
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload.get("status") == "PASS"
        serialized = json.dumps(payload, ensure_ascii=False)
        assert "@" not in serialized
        assert not re.search(r"(?:\+?966|0)?5\d{8}", serialized)


def test_gate_d_project_artifact_report_is_measured_and_passed() -> None:
    path = ROOT / "reports/t10_project_artifact_benchmark.json"
    assert path.is_file()
    report = json.loads(path.read_text(encoding="utf-8"))
    assert report["gate_d_status"] == "PASS"
    assert report["artefact_role"] == "PROJECT_ARTIFACT"
    assert report["result_label"] == "MEASURED"
    assert report["budget_provenance"] == "STUDENT_DEFINED_BEFORE_MEASUREMENT"
    assert report["model"]["id"] == "distilbert/distilbert-base-multilingual-cased"
    assert report["preprocessing_version"] == "ar-en-v1"
    assert report["workload"]["arabic_count"] > 0
    assert report["workload"]["english_count"] > 0
    assert report["quality"]["metric"] == "macro_f1_validation_full_workload"
    assert report["quality"]["quality_tax"] <= report["budget"]["max_quality_tax"]
    assert report["budget_assessment"]["status"] == "PASS"
    assert all(item["status"] == "PASS" for item in report["canaries"])


def test_notebook_08_is_committed_in_project_artifact_mode() -> None:
    notebook = json.loads(_read("notebooks/08_optimization_serving.ipynb"))
    source = "\n".join(
        line
        for cell in notebook["cells"]
        for line in cell.get("source", [])
    )
    assert "PROJECT_MODE = True" in source
    assert "BUDGET_PROVENANCE = \"STUDENT_DEFINED_BEFORE_MEASUREMENT\"" in source
    assert "PROJECT_ARTIFACT" in source
    assert "t10_project_artifact_benchmark.json" in source
    assert "DAY4_NOTEBOOK8_CORE=PASS" in source


def test_project_summary_links_the_project_artifact_evidence() -> None:
    summary = json.loads(_read("PROJECT_SUMMARY.json"))
    assert summary["benchmark_mode"] == "PROJECT_ARTIFACT"
    gate_d = summary["gate_d"]
    assert gate_d["status"] == "PASS"
    assert gate_d["evidence"] == "reports/t10_project_artifact_benchmark.json"
    assert gate_d["artefact_role"] == "PROJECT_ARTIFACT"


def test_submission_validator_report_is_preserved_as_pass() -> None:
    payload = json.loads(_read("reports/submission_validation.json"))
    assert payload["status"] == "PASS"
    assert payload["errors"] == []


def test_peer_review_disposition_is_recorded() -> None:
    text = _read("reports/PEER_REVIEW_DISPOSITION.md")
    assert "Status: PASS" in text
    assert "Disposition:" in text
    assert "Evidence reviewed:" in text
