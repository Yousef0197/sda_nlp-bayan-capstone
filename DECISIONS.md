# DECISIONS — Bayan

يوثّق هذا الملف القرارات الهندسية النهائية لمشروع **Bayan — Bilingual Applied NLP Capstone** بعد اكتمال التنفيذ والتقييم والتوثيق والتسليم.

**Training context:** Bayan — #SDAIA

---

## D-001 — Bilingual preprocessing

**Status:** ✅ COMPLETE

**Decision:** اعتماد مسار موحّد للمعالجة في التدريب والتقييم والخدمة، يشمل Unicode normalization، معالجة العربية، ضبط المسافات، وPII masking.

**Reason:** تقليل الاختلاف بين مراحل النظام وتحسين ثبات النتائج.

**Result:** PASS

---

## D-002 — Canonical notebook

**Status:** ✅ COMPLETE

**Decision:** اعتماد الملف التالي كمرجع التشغيل النهائي للمشروع:

`notebooks/bayan_capstone.ipynb`

ويجمع مختبرات Day 1–Day 4 في Notebook واحد قابل لإعادة التشغيل.

**Result:** PASS

---

## D-003 — Topic & Sentiment Classification

**Status:** ✅ COMPLETE

**Decision:** استخدام TF-IDF كـbaseline ثم مقارنة النتائج بمسار Transformer.

**Measured results:**

- Topic Macro-F1 delta: `+0.858`
- Sentiment Macro-F1 delta: `+0.663`

**Result:** PASS

---

## D-004 — Named Entity Recognition

**Status:** ✅ COMPLETE

**Decision:** استخدام `word_ids()` لمحاذاة الكلمات والـsubwords، مع `-100` للمواضع غير الداخلة في حساب الخسارة.

**Measured result:**

- Entity-level F1: `1.000`

**Result:** PASS

---

## D-005 — Extractive Question Answering

**Status:** ✅ COMPLETE

**Decision:** استخدام start/end span مع valid-span constraints ودعم no-answer.

**Measured result:**

- No-answer: `20/20`

**Result:** PASS

---

## D-006 — Unified Arabic profile

**Status:** ✅ COMPLETE

**Decision:** استخدام نفس ملف المعالجة العربية في train / eval / serve.

كما تم اعتماد Arabic canaries للتحقق من ثبات المسار.

**Result:** PASS

---

## D-007 — Semantic Search

**Status:** ✅ COMPLETE

**Decision:** استخدام FAISS للاسترجاع مع bilingual concept canonicalization وreranking.

**Measured results:**

- Recall@10: `1.000`
- MRR@10: `1.000`

**Reason:** تحسين المطابقة ثنائية اللغة وتقليل أثر الفجوة المعجمية بين العربية والإنجليزية.

**Result:** PASS

---

## D-008 — Behavioural Evaluation

**Status:** ✅ COMPLETE

**Decision:** إضافة اختبارات Invariance وMinimum Functionality Tests ضمن التقييم النهائي، وعدم الاكتفاء بالمقاييس التقليدية.

**Measured results:**

- Invariance: `1.000`
- MFT: `1.000`

**Result:** PASS

---

## D-009 — Error Analysis

**Status:** ✅ COMPLETE

**Decision:** إنشاء جدول من `100` حالة للمراجعة، ثم تنفيذ مراجعة بشرية فعلية على `20` خطأ وتصنيفها وتحديد ثلاثة إصلاحات مرتبة حسب الأولوية.

### Manual review categories

- candidate_ordering: `12`
- cross_language_lexical_gap: `5`
- normalization_drift: `3`

### Prioritized fixes

1. bilingual concept canonicalization before embedding.
2. FAISS candidate retrieval + reranking.
3. unified train/eval/serve Arabic profile.

### Evidence

- `reports/T9_MANUAL_REVIEW.md`
- `reports/t9_manual_error_review.csv`

**Result:** PASS

---

## D-010 — FastAPI Serving

**Status:** ✅ COMPLETE

**Decision:** اعتماد FastAPI لخدمة المشروع.

**Endpoints:**

- `GET /health`
- `POST /v1/classify`

يشمل الاختبار:

- Arabic input
- English input
- invalid input
- startup/API canaries
- PII masking

**Result:** PASS

---

## D-011 — Performance Benchmark

**Status:** ✅ COMPLETE

**Target:**

`HTTP p99 <= 40 ms` عند concurrency = `16`

### Benchmark ladder

تم اعتماد مسار قياس تدريجي يشمل:

- direct classification path.
- cached classification path.
- prediction parity.
- FastAPI / ASGI smoke measurement.
- real HTTP local CPU benchmark.

### Prediction parity

تم التحقق من تطابق المخرجات بين المسار المباشر والمسار المحسن:

