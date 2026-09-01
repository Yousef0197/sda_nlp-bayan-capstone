# MODEL_CARD — Bayan

**Project:** Bayan — Bilingual Applied NLP Capstone  
**Program:** SDA-AIE-211 — Natural Language Processing with Transformers  
**Academy:** [@SDAIAAcademy](https://github.com/SDAIAAcademy) — **#SDAIA**  
**Model card status:** ✅ **COMPLETE**

## System overview

Bayan is an educational bilingual Arabic/English NLP system that demonstrates:

- versioned preprocessing and PII masking;
- topic and sentiment classification;
- named entity recognition;
- extractive QA with no-answer handling;
- bilingual semantic search;
- behavioural evaluation and error analysis;
- benchmark and optimisation paths;
- FastAPI serving;
- one measured extension.

## Intended use

The project is intended for applied NLP learning, assessment and reproducible experimentation. It demonstrates how to connect model decisions, evaluation evidence, serving and engineering trade-offs in one auditable repository.

The system is not intended to serve as an authoritative high-stakes decision system.

## Languages

- Arabic
- English

## Main task checkpoint

Integrated task-training paths use:

`distilbert/distilbert-base-multilingual-cased`

The multilingual family is used because the project targets a shared Arabic/English workflow.

## Tokenizer decision

Measured Day 1 fertility:

| Tokenizer | Arabic fertility | English fertility |
|---|---:|---:|
| mBERT | `2.595` | `1.299` |
| AraBERT | `1.182` | `3.714` |

The bilingual path selects a multilingual family because the measured sample shows a stronger balance across the two target languages.

Architecture evidence also covers:

- truncation measurement;
- attention score shape `T_q × T_k`;
- `sqrt(d_k)` scaling;
- mask semantics;
- quadratic sequence-length growth of self-attention score matrices.

Evidence: `reports/day1_report.md`, `notebooks/02_attention_transformers.ipynb`, `DECISIONS.md`.

## Classification

The classification workflow includes:

- TF-IDF baseline;
- multilingual Transformer comparison;
- Macro-F1 evaluation;
- topic and sentiment tasks.

Measured deltas:

- Topic: `+0.858`
- Sentiment: `+0.663`

**Status:** ✅ COMPLETE

## Named Entity Recognition

NER evidence includes:

- `word_ids()` alignment;
- ignored/special position handling with `-100`;
- entity-level precision/recall/F1 evaluation;
- alignment tests.

Measured entity F1:

`1.000`

**Status:** ✅ COMPLETE

## Extractive QA

QA evidence includes:

- start/end span preparation;
- offsets;
- valid-span constraints;
- explicit no-answer handling;
- post-processing tests.

Measured no-answer result:

`20/20`

**Status:** ✅ COMPLETE

## Arabic processing profile

The project uses one documented Arabic processing contract across train/eval/serve and verifies it with canaries and tests. The formal Arabic notebook integrates CAMeL Tools for Arabic-specific processing evidence.

**Status:** ✅ COMPLETE

## Semantic search

Formal architecture:

`text → preprocessing → multilingual sentence embeddings → L2 normalization → FAISS IndexFlatIP → top-k candidates → CrossEncoder reranking`

Models:

- embedding model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- reranker: `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`

Measured retrieval results:

- Recall@10: `1.000`
- MRR@10: `1.000`

**Status:** ✅ COMPLETE

## Behavioural evaluation

The evaluation path includes:

- Arabic/English slices;
- confidence-interval utilities;
- invariance tests;
- Minimum Functionality Tests.

Measured results:

- Invariance: `1.000`
- MFT: `1.000`

**Status:** ✅ COMPLETE

## Error analysis

Current row-level evidence:

- baseline errors reviewed: `108`
- improved path correct on reviewed baseline errors: `106/108`
- residual improved errors: `2`

Categories:

- cross-language intent/specificity gap: `56`
- hash-collision/candidate-ordering errors: `44`
- modifier-noise ranking instability: `8`

Prioritized fixes:

1. retain bilingual concept canonicalization;
2. strengthen candidate representation;
3. harden reranking against low-information modifiers.

Evidence:

- `reports/T9_MANUAL_REVIEW.md`
- `reports/t9_manual_error_review.csv`

**Status:** ✅ COMPLETE

## Serving

Serving contracts include:

- `GET /health`
- `POST /v1/classify`
- Arabic and English requests
- input validation
- PII masking
- manifest/version checks
- startup canaries
- stable JSON response metadata

Evidence: `src/bayan/serving.py`, `tests/test_day4_serving.py`, Notebook 08.

**Status:** ✅ COMPLETE

## Performance and optimisation

Formal Notebook 08 includes:

- FP32 reference;
- warm-up and repeated measurements;
- p50/p95/p99;
- throughput;
- approximate process RSS/observed peak;
- ONNX checker and ONNX Runtime path;
- prediction/numerical parity;
- INT8 candidate;
- quality tax;
- FP32 rollback;
- FastAPI canaries.

Real HTTP evidence:

| Metric | Result |
|---|---:|
| concurrency | `16` |
| warm-up requests | `32` |
| measured requests | `128` |
| p50 | `19.172 ms` |
| p95 | `24.805 ms` |
| p99 | `27.903 ms` |
| mean | `18.340 ms` |

**Status:** ✅ COMPLETE

## Measured extension

Extension:

**Bilingual concept canonicalization + reranking**

Measured comparison on the same integration workload:

- before Top-1 `0.10`
- after Top-1 `0.98`
- delta `+0.88`

Decision:

`ADOPT`

**Status:** ✅ COMPLETE

## Data and privacy

- synthetic educational data;
- no intentional real citizen/customer PII;
- synthetic email/phone canaries for masking tests;
- `.env`, secrets, model weights and large checkpoints excluded from GitHub;
- privacy and preprocessing behaviour covered by tests.

## Known limitations

1. Synthetic educational datasets do not represent all production dialects or domains.
2. Small training runs can show higher variance than larger curated datasets.
3. Search quality should be re-evaluated when the corpus or intent distribution changes.
4. Real deployment requires ongoing monitoring for domain, dialect and temporal drift.
5. The system is educational and should not be used as an unchecked high-stakes decision authority.

## Reproducibility

The repository provides:

- nine required Colab notebooks;
- integration notebook;
- reusable source modules;
- dedicated tests;
- GitHub Actions CI;
- machine-readable `PROJECT_SUMMARY.json`;
- `SUBMISSION.yml`;
- submission validator;
- final release tag contract.

## Distinction evidence

The model package includes deeper evidence through bilingual slices, confidence intervals, behavioural tests, structured error analysis, automated CI, reproducibility artifacts and a measured before/after extension.

## Final status

**Model/task documentation:** ✅ COMPLETE  
**Evaluation evidence:** ✅ COMPLETE  
**Privacy and limitations:** ✅ COMPLETE  
**Serving and benchmark documentation:** ✅ COMPLETE  
**Measured extension:** ✅ COMPLETE  
**MODEL CARD:** ✅ COMPLETE

**Academy GitHub:** [@SDAIAAcademy](https://github.com/SDAIAAcademy)  
**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
