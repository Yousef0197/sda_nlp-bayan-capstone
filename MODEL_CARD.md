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
- FastAPI serving

---

## Transformer model

يستخدم المشروع نموذجًا متعدد اللغات ضمن مسارات Transformer:

`distilbert/distilbert-base-multilingual-cased`

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

## Semantic Search

يعتمد البحث الدلالي على:

- bilingual text preprocessing
- vector representation
- FAISS retrieval
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

### Measured results

- Invariance: `1.000`
- MFT: `1.000`

**Result:** ✅ PASS

---

## Error Analysis

تم تحليل `100` حالة ضمن مسار تحليل الأخطاء، مع تحديد أنماط الأخطاء وإصلاحات مرتبة حسب الأولوية.

**Result:** ✅ PASS

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

### Benchmark

- Concurrency: `16`
- HTTP p99: `32.907 ms`

**Result:** ✅ PASS

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

المشروع مخصص للتطبيق التعليمي والعملي على مهام معالجة اللغة الطبيعية ثنائية اللغة، مع التركيز على قابلية القياس وإعادة التشغيل.

---

## Data and privacy

يعتمد المشروع على بيانات تعليمية اصطناعية، ويطبق:

- PII masking
- safe preprocessing
- train / validation / test separation
- bilingual evaluation

ولا يعتمد على بيانات شخصية حقيقية داخل المستودع.

---

## Final status

**Classification:** ✅ COMPLETE  
**NER:** ✅ COMPLETE  
**QA:** ✅ COMPLETE  
**Semantic Search:** ✅ COMPLETE  
**Evaluation:** ✅ COMPLETE  
**Serving:** ✅ COMPLETE  
**Benchmark:** ✅ COMPLETE  
**Measured Extension:** ✅ COMPLETE  

**MODEL CARD — COMPLETE**

**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
