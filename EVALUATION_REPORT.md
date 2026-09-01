# EVALUATION_REPORT — Bayan

**Project:** Bayan — Bilingual Applied NLP Capstone  
**Training context:** Bayan — **#SDAIA**

## Evaluation policy

This report separates three evidence classes so that results cannot be overclaimed:

1. `MEASURED_SMOKE` — actual measurements on the small synthetic educational suites included with the course/integration notebook.
2. `MEASURED_LOCAL` — actual measurements on the documented local machine.
3. Academy-frozen/reference-lab evidence — external evidence that is not replaced or invented when the academy package or designated hardware is unavailable.

Controls:

`TEST_USED_FOR_SELECTION=False`  
`ACADEMY_FROZEN_EVAL_REPLACED=False`

The printed integration marker `BAYAN_DAY1_DAY4_OFFICIAL_THRESHOLDS=PASS` means that the included smoke suites meet the same numeric threshold values; it is not interpreted as an academy-frozen evaluation result.

---

## Evaluation sources

- Integration notebook: `notebooks/bayan_capstone.ipynb`
- Full semantic-search lab: `notebooks/06_semantic_search.ipynb`
- Full evaluation lab: `notebooks/07_evaluation_error_analysis.ipynb`
- Full optimization/serving lab: `notebooks/08_optimization_serving.ipynb`
- T9 evidence: `reports/T9_MANUAL_REVIEW.md`
- T9 rows: `reports/t9_manual_error_review.csv`
- Local T10 evidence: `reports/t10_local_cpu_http_benchmark.json`
- Additional preserved Day 2 smoke evidence: `reports/smoke/`

---

## Integration smoke results

| Requirement area | Measurement | Result | Evidence class |
|---|---|---:|---|
| Topic classification | Macro-F1 delta vs baseline | `+0.858` | `MEASURED_SMOKE` |
| Sentiment classification | Macro-F1 delta vs baseline | `+0.663` | `MEASURED_SMOKE` |
| NER | entity-level F1 | `1.000` | `MEASURED_SMOKE` |
| QA | no-answer correct | `20/20` | `MEASURED_SMOKE` |
| Search | Recall@10 | `1.000` | `MEASURED_SMOKE` |
| Search | MRR@10 | `1.000` | `MEASURED_SMOKE` |
| Behavioural | Invariance | `1.000` | `MEASURED_SMOKE` |
| Behavioural | MFT | `1.000` | `MEASURED_SMOKE` |
| Extension | Top-1 delta | `+0.88` | `MEASURED_SMOKE` |

These values are evidence that the project code paths and acceptance suites execute as intended. They are not production-accuracy estimates.

---

## R2 — classification, NER and QA interpretation

Program numeric targets include:

- classifier improvement over TF-IDF by at least `0.08` Macro-F1;
- NER entity F1 at least `0.80`;
- QA no-answer at least `17/20`.

The integration smoke suite is above those numeric values. However, official scoring remains tied to the academy-declared corpus/splits/evaluation package when supplied.

The repository also preserves weaker Day 2 short-training smoke runs under `reports/smoke/`. For example, one short NER fine-tuning smoke run produced F1 `0.0`. This is intentionally preserved rather than hidden because it demonstrates that separate smoke protocols can produce materially different results on tiny datasets.

---

## R3 — semantic search

The formal search lab uses the required two-stage architecture:

1. multilingual sentence embeddings;
2. L2 normalization;
3. FAISS `IndexFlatIP` candidate retrieval;
4. CrossEncoder reranking on a small retrieved candidate set.

Models used in the formal lab:

- embedding model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- reranker: `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`

The integration notebook uses a deterministic concept-canonicalization + lightweight reranking variant for its reproducible smoke suite; it does not replace the full formal search notebook.

Integration smoke:

- Recall@10 `1.000`
- MRR@10 `1.000`

Arabic/English slices and bootstrap confidence intervals are implemented in the evaluation path.

---

## R4 — behavioural evaluation and error analysis

Integration smoke:

- Invariance `1.000`
- MFT `1.000`

### 108-row reviewed error evidence

The repository now contains a row-by-row semantic review of **108 actual baseline retrieval errors**.

Summary:

- baseline errors reviewed: `108`
- improved system correct on those baseline errors: `106/108`
- improved residual errors: `2`
- correction rate on the reviewed baseline errors: `98.148%`

Categories:

