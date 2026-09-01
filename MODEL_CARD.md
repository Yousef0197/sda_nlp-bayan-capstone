# MODEL_CARD — Bayan

## Project

**Bayan — Bilingual Applied NLP Capstone**

**Status:** ✅ COMPLETE

**Training context:** Bayan — #SDAIA

---

## System overview

Bayan هو مسار تطبيقي ثنائي اللغة لمعالجة اللغة الطبيعية بالعربية والإنجليزية، ويجمع عدة مهام داخل Pipeline موحّد.

يشمل:

- Text preprocessing
- PII masking
- Topic classification
- Sentiment classification
- Named Entity Recognition
- Extractive Question Answering
- Semantic Search
- Behavioural Evaluation
- Error Analysis
- FastAPI serving
- Performance benchmarking
- Measured extension

**System status:** ✅ COMPLETE

---

## Canonical notebook

الدفتر المرجعي للمشروع:

`notebooks/bayan_capstone.ipynb`

ويجمع مختبرات Day 1–Day 4 في Notebook واحد قابل لإعادة التشغيل.

**Canonical notebook status:** ✅ COMPLETE

---

## Transformer model

يستخدم المشروع نموذجًا متعدد اللغات ضمن مسارات Transformer:

`distilbert/distilbert-base-multilingual-cased`

ويُستخدم ضمن سياق تعليمي تطبيقي ثنائي اللغة.

**Transformer path status:** ✅ COMPLETE

---

## Topic & Sentiment Classification

يعتمد المشروع على:

- TF-IDF baseline
- Transformer-based classification
- Macro-F1 comparison

### Measured results

- Topic Macro-F1 delta: `+0.858`
- Sentiment Macro-F1 delta: `+0.663`

**Result:** ✅ PASS

---

## Named Entity Recognition

يدعم مسار NER:

- `word_ids()` alignment
- subword handling
- `-100` masking
- entity-level evaluation

### Measured result

- Entity-level F1: `1.000`

**Result:** ✅ PASS

---

## Extractive Question Answering

يدعم مسار QA:

- start position
- end position
- valid span constraints
- no-answer handling

### Measured result

- No-answer success: `20/20`

**Result:** ✅ PASS

---

## Unified Arabic profile

تم اعتماد ملف معالجة عربي موحّد بين:

- Train
- Evaluation
- Serving

كما تم استخدام Arabic canaries للتحقق من ثبات المسار.

**Result:** ✅ PASS

---

## Semantic Search

يعتمد البحث الدلالي على:

- bilingual text preprocessing
- vector representation
- FAISS retrieval
- bilingual concept canonicalization
- reranking

### Measured results

- Recall@10: `1.000`
- MRR@10: `1.000`

**Result:** ✅ PASS

---

## Behavioural Evaluation

يشمل التقييم السلوكي:

- Invariance
- Minimum Functionality Tests
- Arabic / English slices
- bootstrap confidence intervals

### Measured results

- Invariance: `1.000`
- MFT: `1.000`

**Result:** ✅ PASS

---

## Error Analysis

تم إنشاء جدول من `100` حالة للمراجعة ضمن مسار تحليل الأخطاء.

تمت مراجعة `20` خطأ فعليًا يدويًا وتصنيفها.

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

**T9 Result:** ✅ PASS

---

## Serving

يستخدم المشروع FastAPI لتقديم وظائف النظام.

### Endpoints

`GET /health`

`POST /v1/classify`

وتغطي الاختبارات:

- Arabic input
- English input
- invalid input
- PII masking
- startup/API canaries

**Result:** ✅ PASS

---

## Performance

### Benchmark ladder

يشمل مسار القياس:

- direct classification path
- cached classification path
- prediction parity
- FastAPI / ASGI smoke measurement
- real HTTP local CPU benchmark

### Prediction parity

تم التحقق من تطابق المخرجات بين المسار المباشر والمسار المحسن:

`Prediction parity = 1.0`

`DAY4_BENCHMARK_PARITY=PASS`

### Final real-HTTP local CPU benchmark

بيئة القياس:

- Platform: Windows 11
- CPU count: `8`
- Concurrency: `16`
- Warm-up requests: `32`
- Measured requests: `128`

### Measured results

- HTTP p50: `19.172 ms`
- HTTP p95: `24.805 ms`
- HTTP p99: `27.903 ms`
- HTTP mean: `18.340 ms`

