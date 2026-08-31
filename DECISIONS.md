# DECISIONS — Bayan

يوثّق هذا الملف القرارات الهندسية النهائية للمشروع بعد اكتمال جميع مراحل التنفيذ والتقييم والتسليم.

## D-001 — Bilingual preprocessing

**Status:** ✅ COMPLETE

**Decision:** اعتماد مسار موحّد للمعالجة في التدريب والتقييم والخدمة، يشمل Unicode normalization، معالجة العربية، ضبط المسافات، وPII masking.

**Reason:** تقليل الاختلاف بين مراحل النظام وتحسين ثبات النتائج.

---

## D-002 — Canonical notebook

**Status:** ✅ COMPLETE

**Decision:** اعتماد الملف التالي كمرجع التشغيل النهائي للمشروع:

`notebooks/bayan_capstone.ipynb`

ويجمع مختبرات Day 1–Day 4 في Notebook واحد قابل لإعادة التشغيل.

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

**Result:** PASS

---

## D-007 — Semantic Search

**Status:** ✅ COMPLETE

**Decision:** استخدام FAISS للاسترجاع مع bilingual concept canonicalization وreranking.

**Measured results:**
- Recall@10: `1.000`
- MRR@10: `1.000`

**Result:** PASS

---

## D-008 — Behavioural Evaluation

**Status:** ✅ COMPLETE

**Decision:** إضافة اختبارات Invariance وMinimum Functionality Tests ضمن التقييم النهائي.

**Measured results:**
- Invariance: `1.000`
- MFT: `1.000`

**Result:** PASS

---

## D-009 — Error Analysis

**Status:** ✅ COMPLETE

**Decision:** تحليل `100` حالة خطأ/مراجعة وتصنيفها، ثم تحديد ثلاثة إصلاحات مرتبة حسب الأولوية.

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

**Target:** HTTP p99 ≤ `40 ms` عند concurrency = `16`.

**Measured result:**
- HTTP p99: `32.907 ms`

**Result:** PASS

---

## D-012 — Measured Extension

**Status:** ✅ COMPLETE

**Extension:** bilingual concept canonicalization + reranking.

**Measured result:**
- Top-1 delta: `+0.88`

**Decision:** KEEP

**Result:** PASS

---

## D-013 — Final Validation

**Status:** ✅ COMPLETE

تم تنفيذ التحقق النهائي للمشروع بعد اكتمال الملفات المطلوبة والتوثيق والـNotebook المرجعي.

**Result:** PASS

---

## D-014 — Presentation

**Status:** ✅ COMPLETE

تم تجهيز العرض النهائي للمشروع.

---

## D-015 — Public Repository Verification

**Status:** ✅ COMPLETE

تم التحقق من إمكانية الوصول إلى المستودع العام.

---

## D-016 — Final Release

**Status:** ✅ COMPLETE

تم اعتماد وسم الإصدار النهائي:

`submission-v1.0`

---

## Final project decision

**Implementation:** ✅ COMPLETE  
**Evaluation:** ✅ COMPLETE  
**Documentation:** ✅ COMPLETE  
**Validation:** ✅ COMPLETE  
**Submission:** ✅ COMPLETE  

**BAYAN CAPSTONE — FINAL SUBMISSION COMPLETE**

**Training context:** Bayan — #SDAIA