| Category | Count |
|---|---:|
| `cross_language_intent_specificity_gap` | `56` |
| `hash_collision_candidate_ordering` | `44` |
| `modifier_noise_ranking_instability` | `8` |

Prioritized fixes:

1. keep bilingual concept canonicalization before embedding;
2. strengthen/replace the hashed lexical candidate representation;
3. harden reranking against low-information modifiers.

### Reviewer boundary

**Reviewer:** GPT-5.6 Sol  
**Method:** AI-assisted row-by-row semantic inspection  
**Independent human-review claim:** `FALSE`

This evidence satisfies the count and row-level inspection artifact in the repository, but it is not mislabeled as learner/instructor human review. If the academy explicitly requires a human reviewer, human confirmation or spot-checking remains necessary before making that stricter claim.

---

## R5 — performance and serving

### Formal benchmark path

`notebooks/08_optimization_serving.ipynb` implements the program benchmark ladder, including:

- device/runtime/version capture;
- explicit budget;
- warm-up and repeated measurements;
- p50/p95/p99;
- throughput;
- approximate process RSS/observed peak;
- FP32 reference;
- ONNX checker and ONNX Runtime;
- numerical/prediction parity;
- dynamic INT8 candidate;
- quality tax;
- FP32 rollback/fallback;
- FastAPI and startup canaries.

### Local real-HTTP measurement

Environment:

- Windows 11 local CPU
- logical CPUs: `8`
- concurrency: `16`
- warm-up requests: `32`
- measured requests: `128`

Results:

| Metric | Result |
|---|---:|
| HTTP p50 | `19.172 ms` |
| HTTP p95 | `24.805 ms` |
| HTTP p99 | `27.903 ms` |
| HTTP mean | `18.340 ms` |

The local result is below the program numeric target of `40 ms` at concurrency `16`.

**Evidence class:** `MEASURED_LOCAL`.

**Hardware boundary:** the machine is not identified as the academy reference lab CPU. Therefore this report records the local result without claiming official hardware equivalence.

The local JSON artifact records latency statistics but not local-run throughput or peak RSS. Those fields are implemented by the formal Notebook 08 benchmark schema; no local throughput/RSS value is fabricated for the `27.903 ms` run.

---

## R6 — architectural evidence

Day 1 measured tokenizer fertility:

| Tokenizer | Arabic fertility | English fertility |
|---|---:|---:|
| mBERT | `2.595` | `1.299` |
| AraBERT | `1.182` | `3.714` |

The bilingual decision therefore favors a multilingual tokenizer/checkpoint family rather than optimizing only for Arabic token count.

Architecture documentation also records:

- attention score shapes;
- `sqrt(d_k)` scaling;
- padding-mask semantics;
- self-attention quadratic sequence-length cost in the score matrix;
- truncation as a measured design risk;
- bilingual slice evidence.

See `reports/day1_report.md` and `DECISIONS.md`.

---

## R7 — extension and evaluation integrity

Measured extension:

**Bilingual concept canonicalization + reranking**

Integration smoke:

- before Top-1: `0.10`
- after Top-1: `0.98`
- delta: `+0.88`

The notebook prints `KEEP` for a positive delta. Final documentation uses the normalized decision word:

`ADOPT`

These labels represent the same decision: retain the measured improved candidate.

---

## Program-alignment summary

| Requirement | Repository status | Official-boundary status |
|---|---|---|
| R1 | implementation + tests/canaries present | academy-specific canary package, if supplied, remains external |
| R2 | complete code paths + smoke measurements | academy-frozen model evaluation not replaced |
| R3 | formal SentenceTransformer + FAISS + CrossEncoder path present | frozen query package not replaced |
| R4 | behavioural smoke + 108 AI-assisted reviewed errors + top-3 fixes | independent human-review claim not made |
| R5 | full benchmark/rollback path + local real HTTP evidence | academy reference CPU not claimed |
| R6 | fertility, attention, truncation, slices and rationale documented | complete repository evidence |
| R7 | hygiene, reproducibility controls and measured extension present | final tag must be refreshed after latest validation |

---

## Final evaluation status

**Repository evaluation documentation:** ✅ ALIGNED  
**Smoke/local evidence:** ✅ RECORDED  
**T9 AI-assisted 108-row review:** ✅ RECORDED  
**Academy frozen evaluation replaced:** ❌ NO  
**Academy reference CPU claimed:** ❌ NO  
**Final release tag:** ⏳ REFRESH AFTER FINAL CI/VALIDATION

**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
