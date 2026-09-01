# DECISIONS — Bayan

يوثّق هذا الملف القرارات الهندسية النهائية لمشروع **Bayan — Bilingual Applied NLP Capstone** ويربط كل قرار بالدليل المقاس أو الاختبار المقابل له.

**Program:** SDA-AIE-211 — Natural Language Processing with Transformers  
**Academy:** [@SDAIAAcademy](https://github.com/SDAIAAcademy) — **#SDAIA**  
**Decision record status:** ✅ **COMPLETE**

## D-001 — Versioned preprocessing and privacy

**Decision:** استخدام خط معالجة موحّد وقابل للإصدار مع فصل النص المعروض عن نسخة النموذج وتطبيق PII masking قبل مسارات النموذج.

**Why:** تقليل train/eval/serve skew وحماية البيانات قبل التمثيل أو الاستدلال.

**Evidence:**

- `src/bayan/preprocessing.py`
- `src/bayan/arabic_profiles.py`
- `tests/test_day1_preprocessing.py`
- serving canaries

**Status:** ✅ ADOPTED

## D-002 — Bilingual tokenizer family

**Decision:** اعتماد عائلة tokenizer/checkpoint متعددة اللغات لمسار عربي/إنجليزي موحّد.

Measured fertility:

| Tokenizer | Arabic | English |
|---|---:|---:|
| mBERT | `2.595` | `1.299` |
| AraBERT | `1.182` | `3.714` |

**Interpretation:** AraBERT أكثر اقتصادًا في العينة العربية، بينما mBERT أكثر توازنًا عبر اللغتين، وهو الأنسب لمسار ثنائي اللغة واحد.

**Evidence:** `reports/day1_report.md`

**Status:** ✅ ADOPTED

## D-003 — Multilingual task checkpoint

**Decision:** استخدام:

`distilbert/distilbert-base-multilingual-cased`

لمسارات التدريب التعليمية المدمجة.

**Why:** checkpoint متعدد اللغات وخفيف نسبيًا لتجارب Colab القصيرة مع الحفاظ على هدف المشروع الثنائي اللغة.

**Status:** ✅ ADOPTED

## D-004 — Explicit sequence-length and attention constraints

**Decision:** قياس truncation وتوثيق تكلفة attention بدل اختيار `max_length` بشكل عشوائي.

Evidence includes:

- attention score shape `T_q × T_k`;
- `sqrt(d_k)` scaling;
- mask semantics;
- quadratic self-attention score-matrix cost;
- measured truncation evidence.

**Status:** ✅ ADOPTED

## D-005 — Preserve TF-IDF baseline

**Decision:** الاحتفاظ بـTF-IDF baseline ومقارنة Transformer به باستخدام Macro-F1 بدل عرض نتيجة النموذج منفردة.

Measured deltas:

- Topic: `+0.858`
- Sentiment: `+0.663`

**Why:** المقارنة المباشرة تجعل التحسن قابلاً للدفاع والمراجعة.

**Status:** ✅ ADOPTED

## D-006 — NER alignment contract

**Decision:** استخدام `word_ids()` لمحاذاة subwords مع تجاهل المواقع غير المخصصة للخسارة عبر `-100` وفق عقد التدريب.

Measured integration entity F1:

`1.000`

**Evidence:** `notebooks/04_ner_and_qa.ipynb`, `src/bayan/ner_alignment.py`

**Status:** ✅ ADOPTED

## D-007 — Extractive QA with explicit no-answer handling

**Decision:** استخدام start/end spans مع offsets وقيود span صحيحة ومسار صريح لحالة no-answer.

Measured result:

`20/20`

**Status:** ✅ ADOPTED

## D-008 — Unified Arabic profile

**Decision:** استخدام عقد معالجة عربي موحّد عبر train/eval/serve مع canaries واختبارات، وإدخال CAMeL Tools داخل المختبر العربي الرسمي عند الحاجة.

**Why:** منع اختلاف المعالجة الصامت بين التدريب والتقييم والخدمة.

**Status:** ✅ ADOPTED

## D-009 — Two-stage semantic search

**Decision:** استخدام بنية بحث من مرحلتين:

1. multilingual sentence embeddings;
2. L2 normalization;
3. FAISS `IndexFlatIP` retrieval;
4. small top-k candidate set;
5. CrossEncoder reranking.

Models:

- `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`

Measured integration results:

- Recall@10 `1.000`
- MRR@10 `1.000`

**Status:** ✅ ADOPTED

## D-010 — Evaluate slices and behaviour, not one score

**Decision:** إضافة Arabic/English slices وconfidence intervals واختبارات Invariance وMFT بجانب المقاييس الإجمالية.

Measured behavioural results:

- Invariance `1.000`
- MFT `1.000`

**Why:** الأداء الإجمالي وحده قد يخفي نقاط ضعف لغوية أو سلوكية.

**Status:** ✅ ADOPTED

## D-011 — T9 error-analysis policy

**Decision:** مراجعة أكثر من الحد المطلوب وتصنيف الأخطاء حسب آلية الفشل، ثم تحويل النتائج إلى إصلاحات مرتبة.

Current evidence:

- reviewed baseline errors: `108`
- improved path correct: `106/108`
- residual errors: `2`

Categories:

- `cross_language_intent_specificity_gap`: `56`
- `hash_collision_candidate_ordering`: `44`
- `modifier_noise_ranking_instability`: `8`

Prioritized fixes:

1. retain bilingual concept canonicalization;
2. strengthen candidate representation;
3. harden reranking against low-information modifiers.

**Status:** ✅ ADOPTED

## D-012 — FastAPI service contract

**Decision:** توفير خدمة صغيرة بعقود ثابتة وقابلة للاختبار.

Endpoints and behaviours:

- `GET /health`
- `POST /v1/classify`
- Arabic and English requests
- invalid-input validation
- PII masking
- startup/manifest canaries

**Status:** ✅ ADOPTED

## D-013 — Benchmark ladder and rollback

**Decision:** عدم اعتماد تحسين الأداء على latency منفردة؛ يجب قياس tail latency، throughput، memory، parity وquality tax مع fallback واضح.

Formal Notebook 08 covers:

- PyTorch FP32 reference;
- ONNX Runtime candidate;
- INT8 candidate;
- p50/p95/p99;
- throughput;
- approximate RSS peak;
- parity;
- quality tax;
- rollback.

Real HTTP measurement:

- concurrency `16`
- p99 `27.903 ms`

**Status:** ✅ ADOPTED

## D-014 — Measured extension

**Extension:** bilingual concept canonicalization + reranking.

Same-workload comparison:

- before Top-1 `0.10`
- after Top-1 `0.98`
- delta `+0.88`

**Decision:** `ADOPT`

**Why:** التحسن المقاس موجب وكبير على workload نفسه، والقرار مرتبط بالنتيجة وليس بإضافة شكلية.

**Status:** ✅ ADOPTED

## D-015 — Reproducible submission contract

**Decision:** جعل المستودع نفسه قابلاً للفحص عبر:

- nine required notebooks;
- modular `src/`;
- dedicated `tests/`;
- GitHub Actions CI;
- `PROJECT_SUMMARY.json`;
- `SUBMISSION.yml`;
- local submission validator;
- final tag `submission-v1.0`.

**Status:** ✅ ADOPTED

## Distinction rationale

The final project emphasizes evidence depth and engineering quality:

- multiple evaluation views rather than one score;
- reproducible measurements and explicit environments;
- automated tests and CI;
- structured error analysis with three prioritized fixes;
- a measured before/after extension with an explicit `ADOPT` decision;
- clear data, model, evaluation, benchmark and decision documentation.

## Final decision summary

**Preprocessing/privacy:** ✅ ADOPTED  
**Bilingual tokenizer/model path:** ✅ ADOPTED  
**Tasks and evaluation:** ✅ ADOPTED  
**Semantic search:** ✅ ADOPTED  
**Serving/benchmark:** ✅ ADOPTED  
**Measured extension:** ✅ ADOPTED  
**Submission/reproducibility:** ✅ ADOPTED  
**Decision documentation:** ✅ COMPLETE

**Academy GitHub:** [@SDAIAAcademy](https://github.com/SDAIAAcademy)  
**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
