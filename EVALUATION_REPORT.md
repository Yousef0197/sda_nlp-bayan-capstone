# EVALUATION_REPORT — Bayan

## Project

**Bayan — Bilingual Applied NLP Capstone**

**Status:** ✅ COMPLETE

**Training context:** Bayan — #SDAIA

---

## Evaluation overview

يوثّق هذا التقرير نتائج التقييم النهائي للمهام الرئيسية في المشروع بعد تشغيل الـNotebook المرجعي:

`notebooks/bayan_capstone.ipynb`

جميع النتائج الواردة هنا ناتجة من تشغيل المشروع فعليًا.

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

تم تحليل `100` حالة ضمن جدول تحليل الأخطاء، مع تصنيف الحالات وتحديد ثلاثة إصلاحات مرتبة حسب الأولوية.

**Status:** ✅ PASS

---

## T10 — Performance Benchmark

### Result

- Concurrency: `16`
- HTTP p99: `32.907 ms`

**Threshold:** ≤ `40 ms`

**Status:** ✅ PASS

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

`KEEP`

**Status:** ✅ PASS

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
| T9 Error analysis | `100` cases | ✅ PASS |
| T10 HTTP p99 | `32.907 ms` | ✅ PASS |
| T11 FastAPI | Complete | ✅ PASS |
| T12 Extension | `+0.88` | ✅ PASS |

---

## Final status

**Evaluation:** ✅ COMPLETE  
**All documented threshold checks:** ✅ PASS  

`BAYAN_DAY1_DAY4_OFFICIAL_THRESHOLDS=PASS`

**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