`Prediction parity = 1.0`

`DAY4_BENCHMARK_PARITY=PASS`

ولم تظهر تغييرات في التنبؤات على حالات parity المقاسة.

### Final measured result

بيئة القياس النهائي:

- Platform: Windows 11
- CPU count: `8`
- Concurrency: `16`
- Warm-up requests: `32`
- Measured requests: `128`

النتائج:

- HTTP p50: `19.172 ms`
- HTTP p95: `24.805 ms`
- HTTP p99: `27.903 ms`
- HTTP mean: `18.340 ms`

العلامات:

`T10_LOCAL_CPU_HTTP_TARGET_MET=True`

`T10_LOCAL_CPU_HTTP_BENCHMARK=PASS`

الدليل:

`reports/t10_local_cpu_http_benchmark.json`

### Environment boundary

القياس النهائي تم على CPU محلي بنظام Windows.

لا يُنسب الجهاز إلى academy lab CPU محدد إلا إذا كانت البيئة الرسمية مطابقة ومعلنة.

هذه الملاحظة توثّق بيئة القياس ولا تغيّر حالة اكتمال المشروع.

**Result:** PASS

---

## D-012 — Measured Extension

**Implementation status:** ✅ COMPLETE

**Extension:** bilingual concept canonicalization + reranking.

**Measured result:**

- Top-1 delta: `+0.88`

**Decision:** ADOPT

**T12 status:** ✅ PASS

تم اعتماد الامتداد بعد القياس لأن المقارنة قبل/بعد أظهرت تحسنًا موجبًا في Top-1 بمقدار `+0.88`.

---

## D-013 — Final Validation

**Status:** ✅ COMPLETE

تم تنفيذ التحقق النهائي للمشروع بعد اكتمال الملفات المطلوبة والتوثيق والـNotebook المرجعي.

تم تشغيل الـsubmission validator من Fresh Clone للوسم النهائي، وكانت النتيجة:

`BAYAN_SUBMISSION_VALIDATOR=PASS`

وشملت الفحوص:

- Required project structure.
- Nine valid notebooks and Core markers.
- `PROJECT_SUMMARY.json` contract.
- `SUBMISSION.yml` contract.
- No forbidden or oversized tracked artefacts.
- Final Git tag `submission-v1.0`.

**Result:** PASS

---

## D-014 — Presentation

**Status:** ✅ COMPLETE

تم تجهيز العرض النهائي للمشروع واستكمال متطلب العرض.

**Result:** COMPLETE

---

## D-015 — Public Repository & Colab Verification

**Status:** ✅ COMPLETE

تم التحقق من إمكانية الوصول إلى:

- المستودع العام على GitHub من نافذة خاصة.
- الـcanonical notebook على Google Colab من نافذة خاصة.

رابط Colab:

https://colab.research.google.com/github/Yousef0197/sda_nlp-bayan-capstone/blob/main/notebooks/bayan_capstone.ipynb

**Result:** PASS

---

## D-016 — Final Release

**Status:** ✅ COMPLETE

تم اعتماد وسم الإصدار النهائي:

`submission-v1.0`

ويمثل النسخة النهائية المخصصة للتسليم بعد اكتمال التوثيق والتحقق.

**Result:** COMPLETE

---

## D-017 — Evidence interpretation

**Status:** ✅ COMPLETE

تم اعتماد الحدود التالية عند تفسير النتائج:

- `MEASURED_SMOKE=True`
- `TEST_USED_FOR_SELECTION=False`
- `ACADEMY_FROZEN_EVAL_REPLACED=False`

نتائج الـcanonical notebook ناتجة من تشغيل فعلي للحزم التعليمية الاصطناعية.

نتيجة T10 النهائية `27.903 ms` مصدرها قياس real HTTP محلي منفصل وموثق في `reports/`.

النتائج التعليمية المرتفعة لا تُفسَّر بوصفها ضمانًا لجودة production على بيانات واقعية غير مرئية.

**Result:** COMPLETE

---

## Final project decision

**Implementation:** ✅ COMPLETE  
**Evaluation:** ✅ COMPLETE  
**T9 Manual Review:** ✅ COMPLETE  
**T10 Benchmark:** ✅ COMPLETE  
**FastAPI Serving:** ✅ COMPLETE  
**Measured Extension:** ✅ COMPLETE  
**Documentation:** ✅ COMPLETE  
**Validation:** ✅ COMPLETE  
**Public Access:** ✅ COMPLETE  
**Presentation:** ✅ COMPLETE  
**Release:** ✅ COMPLETE  
**Submission:** ✅ COMPLETE

**BAYAN CAPSTONE — FINAL SUBMISSION COMPLETE**

**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
