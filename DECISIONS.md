# DECISIONS — Bayan

يوثّق هذا الملف القرارات الهندسية النهائية لمشروع **Bayan — Bilingual Applied NLP Capstone** مع ربط القرار بالدليل وحدود الادعاء المطلوبة في البرنامج.

**Training context:** Bayan — [@SDAIAAcademy](https://github.com/SDAIAAcademy) — **#SDAIA**

## Evidence vocabulary

- `MEASURED_SMOKE`: قياس حقيقي على حزمة تعليمية صغيرة؛ لا يستبدل التقييم المجمد للأكاديمية.
- `MEASURED_LOCAL`: قياس حقيقي على جهاز الطالب/المطور الموثق؛ لا يُنسب إلى جهاز مختبر مرجعي مختلف.
- `IMPLEMENTED`: المسار البرمجي موجود وقابل للفحص.
- `ADOPT`: القرار النهائي في التوثيق باعتماد التغيير بعد قياس إيجابي.

---

## D-001 — Preprocessing and privacy contract

**Decision:** استخدام مسار versioned موحّد للمعالجة مع فصل النص المعروض عن نسخة النموذج، وإخفاء PII قبل مسارات النموذج.

**Why:** تقليل train/eval/serve skew ومنع تسرب بيانات حساسة إلى التمثيل المستخدم في النماذج.

**Evidence:**

- `src/bayan/preprocessing.py`
- `src/bayan/arabic_profiles.py`
- `tests/test_day1_preprocessing.py`
- `tests/test_day3_arabic_profiles.py`
- startup/manifest canaries in serving path.

**Status:** `IMPLEMENTED`.

---

## D-002 — Bilingual tokenizer family

**Decision:** تفضيل tokenizer/checkpoint متعدد اللغات عندما يكون المطلوب مسارًا واحدًا للعربية والإنجليزية، بدل اختيار tokenizer عربي فقط بسبب انخفاض fertility العربية.

**Measured Day 1 evidence:**

| Tokenizer | Arabic fertility | English fertility |
|---|---:|---:|
| mBERT | `2.595` | `1.299` |
| AraBERT | `1.182` | `3.714` |

AraBERT كان أكثر اقتصادًا للعربية في العينة، لكنه أعلى بكثير في fertility الإنجليزية. mBERT أعطى توازنًا أفضل للمسار الثنائي اللغة.

Truncation on the small Day 1 sample was `0%` at `max_length=32` and `64`, but this is not used to claim that short sequence lengths are universally safe.

**Evidence:** `reports/day1_report.md`.

**Status:** `ADOPT multilingual tokenizer family`.

---

## D-003 — Transformer checkpoint for task smoke paths

**Decision:** استخدام:

`distilbert/distilbert-base-multilingual-cased`

في مسارات التدريب التعليمية المدمجة.

**Why:** checkpoint متعدد اللغات ومتوافق مع هدف المشروع الثنائي اللغة، وأخف من BERT-base الكامل لتجارب Colab التعليمية القصيرة.

**Boundary:** نتائج fine-tuning الصغيرة تبقى `MEASURED_SMOKE`; لا تُقرأ كجودة إنتاجية أو تقييم مجمد.

**Status:** `IMPLEMENTED`.

---

## D-004 — Attention and sequence-length constraints

**Decision:** توثيق حدود attention صراحة وعدم التعامل مع `max_length` كرقم ثابت بلا قياس.

**Evidence:**

- attention score matrix has shape `T_q × T_k`;
- self-attention therefore has quadratic sequence-length memory/compute growth in the score matrix;
- scaled dot-product attention uses `sqrt(d_k)` scaling;
- padding-mask semantics are verified rather than assumed across APIs;
- truncation is measured before choosing a production sequence length.

**Why:** R6 requires connecting architecture literacy to practical model choices rather than only reporting task metrics.

**Evidence:** `reports/day1_report.md`, `notebooks/02_attention_transformers.ipynb`.

**Status:** `DOCUMENTED`.

---

## D-005 — Topic and sentiment classification

**Decision:** الاحتفاظ بـTF-IDF baseline منفصل، ثم مقارنة Transformer against baseline using Macro-F1.

Integration smoke evidence:

- Topic delta: `+0.858`
- Sentiment delta: `+0.663`

**Evidence class:** `MEASURED_SMOKE`.

The separately preserved Day 2 short-training smoke reports may be weaker; they are intentionally retained under `reports/smoke/` instead of hidden. Different smoke runs therefore are not conflated.

**Status:** `IMPLEMENTED`; official frozen threshold claim is deferred to the academy package when supplied.

---

## D-006 — NER and QA

**NER decision:** use `word_ids()` alignment and `-100` for ignored/special/continuation positions according to the training contract.

**QA decision:** use extractive start/end spans with valid-span checks and explicit no-answer handling.

Integration smoke evidence:

- NER entity F1: `1.000`
- QA no-answer: `20/20`

**Evidence class:** `MEASURED_SMOKE`.

The preserved short-training Day 2 smoke file with NER F1 `0.0` remains in `reports/smoke/day2_ner_qa_metrics.json`; it is a different, deliberately short run and is not overwritten by the integration acceptance suite.

**Status:** `IMPLEMENTED`.

---

## D-007 — Arabic processing profile and CAMeL Tools

**Decision:** use one documented Arabic preprocessing contract across train/eval/serve and keep CAMeL Tools inside the formal Arabic lab where it adds explicit Arabic normalization functionality.

**Why:** avoid silent preprocessing skew and make Arabic-specific behavior reviewable.

**Evidence:**

- `notebooks/05_arabic_nlp.ipynb`
- `src/bayan/arabic_profiles.py`
- Arabic canaries and tests.

**Status:** `IMPLEMENTED`.

---

## D-008 — Semantic search architecture

**Formal lab decision:**

1. multilingual sentence embeddings using `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`;
2. L2 normalisation;
3. FAISS `IndexFlatIP` candidate retrieval;
4. re-rank a small candidate set using `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`;
5. evaluate retrieval quality and latency before adopting the reranker.

**Why:** the CrossEncoder reads query and candidate jointly and is therefore applied only after first-stage retrieval.

**Evidence:** `notebooks/06_semantic_search.ipynb`.

**Integration-smoke variant:** `notebooks/bayan_capstone.ipynb` uses deterministic bilingual concept canonicalization plus lightweight lexical reranking so the combined notebook can run reproducibly without replacing the fuller formal lab.

Integration smoke metrics:

- Recall@10: `1.000`
- MRR@10: `1.000`

**Status:** formal required architecture `IMPLEMENTED`; metrics are `MEASURED_SMOKE` unless measured on an academy-frozen query package.

---

## D-009 — Evaluation, uncertainty and behavioural tests

**Decision:** do not report one aggregate metric only. Preserve:

- Arabic/English slices;
- bootstrap confidence intervals where applicable;
- Invariance;
- Minimum Functionality Tests;
- error taxonomy and prioritized fixes.

Integration smoke:

- Invariance: `1.000`
- MFT: `1.000`

**Status:** `IMPLEMENTED`, `MEASURED_SMOKE`.

---

## D-010 — T9 error-analysis review

**Decision:** expand the previous 20-row review evidence to a row-by-row semantic review of more than the program minimum.

Current evidence:

- reviewed baseline errors: `108`
- improved path correct on reviewed baseline errors: `106/108`
- residual improved errors: `2`

Categories:

- `cross_language_intent_specificity_gap`: `56`
- `hash_collision_candidate_ordering`: `44`
- `modifier_noise_ranking_instability`: `8`

Prioritized fixes:

1. retain bilingual concept canonicalization before embedding;
2. replace/strengthen hashed lexical candidate representation;
3. harden reranking against low-information modifiers.

**Reviewer:** GPT-5.6 Sol, AI-assisted row-by-row semantic review.

`T9_HUMAN_REVIEW_CLAIM=FALSE`

**Why the boundary matters:** the project may claim that 108 rows were inspected and categorized by an AI assistant, but it must not relabel this as independent learner/instructor human review.

**Evidence:**

- `reports/T9_MANUAL_REVIEW.md`
- `reports/t9_manual_error_review.csv`

**Status:** `AI_ASSISTED_REVIEW_COMPLETE`; human confirmation remains external if the academy explicitly requires it.

---

## D-011 — FastAPI and serving contracts

**Decision:** expose stable service contracts and fail closed on manifest/preprocessing mismatch.

Evidence includes:

- `GET /health`
- `POST /v1/classify`
- Arabic and English requests
- invalid-input validation
- PII masking canary
- manifest/version helpers
- startup canaries.

**Evidence:** `src/bayan/serving.py`, `tests/test_day4_serving.py`, Notebook 08.

**Status:** `IMPLEMENTED`.

---

## D-012 — Performance benchmark and rollback

**Decision:** keep a benchmark ladder instead of optimizing one latency number in isolation.

Formal Notebook 08 covers:

- PyTorch FP32 reference;
- warm-up and repeated measurements;
- p50/p95/p99 and throughput;
- approximate process RSS/observed peak;
- ONNX checker and ORT session;
- numerical/prediction parity;
- dynamic INT8 candidate;
- quality tax;
- FP32 fallback/rollback;
- service canaries.

Additional `MEASURED_LOCAL` real-HTTP evidence:

- Windows 11 local CPU
- 8 logical CPUs
- concurrency `16`
- warm-up `32`
- measured requests `128`
- p50 `19.172 ms`
- p95 `24.805 ms`
- p99 `27.903 ms`
- mean `18.340 ms`

**Decision on this evidence:** local target `p99 <= 40 ms` is met.

**Boundary:** this machine is not called the academy reference lab CPU unless the academy explicitly identifies it as such.

**Evidence:** `BENCHMARKS.md`, `reports/t10_local_cpu_http_benchmark.json`, `notebooks/08_optimization_serving.ipynb`.

**Status:** `MEASURED_LOCAL`; official hardware-specific R5 claim depends on the designated lab environment.

---

## D-013 — Measured extension

**Extension:** bilingual concept canonicalization + reranking.

Integration smoke result:

- before Top-1: `0.10`
- after Top-1: `0.98`
- delta: `+0.88`

The integration notebook prints `KEEP` when the delta is positive. Release documentation normalizes that semantic decision to:

`ADOPT`

**Why:** `KEEP` and `ADOPT` refer to the same measured outcome — retain/deploy the better candidate. Documentation uses `ADOPT` consistently as the final decision vocabulary.

**Status:** `ADOPT`, `MEASURED_SMOKE`.

---

## D-014 — Frozen-test and evidence integrity

**Decision:** never convert course smoke data into an academy-frozen result.

Recorded controls:

- `TEST_USED_FOR_SELECTION=False`
- `ACADEMY_FROZEN_EVAL_REPLACED=False`
- no model weights/checkpoints/secrets committed;
- weaker or failed smoke measurements are preserved instead of deleted.

**Status:** `ADOPT`.

---

## D-015 — Release and tag integrity

**Decision:** a release tag must identify the final validated commit, not merely exist somewhere in history.

`submission-v1.0` currently predates the latest evidence-alignment commits. It must be refreshed after the final `main` commit passes tests and the submission validator.

Final freeze sequence:

1. tests pass;
2. submission validator passes;
3. refresh `submission-v1.0` to the final commit;
4. fresh clone;
5. run validator with `--require-tag`;
6. submit the public repository/release link according to academy instructions.

**Status:** `PENDING_FINAL_TAG_REFRESH`.

---

## Final decision summary

**Implementation:** COMPLETE  
**Documentation alignment:** COMPLETE  
**Measured smoke/local evidence:** RECORDED  
**AI-assisted 108-row T9 review:** COMPLETE  
**Frozen-evaluation substitution:** NOT CLAIMED  
**Reference-lab substitution:** NOT CLAIMED  
**Final release tag:** REFRESH AFTER FINAL VALIDATION

**Academy GitHub:** [@SDAIAAcademy](https://github.com/SDAIAAcademy)  
**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
