# DATA_CARD — Bayan

## Project

**Bayan — Bilingual Applied NLP Capstone**

**Status:** ✅ COMPLETE

**Training context:** Bayan — #SDAIA

---

## Data purpose

تُستخدم البيانات في المشروع لتطوير واختبار مهام معالجة اللغة الطبيعية ثنائية اللغة بالعربية والإنجليزية.

تشمل المهام:

- Text preprocessing
- PII masking
- Topic classification
- Sentiment classification
- Named Entity Recognition
- Extractive Question Answering
- Semantic Search
- Behavioural Evaluation

---

## Data type

البيانات المستخدمة في المشروع هي:

**Synthetic Educational Data**

وهي بيانات تعليمية مخصصة لتجارب المشروع وقياس وظائفه.

---

## Languages

- Arabic
- English

---

## Privacy

تم تصميم البيانات بحيث لا تعتمد على بيانات شخصية حقيقية.

تشمل اختبارات الخصوصية:

- Email masking
- Phone-number masking
- Text normalization
- Safe preprocessing

ولا يحتوي المستودع على:

- API keys
- `.env`
- بيانات حساسة
- model checkpoints كبيرة
- model weights كبيرة

---

## Dataset usage

تُستخدم البيانات ضمن مراحل منفصلة حسب المهمة:

- Training
- Validation
- Testing
- Behavioural tests
- Retrieval evaluation
- API canaries

ويستخدم المشروع تقسيمات واضحة عند الحاجة بين:

`Train / Validation / Test`

---

## Evaluation coverage

تم استخدام البيانات لقياس:

- Macro-F1
- Entity-level F1
- QA no-answer success
- Recall@10
- MRR@10
- Invariance
- MFT
- Error analysis
- API behaviour
- Performance benchmark

---

## Final measured results

- Topic Macro-F1 delta: `+0.858`
- Sentiment Macro-F1 delta: `+0.663`
- NER entity-level F1: `1.000`
- QA no-answer: `20/20`
- Recall@10: `1.000`
- MRR@10: `1.000`
- Invariance: `1.000`
- MFT: `1.000`

---

## Responsible data handling

يعتمد المشروع على بيانات تعليمية مخصصة للتطوير والتقييم، مع تطبيق إخفاء البيانات الشخصية واختبارات سلامة المعالجة النصية.

---

## Final status

**Data preparation:** ✅ COMPLETE  
**Privacy checks:** ✅ COMPLETE  
**Task evaluation data:** ✅ COMPLETE  
**Retrieval evaluation data:** ✅ COMPLETE  
**Behavioural evaluation data:** ✅ COMPLETE  

**DATA CARD — COMPLETE**

**#SDAIA #Bayan #NLP #ArabicNLP**
