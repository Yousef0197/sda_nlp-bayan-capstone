# EVALUATION_REPORT — Bayan

**Project:** Bayan — Bilingual Applied NLP Capstone  
**Program:** SDA-AIE-211 — Natural Language Processing with Transformers  
**Academy:** [@SDAIAAcademy](https://github.com/SDAIAAcademy) — **#SDAIA**  
**Evaluation status:** ✅ **COMPLETE**

## Evaluation scope

This report consolidates the measurable evidence produced by the project's notebooks, tests and reports. Each metric is tied to a documented data source, split/evaluation protocol and runtime so the result can be inspected and reproduced.

Primary sources:

- `notebooks/03_text_classification.ipynb`
- `notebooks/04_ner_and_qa.ipynb`
- `notebooks/05_arabic_nlp.ipynb`
- `notebooks/06_semantic_search.ipynb`
- `notebooks/07_evaluation_error_analysis.ipynb`
- `notebooks/08_optimization_serving.ipynb`
- `notebooks/bayan_capstone.ipynb`
- `reports/T9_MANUAL_REVIEW.md`
- `reports/t9_manual_error_review.csv`
- `reports/t10_local_cpu_http_benchmark.json`
- `reports/smoke/`

## Final evaluation summary

| Requirement | Measurement | Result | Status |
|---|---|---:|---|
| T3 — Topic | Macro-F1 delta vs TF-IDF baseline | `+0.858` | ✅ COMPLETE |
| T3 — Sentiment | Macro-F1 delta vs TF-IDF baseline | `+0.663` | ✅ COMPLETE |
| T4 — NER | Entity-level F1 | `1.000` | ✅ COMPLETE |
| T5 — QA | no-answer cases | `20/20` | ✅ COMPLETE |
| T7 — Search | Recall@10 | `1.000` | ✅ COMPLETE |
| T7 — Search | MRR@10 | `1.000` | ✅ COMPLETE |
| T8 — Behavioural | Invariance | `1.000` | ✅ COMPLETE |
| T8 — Behavioural | MFT | `1.000` | ✅ COMPLETE |
| T9 — Error analysis | reviewed baseline errors | `108` | ✅ COMPLETE |
| T10 — Service | HTTP p99 @ concurrency 16 | `27.903 ms` | ✅ COMPLETE |
| T12 — Extension | Top-1 delta | `+0.88` | ✅ COMPLETE |

## T3 — Classification

The classification path preserves a TF-IDF baseline and compares it with the multilingual Transformer path using Macro-F1.

Measured integration results:

- Topic delta vs baseline: `+0.858`
- Sentiment delta vs baseline: `+0.663`

Both measured improvements exceed the program's `+0.08` comparison target.

Evidence:

- `notebooks/03_text_classification.ipynb`
- `notebooks/bayan_capstone.ipynb`
- `reports/smoke/day2_classification_metrics.json`

The shorter Day 2 smoke report is preserved as a separate run so variation across tiny training protocols remains auditable.

**T3 status:** ✅ COMPLETE

## T4 — Named Entity Recognition

The NER implementation includes:

- subword alignment through `word_ids()`;
- ignored/special positions using `-100` according to the training contract;
- entity-level precision, recall and F1 evaluation;
- alignment unit tests.

Measured integration entity F1:

`1.000`

Evidence:

- `notebooks/04_ner_and_qa.ipynb`
- `src/bayan/ner_alignment.py`
- `tests/test_day2_ner_alignment.py`

**T4 status:** ✅ COMPLETE

## T5 — Extractive QA

The QA path implements:

- character/token offsets;
- start/end span constraints;
- valid-span filtering;
- explicit no-answer handling;
- dedicated post-processing tests.

Measured no-answer result:

`20/20`

Evidence:

- `notebooks/04_ner_and_qa.ipynb`
- `src/bayan/qa_postprocess.py`
- `tests/test_day2_qa_postprocess.py`

**T5 status:** ✅ COMPLETE

## T6 — Arabic processing consistency

The Arabic path uses a documented processing profile across train/eval/serve and includes canaries and dedicated tests. The formal Arabic notebook uses CAMeL Tools for Arabic-specific processing evidence.

Evidence:

- `notebooks/05_arabic_nlp.ipynb`
- `src/bayan/arabic_profiles.py`
- `tests/test_day3_arabic_profiles.py`

**T6 status:** ✅ COMPLETE

## T7 — Semantic search

Formal search architecture:

`text → preprocessing → multilingual sentence embeddings → L2 normalization → FAISS IndexFlatIP → top-k candidates → CrossEncoder reranking`

Formal models:

- embedding model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- reranker: `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`

Measured integration results:

- Recall@10: `1.000`
- MRR@10: `1.000`

The evaluation includes bilingual/cross-lingual retrieval cases and a reranking decision based on measured before/after behaviour.

Evidence:

- `notebooks/06_semantic_search.ipynb`
- `src/bayan/retrieval.py`
- `tests/test_day3_retrieval.py`

**T7 status:** ✅ COMPLETE

## T8 — Slices, confidence and behavioural testing

Evaluation evidence includes:

- Arabic and English slices;
- bootstrap confidence-interval utilities;
- paired evaluation support;
- invariance tests;
- Minimum Functionality Tests.

Measured integration results:

- Invariance: `1.000`
- MFT: `1.000`

Evidence:

- `notebooks/07_evaluation_error_analysis.ipynb`
- `src/bayan/eval_stats.py`
- `tests/test_day3_eval_stats.py`

**T8 status:** ✅ COMPLETE

## T9 — Error analysis

The repository contains a row-by-row review of **108 baseline retrieval errors**.

Summary:

- baseline errors reviewed: `108`
- improved system correct on those errors: `106/108`
- residual improved-system errors: `2`
- correction rate across the reviewed baseline errors: `98.148%`

Error taxonomy:

| Category | Count |
|---|---:|
| `cross_language_intent_specificity_gap` | `56` |
| `hash_collision_candidate_ordering` | `44` |
| `modifier_noise_ranking_instability` | `8` |

Prioritized fixes:

1. retain bilingual concept canonicalization before embedding;
2. strengthen the lexical/candidate representation;
3. harden reranking against low-information modifiers.

Evidence:

- `reports/T9_MANUAL_REVIEW.md`
- `reports/t9_manual_error_review.csv`

**T9 status:** ✅ COMPLETE

## T10 — Performance and serving evaluation

Formal Notebook 08 implements the benchmark ladder required to compare candidates safely:

- environment capture;
- warm-up and repeated measurements;
- p50/p95/p99;
- throughput;
- approximate process RSS/observed peak;
- FP32 reference;
- ONNX checker and ONNX Runtime;
- dynamic INT8 candidate;
- numerical/prediction parity;
- quality tax;
- rollback/fallback;
- FastAPI canaries.

Additional real HTTP measurement:

| Metric | Result |
|---|---:|
| concurrency | `16` |
| warm-up requests | `32` |
| measured requests | `128` |
| HTTP p50 | `19.172 ms` |
| HTTP p95 | `24.805 ms` |
| HTTP p99 | `27.903 ms` |
| HTTP mean | `18.340 ms` |

Evidence:

- `BENCHMARKS.md`
- `notebooks/08_optimization_serving.ipynb`
- `reports/t10_local_cpu_http_benchmark.json`

**T10 status:** ✅ COMPLETE

## T11 — FastAPI service evaluation

The service contract covers:

- `GET /health`;
- `POST /v1/classify`;
- Arabic request;
- English request;
- invalid-input handling;
- PII masking;
- startup/manifest canaries;
- stable response metadata.

Evidence:

- `src/bayan/serving.py`
- `tests/test_day4_serving.py`
- `notebooks/08_optimization_serving.ipynb`

**T11 status:** ✅ COMPLETE

## T12 — Measured extension

Extension:

**Bilingual concept canonicalization + reranking**

Before/after result on the same integration workload:

- before Top-1: `0.10`
- after Top-1: `0.98`
- delta: `+0.88`

Final decision:

`ADOPT`

The decision is based on the measured improvement and is documented consistently in the project reports.

**T12 status:** ✅ COMPLETE

## Distinction evidence

The evaluation package supports the program's distinction criteria through:

- deeper slice analysis rather than a single aggregate score;
- confidence-interval and paired-evaluation utilities;
- behavioural tests;
- 108-row error analysis with a concrete taxonomy and prioritized fixes;
- preserved strong and weak measured runs for auditability;
- reproducible notebook/report links;
- a measured extension with before/after evidence and an explicit adoption decision.

## Interpretation and limitations

The reported values are scoped to the project's recorded educational datasets and environments. Synthetic datasets are useful for reproducible assessment, but they are not a substitute for broader production validation. Before real deployment, the system should be re-evaluated for dialect, domain and temporal drift using appropriately governed data.

## Final evaluation status

**T3–T12 evaluation evidence:** ✅ COMPLETE  
**Slices / confidence / behavioural tests:** ✅ COMPLETE  
**108-row error analysis:** ✅ COMPLETE  
**Benchmark and serving evidence:** ✅ COMPLETE  
**Measured extension:** ✅ COMPLETE  
**Evaluation report:** ✅ COMPLETE

**Academy GitHub:** [@SDAIAAcademy](https://github.com/SDAIAAcademy)  
**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
