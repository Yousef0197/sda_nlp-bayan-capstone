# MODEL_CARD — Bayan

**Project:** Bayan — Bilingual Applied NLP Capstone  
**Training context:** Bayan — [@SDAIAAcademy](https://github.com/SDAIAAcademy) — **#SDAIA**

## System overview

Bayan is an educational bilingual Arabic/English NLP system that demonstrates:

- versioned preprocessing and PII masking;
- topic and sentiment classification;
- named entity recognition;
- extractive QA with no-answer handling;
- bilingual semantic search;
- behavioural evaluation and error analysis;
- benchmark/optimization paths;
- FastAPI serving;
- one measured extension.

**Implementation status:** ✅ COMPLETE

---

## Evidence hierarchy

This model card deliberately separates:

- `MEASURED_SMOKE` — small synthetic educational suites;
- `MEASURED_LOCAL` — actual local-machine measurements;
- academy-frozen/reference-lab evidence — external evidence not replaced by this repository.

`ACADEMY_FROZEN_EVAL_REPLACED=False`

---

## Main model and tokenizer choices

### Bilingual task checkpoint

Integrated task-training smoke paths use:

`distilbert/distilbert-base-multilingual-cased`

The project uses a multilingual family because the target workflow is bilingual rather than Arabic-only.

### Day 1 tokenizer evidence

| Tokenizer | Arabic fertility | English fertility |
|---|---:|---:|
| mBERT | `2.595` | `1.299` |
| AraBERT | `1.182` | `3.714` |

AraBERT tokenizes the Arabic sample more economically, while mBERT is substantially more balanced across the two languages in the measured sample. This evidence supports the multilingual-family decision for a shared bilingual path.

### Semantic search models

The formal search notebook uses:

- embedding model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- candidate index: FAISS `IndexFlatIP` after L2 normalization
- reranker: `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`

The additional integration notebook uses deterministic bilingual concept canonicalization and lightweight reranking for a reproducible smoke run; that simplified integrated path does not replace the full formal CrossEncoder lab.

---

## Architecture constraints

The project documentation records:

- scaled dot-product attention;
- explicit mask semantics;
- attention score shape `T_q × T_k`;
- quadratic sequence-length growth of self-attention score matrices;
- truncation as a measured design risk rather than an assumed-safe constant;
- token fertility as evidence for tokenizer selection.

See `reports/day1_report.md` and `DECISIONS.md`.

---

## Task capabilities and measured smoke evidence

| Task | Integration result | Evidence class |
|---|---:|---|
| Topic classification delta | `+0.858` Macro-F1 | `MEASURED_SMOKE` |
| Sentiment classification delta | `+0.663` Macro-F1 | `MEASURED_SMOKE` |
| NER entity F1 | `1.000` | `MEASURED_SMOKE` |
| QA no-answer | `20/20` | `MEASURED_SMOKE` |
| Recall@10 | `1.000` | `MEASURED_SMOKE` |
| MRR@10 | `1.000` | `MEASURED_SMOKE` |
| Invariance | `1.000` | `MEASURED_SMOKE` |
| MFT | `1.000` | `MEASURED_SMOKE` |
| Extension Top-1 delta | `+0.88` | `MEASURED_SMOKE` |

These values do not imply production accuracy or an academy-frozen score.

The repository also preserves weaker short-training Day 2 smoke reports under `reports/smoke/` rather than discarding inconvenient results. Those runs have different training/evaluation scopes and therefore are not mixed with the integration acceptance suite.

---

## Named Entity Recognition

NER evidence includes:

- `word_ids()` alignment;
- explicit continuation/special-token handling with `-100`;
- entity-level precision/recall/F1 evaluation path;
- dedicated tests.

**Status:** `IMPLEMENTED`.

---

## Extractive QA

QA evidence includes:

- start/end span preparation;
- valid-span constraints;
- no-answer handling;
- boundary tests.

**Status:** `IMPLEMENTED`.

---

## Arabic profile

The project uses a documented Arabic processing contract and canaries to reduce train/eval/serve skew. The formal Arabic notebook includes CAMeL Tools where Arabic-specific normalization is useful.

**Status:** `IMPLEMENTED`.

---

## Semantic search

Formal architecture:

`text → preprocessing → multilingual sentence embeddings → L2 normalization → FAISS IndexFlatIP → top-k candidates → CrossEncoder reranking`

The project evaluates retrieval using Recall/MRR and includes bilingual/cross-lingual analysis.

**Status:** `IMPLEMENTED`.

---

## Error analysis

Current row-level evidence:

- baseline errors reviewed: `108`
- improved path correct on those baseline errors: `106/108`
- residual improved errors: `2`

Categories:

- cross-language intent/specificity gap: `56`
- hash-collision/candidate-ordering errors: `44`
- modifier-noise ranking instability: `8`

Evidence:

- `reports/T9_MANUAL_REVIEW.md`
- `reports/t9_manual_error_review.csv`

**Reviewer:** GPT-5.6 Sol  
**Review type:** AI-assisted row-by-row semantic review  
**Independent human-review claim:** `FALSE`

If the academy requires the learner/instructor specifically to conduct the manual reading, human confirmation remains necessary before making that stricter claim.

---

## Serving

Serving contracts include:

- `GET /health`
- `POST /v1/classify`
- input validation
- language handling
- PII masking
- model/preprocessing manifest validation
- startup canaries
- stable JSON response metadata.

See `src/bayan/serving.py` and Day 4 tests/notebooks.

**Status:** `IMPLEMENTED`.

---

## Performance

Formal Notebook 08 implements:

- FP32 reference;
- warm-up and repeated measurements;
- p50/p95/p99 and throughput;
- approximate process RSS/observed peak;
- ONNX checker and ORT path;
- prediction/numerical parity;
- INT8 candidate;
- quality tax;
- FP32 rollback;
- FastAPI canaries.

Additional local real-HTTP evidence:

- Windows 11 local CPU
- 8 logical CPUs
- concurrency `16`
- warm-up `32`
- measured requests `128`
- p50 `19.172 ms`
- p95 `24.805 ms`
- p99 `27.903 ms`
- mean `18.340 ms`

**Evidence class:** `MEASURED_LOCAL`.

The machine is not represented as the academy reference lab CPU.

---

## Measured extension

Extension:

**Bilingual concept canonicalization + reranking**

Integration smoke:

- before Top-1 `0.10`
- after Top-1 `0.98`
- delta `+0.88`

The integration notebook prints `KEEP` for a positive delta; project documentation normalizes the release decision to `ADOPT`. Both mean retain the improved candidate.

**Decision:** `ADOPT`.

---

## Intended use

This repository is intended for:

- education and assessment in applied NLP;
- reproducible demonstrations of bilingual NLP engineering;
- inspection of design decisions, limitations and evidence provenance.

It is **not** a production government decision system and must not be treated as an authoritative high-stakes classifier.

---

## Data and privacy

- synthetic educational data only;
- no real citizen/customer PII is intentionally included;
- email/phone samples are synthetic canaries;
- secrets, `.env`, model weights and large checkpoints are excluded from GitHub;
- frozen-test boundaries are documented.

---

## Limitations

1. Small synthetic suites can yield unstable or unrealistically high metrics.
2. Separate smoke runs can disagree materially; preserved Day 2 smoke evidence demonstrates this.
3. No academy-frozen evaluation package is replaced by repository smoke data.
4. The `27.903 ms` HTTP p99 result is local-machine evidence, not a verified academy reference-CPU measurement.
5. T9 row-level review is AI-assisted and not represented as independent human review.
6. Production dialect/domain drift requires broader real-world validation before deployment.

---

## Validation and release

Required submission files, numbered notebooks, source modules, tests, reports and validator are present.

`submission-v1.0` exists but predates the latest evidence-alignment changes. The release must be refreshed to the final validated `main` commit before the repository is considered frozen for submission.

**Implementation:** ✅ COMPLETE  
**Evidence documentation:** ✅ ALIGNED  
**Final tag refresh:** ⏳ PENDING FINAL VALIDATION

**Academy GitHub:** [@SDAIAAcademy](https://github.com/SDAIAAcademy)  
**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