### Target

`HTTP p99 <= 40 ms` at concurrency `16`

### Benchmark result

`T10_LOCAL_CPU_HTTP_TARGET_MET=True`

`T10_LOCAL_CPU_HTTP_BENCHMARK=PASS`

### Evidence

`reports/t10_local_cpu_http_benchmark.json`

### Environment boundary

القياس النهائي تم على CPU محلي بنظام Windows.

لا يُنسب هذا الجهاز إلى academy lab CPU محدد إلا إذا كانت البيئة الرسمية مطابقة ومعلنة.

هذه الملاحظة توثّق بيئة القياس ولا تغيّر حالة اكتمال المشروع.

**T10 Result:** ✅ PASS

---

## Measured extension

تمت إضافة:

**Bilingual concept canonicalization + reranking**

### Measured result

- Top-1 delta: `+0.88`

### Decision

`KEEP`

**Result:** ✅ PASS

---

## Intended use

المشروع مخصص للتطبيق التعليمي والعملي على مهام معالجة اللغة الطبيعية ثنائية اللغة، مع التركيز على:

- قابلية القياس.
- إعادة التشغيل.
- المقارنة بين baseline والمسارات المحسنة.
- التقييم السلوكي.
- التوثيق القابل للمراجعة.
- خدمة النموذج عبر API.

**Intended-use status:** ✅ DOCUMENTED

---

## Data and privacy

يعتمد المشروع على بيانات تعليمية اصطناعية، ويطبق:

- PII masking
- safe preprocessing
- train / validation / test separation
- bilingual evaluation

ولا يعتمد على بيانات شخصية حقيقية داخل المستودع.

كما أن أمثلة الهاتف والبريد المستخدمة في الاختبارات أمثلة اصطناعية.

**Privacy status:** ✅ COMPLETE

---

## Evaluation interpretation

تُفسَّر النتائج ضمن الحدود التالية:

- `MEASURED_SMOKE=True`
- `TEST_USED_FOR_SELECTION=False`
- `ACADEMY_FROZEN_EVAL_REPLACED=False`

نتائج الـcanonical notebook ناتجة من تشغيل فعلي للحزم التعليمية الاصطناعية.

النتائج المرتفعة على هذه الحزم لا تعني ضمان جودة production مماثلة على بيانات واقعية غير مرئية.

نتيجة T10 النهائية `27.903 ms` مصدرها قياس real HTTP محلي منفصل وموثق داخل `reports/`.

**Evaluation documentation status:** ✅ COMPLETE

---

## Validation and release

تم تشغيل Submission Validator من Fresh Clone للوسم النهائي، وظهرت النتيجة:

`BAYAN_SUBMISSION_VALIDATOR=PASS`

تم التحقق من:

- Required project structure
- Nine valid notebooks and Core markers
- `PROJECT_SUMMARY.json`
- `SUBMISSION.yml`
- No forbidden or oversized tracked artefacts
- Final tag `submission-v1.0`

كما تم التحقق من فتح المستودع العام ورابط Colab من نافذة خاصة.

**Validation:** ✅ COMPLETE  
**Public access:** ✅ COMPLETE  
**Release:** ✅ COMPLETE

---

## Presentation

تم تجهيز العرض النهائي للمشروع واستكمال متطلب العرض.

**Presentation:** ✅ COMPLETE

---

## Final status

**Classification:** ✅ COMPLETE  
**Sentiment:** ✅ COMPLETE  
**NER:** ✅ COMPLETE  
**QA:** ✅ COMPLETE  
**Arabic Profile:** ✅ COMPLETE  
**Semantic Search:** ✅ COMPLETE  
**Behavioural Evaluation:** ✅ COMPLETE  
**T9 Manual Error Review:** ✅ COMPLETE  
**Serving:** ✅ COMPLETE  
**T10 Benchmark:** ✅ COMPLETE  
**Measured Extension:** ✅ COMPLETE  
**Privacy Documentation:** ✅ COMPLETE  
**Validation:** ✅ COMPLETE  
**Public Access:** ✅ COMPLETE  
**Presentation:** ✅ COMPLETE  
**Release:** ✅ COMPLETE  
**Submission:** ✅ COMPLETE

**MODEL CARD — COMPLETE**

**BAYAN CAPSTONE — FINAL SUBMISSION COMPLETE**

**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
