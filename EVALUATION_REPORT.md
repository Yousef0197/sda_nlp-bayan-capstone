# EVALUATION_REPORT — Bayan

## Project

**Bayan — Bilingual Applied NLP Capstone**

**Status:** ✅ COMPLETE

**Training context:** Bayan — #SDAIA

---

## Evaluation overview

يوثّق هذا التقرير نتائج التقييم النهائي للمهام الرئيسية في المشروع.

الدفتر المرجعي:

`notebooks/bayan_capstone.ipynb`

تم الحفاظ على نتائج التشغيل الكامل للـNotebook، مع إضافة أدلة T9 وT10 النهائية الموثقة داخل المستودع.

أدلة T9:

- `reports/T9_MANUAL_REVIEW.md`
- `reports/t9_manual_error_review.csv`

دليل T10:

- `reports/t10_local_cpu_http_benchmark.json`

جميع البيانات المستخدمة في المشروع تعليمية اصطناعية، ولا تُقدَّم النتائج بوصفها بديلًا عن أي Frozen Evaluation رسمي مستقل قد تعلنه الأكاديمية.

---

## T3 — Topic Classification

### Result

- Macro-F1 improvement over baseline: `+0.858`

**Threshold:** ≥ `+0.08`

**Status:** ✅ PASS

---

## T3 — Sentiment Classification

### Result

- Macro-F1 improvement over baseline: `+0.663`

**Threshold:** ≥ `+0.08`

**Status:** ✅ PASS

---

## T4 — Named Entity Recognition

### Result

- Entity-level F1: `1.000`

**Threshold:** ≥ `0.80`

**Status:** ✅ PASS

---

## T5 — Extractive Question Answering

### Result

- No-answer correct cases: `20/20`

**Threshold:** ≥ `17/20`

**Status:** ✅ PASS

---

## T6 — Unified Arabic Profile

تم استخدام ملف معالجة عربي موحّد في:

- Train
- Evaluation
- Serving

كما تم اختبار Arabic canaries.

**Status:** ✅ PASS

---

## T7 — Semantic Search

### Results

- Recall@10: `1.000`
- MRR@10: `1.000`

**Thresholds:**

- Recall@10 ≥ `0.80`
- MRR@10 ≥ `0.70`

**Status:** ✅ PASS

---

## T8 — Behavioural Evaluation

### Results

- Invariance: `1.000`
- MFT: `1.000`

**Thresholds:**

- Invariance ≥ `0.95`
- MFT ≥ `0.90`

**Status:** ✅ PASS

---

## T9 — Error Analysis

تم إنشاء جدول من `100` حالة للمراجعة ضمن مسار تحليل الأخطاء.

تمت مراجعة `20` خطأ فعليًا يدويًا وتصنيفها.

نتيجة المراجعة اليدوية:

- candidate_ordering: `12`
- cross_language_lexical_gap: `5`
- normalization_drift: `3`

كما تم تحديد ثلاثة إصلاحات مرتبة حسب الأولوية:

1. bilingual concept canonicalization before embedding.
2. FAISS candidate retrieval + reranking.
3. unified train/eval/serve Arabic profile.

الأدلة:

- `reports/T9_MANUAL_REVIEW.md`
- `reports/t9_manual_error_review.csv`

**Status:** ✅ PASS

---

## T10 — Performance Benchmark

### Final real-HTTP local CPU result

- Environment: Windows local CPU
- Logical CPUs: `8`
- Concurrency: `16`
- Warm-up requests: `32`
- Measured requests: `128`
- HTTP p50: `19.172 ms`
- HTTP p95: `24.805 ms`
- HTTP p99: `27.903 ms`
- HTTP mean: `18.340 ms`

**Threshold:** HTTP p99 ≤ `40 ms` at concurrency `16`

**Measured:** `27.903 ms`

**Evidence:**

`reports/t10_local_cpu_http_benchmark.json`

**Status:** ✅ PASS

### Benchmark boundary

هذا القياس هو real HTTP benchmark منفذ على CPU محلي بنظام Windows.

القياس السابق داخل Colab عبر ASGI كان smoke measurement فقط ولا يُستخدم بوصفه نتيجة T10 النهائية.

إذا كانت الأكاديمية تشترط جهاز lab CPU محددًا بالاسم أو المواصفات، فلا يُدَّعى أن الجهاز المحلي هو ذلك الجهاز بعينه.

---

## T11 — FastAPI

تم اختبار:

- `GET /health`
- `POST /v1/classify`
- Arabic input
- English input
- Invalid input
- Startup/API canaries
- PII masking

**Status:** ✅ PASS

---

## T12 — Measured Extension

### Extension

Bilingual concept canonicalization + reranking

### Result

- Top-1 delta: `+0.88`

### Decision

`ADOPT`

**Status:** ✅ PASS

**Implementation:** ✅ COMPLETE

تم اعتماد الامتداد بعد القياس لأن المقارنة قبل/بعد أظهرت تحسنًا موجبًا في Top-1 بمقدار `+0.88`.

---

## Final evaluation summary

| Requirement | Result | Status |
|---|---:|---|
| T3 Topic | `+0.858` | ✅ PASS |
| T3 Sentiment | `+0.663` | ✅ PASS |
| T4 NER | `1.000` | ✅ PASS |
| T5 QA | `20/20` | ✅ PASS |
| T6 Arabic profile | Complete | ✅ PASS |
| T7 Recall@10 | `1.000` | ✅ PASS |
| T7 MRR@10 | `1.000` | ✅ PASS |
| T8 Invariance | `1.000` | ✅ PASS |
| T8 MFT | `1.000` | ✅ PASS |
| T9 Error analysis | `100` generated cases; `20` manually reviewed errors | ✅ PASS |
| T10 HTTP p99 | `27.903 ms` real HTTP, local CPU, concurrency `16` | ✅ PASS |
| T11 FastAPI | Complete | ✅ PASS |
| T12 Extension | `+0.88` | ✅ PASS |

---

## Evidence interpretation

- `MEASURED_SMOKE=True`
- `TEST_USED_FOR_SELECTION=False`
- `ACADEMY_FROZEN_EVAL_REPLACED=False`

الأرقام المرتفعة في الحزم التعليمية الاصطناعية لا تعني جودة إنتاجية مماثلة على بيانات واقعية غير مرئية.

---

## Final status

**Evaluation:** ✅ COMPLETE  
**Documented threshold checks:** ✅ PASS  
**T9 manual-review evidence:** ✅ RECORDED  
**T10 real-HTTP local CPU evidence:** ✅ RECORDED  
**Submission validator:** `BAYAN_SUBMISSION_VALIDATOR=PASS`  
**Final tag:** `submission-v1.0`

`BAYAN_DAY1_DAY4_OFFICIAL_THRESHOLDS=PASS`

**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
