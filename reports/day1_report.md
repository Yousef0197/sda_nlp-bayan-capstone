# Day 1 Report — Text Processing, Tokenisation, Attention & Transformers

**Project:** Bayan — Bilingual Applied NLP Capstone
**Student:** Yousef Al-Mutiri
**Date:** 2026-08-30
**Gate:** A — Ingest
**Status:** ✅ PASSED

---

## 1. Purpose | الهدف

يُوثّق هذا التقرير أدلة اليوم الأول من مشروع Bayan.

غطّى اليوم الأول مختبرين:

1. معالجة النصوص والترميز.
2. الانتباه والمحولات.

الهدف هو إثبات أن مسار المشروع يستطيع استقبال نصوص عربية وإنجليزية، حمايتها ومعالجتها بصورة محافظة، تحويلها إلى رموز وتمثيلات عددية، ثم توضيح كيفية بناء تمثيلات سياقية باستخدام آلية الانتباه والمحولات.

جميع الأمثلة المستخدمة في تجارب اليوم الأول اصطناعية وتعليمية.

لا تُستخدم بيانات مستفيدين حقيقية أو بيانات حكومية حساسة.

---

# Part A — Text Processing & Tokenisation

## 2. Two-copy preprocessing | المعالجة بنسختين

اعتمد المشروع عقدًا واضحًا للمعالجة:

- الاحتفاظ بالنص الخام كما دخل النظام.
- إنشاء نسخة منفصلة مهيأة للنموذج.

السبب هو منع ضياع النص الأصلي أثناء عمليات التنظيف والتطبيع.

مثال:

`مرحبــاً بكم`

تصبح في نسخة النموذج:

`مرحباً بكم`

مع الاحتفاظ بالنص الخام بصورة مستقلة.

---

## 3. Conservative Arabic preprocessing | المعالجة العربية المحافظة

يشمل الملف الافتراضي:

- Unicode normalization باستخدام `NFC`.
- إزالة الكشيدة.
- توحيد المسافات.
- إخفاء البريد الإلكتروني.
- إخفاء أرقام الهاتف.

ولا تُطبق افتراضيًا:

- إزالة التشكيل.
- توحيد صور الألف.

السبب أن التطبيع المفرط قد يحذف معلومات لغوية قد تحتاج إليها مهام لاحقة.

---

## 4. Privacy masking | إخفاء البيانات

اختُبرت أمثلة اصطناعية تشمل:

- بريدًا إلكترونيًا تعليميًا.
- رقم هاتف تجريبيًا.

تحولت القيم الحساسة إلى رموز مثل:

`<EMAIL>`

و:

`<PHONE>`

من دون استخدام بيانات شخصية حقيقية.

---

## 5. Unicode evidence

تم فحص نقاط Unicode بدل الاعتماد على الشكل المرئي للحرف.

مثال:

`أ`

يمثل نقطة Unicode:

`U+0623`

ويختلف مفهوم Unicode code point عن:

- UTF-8 bytes.
- Token ID.
- Model embedding.

Marker:

`Unicode inspection=PASS`

---

## 6. Sentence segmentation

استُخدم spaCy لتقسيم النصوص إلى جمل.

نجح المسار الأساسي، مع توثيق قيد معروف يتعلق ببعض الاختصارات مثل:

`د.`

إذ قد تحتاج الاختصارات العربية إلى قواعد إضافية أو معالجة مخصصة في البيانات الفعلية.

---

# Tokenisation evidence

## 7. Token fertility

قورِن:

- `google-bert/bert-base-multilingual-cased`
- `aubmindlab/bert-base-arabertv02`

على عينة ثابتة من:

- أربعة نصوص عربية.
- أربعة نصوص إنجليزية.

### Measured results

| Tokenizer | Arabic fertility | English fertility |
|---|---:|---:|
| mBERT | `2.595` | `1.299` |
| AraBERT | `1.182` | `3.714` |

### Interpretation

أظهر AraBERT تجزئة أكثر اقتصادًا للنص العربي في العينة الحالية.

في المقابل، أظهر تجزئة مرتفعة للنص الإنجليزي.

أظهر mBERT توازنًا أفضل بين اللغتين عندما يكون المطلوب استخدام مرمّز واحد لمسار ثنائي اللغة.

لا تعني خصوبة أقل بالضرورة جودة أعلى في المهمة النهائية.

---

## 8. Truncation measurement

قيس معدل القطع عند:

- `max_length = 32`
- `max_length = 64`

وكانت النتائج:

| Tokenizer | Language | max_length=32 | max_length=64 |
|---|---|---:|---:|
| mBERT | Arabic | `0.0%` | `0.0%` |
| mBERT | English | `0.0%` | `0.0%` |
| mBERT | Combined | `0.0%` | `0.0%` |
| AraBERT | Arabic | `0.0%` | `0.0%` |
| AraBERT | English | `0.0%` | `0.0%` |
| AraBERT | Combined | `0.0%` | `0.0%` |

لم تُظهر العينة الحالية قطعًا عند الطولين.

هذا لا يثبت أن `32` سيكون كافيًا لمجموعة المشروع النهائية.

سيُعاد القياس بعد تجميد البيانات.

---

## 9. Approximate tokenisation time

في التشغيل النظيف المحفوظ:

| Tokenizer | Mean tokenisation time |
|---|---:|
| mBERT | `0.1421 ms` |
| AraBERT | `0.1631 ms` |

هذه أرقام تقريبية من Notebook على عينة صغيرة.

لا تمثل Benchmark نهائيًا للخدمة.

---

## 10. Arabic clitic probe

اختُبرت:

`الخدمة`

فكانت تجزئة mBERT:

`['ال', '##خدمة']`

بعدد:

`2`

قطع.

واختُبرت:

`وبالخدمة`

فكانت:

`['وب', '##ال', '##خدمة']`

بعدد:

`3`

قطع.

الاستنتاج:

اتصال اللواصق العربية يمكن أن يغير بنية التجزئة، ولذلك لا ينبغي افتراض أن الكلمة العربية تمثل دائمًا بعدد ثابت من الرموز.

Marker:

`DISTINCTION_CLITIC_TEST=PASS`

كما يوجد اختبار آلي للحالة في:

`tests/test_day1_tokenization.py`

---

## 11. Three-seed embedding experiment

استُخدمت البذور:

- `7`
- `42`
- `2026`

وبقي شكل مصفوفة التضمينات الناتجة:

`(2, 5, 8)`

في جميع التشغيلات.

تغيرت القيم العددية مع تغير البذرة، بينما بقيت:

- أبعاد البيانات.
- Token IDs.
- بنية المدخلات.

ثابتة.

Marker:

`DISTINCTION_THREE_SEEDS=PASS`

---

## 12. Tokenizer decision

القرار المبدئي:

`google-bert/bert-base-multilingual-cased`

أي:

`mBERT`

مع:

`max_length = 64`

سبب الاختيار هو التوازن الحالي بين العربية والإنجليزية عند الحاجة إلى مسار موحد.

القرار ليس نهائيًا وغير قابل للمراجعة.

سيُعاد تقييمه باستخدام:

- مجموعة البيانات المجمدة.
- جودة المهام الفعلية.
- معدل القطع.
- الكلفة الحسابية.

التوثيق التفصيلي موجود في:

`DECISIONS.md`

---

# Part B — Attention & Transformers

## 13. Scaled Dot-Product Attention

استُخدمت المعادلة:

`Attention(Q,K,V) = softmax((QK^T / sqrt(d_k)) + M)V`

حيث:

- `Q` = Query.
- `K` = Key.
- `V` = Value.
- `M` = Mask عند الحاجة.

القسمة على:

`sqrt(d_k)`

تساعد على الحد من تضخم قيم الضرب النقطي عندما يكبر البعد، مما يقلل دخول Softmax في مناطق شديدة الحدة.

---

## 14. Shapes table

### General attention shapes

| Tensor | Shape | المعنى |
|---|---|---|
| Q | `(T_q, d_k)` | استعلام لكل موضع |
| K | `(T_k, d_k)` | مفتاح لكل موضع |
| V | `(T_k, d_v)` | قيمة لكل موضع |
| Scores | `(T_q, T_k)` | درجة كل Query مع كل Key |
| Weights | `(T_q, T_k)` | احتمالات الانتباه بعد Softmax |
| Output | `(T_q, d_v)` | التمثيل السياقي الناتج |

### Toy attention example

في المثال المنفذ:

| Tensor | Shape |
|---|---:|
| Q | `(2, 2)` |
| K | `(3, 2)` |
| V | `(3, 2)` |
| Scores | `(2, 3)` |
| Weights | `(2, 3)` |
| Output | `(2, 2)` |

وكان:

`row sums = [1.0, 1.0]`

أي أن مجموع أوزان الانتباه لكل Query يساوي واحدًا.

Marker:

`Scaled attention=PASS`

---

## 15. Mask semantics | دلالة القناع

اعتمد Notebook 02 عقدًا صريحًا:

`True`

يعني:

**يسمح للمفتاح بالمشاركة في الانتباه.**

أما:

`False`

فيعني:

**الموضع محجوب.**

قبل تطبيق Softmax، تعطى المواضع المحجوبة قيمة سالبة غير منتهية عمليًا:

`-inf`

فتصبح احتمالاتها بعد Softmax:

`0`

### Important limitation

لا توجد دلالة موحدة للقناع بين جميع المكتبات والواجهات.

لذلك يجب مراجعة عقد الدالة المستخدمة وعدم افتراض أن:

`True`

يعني دائمًا الشيء نفسه في كل API.

---

## 16. Causal mask versus padding mask

القناع السببي يمنع الموضع الحالي من رؤية الرموز المستقبلية.

يستخدم عادة في نماذج توليدية ذات اتجاه سببي.

أما Encoder مثل BERT فيستخدم في صورته المعتادة Padding Mask لحجب الرموز المضافة للحشو، ولا يحتاج Causal Mask بالطريقة نفسها في مهام الفهم ثنائية الاتجاه.

---

## 17. NumPy versus PyTorch mask semantics

تمت مقارنة تنفيذ NumPy مع تنفيذ PyTorch باستخدام القناع نفسه.

كان أقصى فرق عددي مقاس:

`4.441e-16`

وهو ضمن حدود دقة floating-point.

كما تحققت الشروط التالية:

- المواضع المحجوبة أخذت احتمالًا صفريًا.
- الصفوف حافظت على مجموع احتمالات يساوي واحدًا.
- ناتج NumPy وناتج PyTorch تطابقا عمليًا.

Marker:

`DISTINCTION_MASK_SEMANTICS=PASS`

---

# Multi-Head Attention

## 18. Head splitting and combining

في التجربة التعليمية كان شكل الإدخال:

`(2, 5, 12)`

حيث:

- Batch = `2`
- Sequence length = `5`
- `d_model = 12`

استخدم:

`num_heads = 3`

وبالتالي:

`head_dim = 4`

بعد تقسيم الرؤوس يصبح الشكل:

`(2, 3, 5, 4)`

أي:

`(batch, heads, sequence, head_dim)`

وبعد دمج الرؤوس يعود الشكل إلى:

`(2, 5, 12)`

تم التحقق من أن الدمج يعيد القيم الأصلية.

Marker:

`heads_round_trip=PASS`

---

## 19. Encoder Layer

اختُبر Encoder Layer على CPU باستخدام:

- `d_model = 12`
- `nhead = 3`
- `dim_feedforward = 24`
- `dropout = 0.0`

البنية المفاهيمية:

1. Multi-Head Self-Attention.
2. Residual Connection.
3. Layer Normalization.
4. Feed-Forward Network.
5. Residual Connection.
6. Layer Normalization.

الغرض من الاختبار هو إثبات سلامة تدفق الأبعاد والتنفيذ، وليس تدريب نموذج نهائي.

---

# Actual Transformer Forward Pass

## 20. Actual model evidence

في التشغيل الفعلي للنموذج ظهر:

`Hidden-state shape = (2, 10, 768)`

كما كان شكل مصفوفة الانتباه:

`(2, 12, 10, 10)`

بترتيب:

`[batch, heads, query, key]`

وهذا يعني:

- Batch size = `2`
- Attention heads = `12`
- Query positions = `10`
- Key positions = `10`

تم تنفيذ مدخل عربي ومدخل إنجليزي ضمن التشغيل الفعلي.

Marker:

`actual_forward=PASS`

---

## 21. Attention interpretation limitation

مصفوفة الانتباه توضح توزيع الأوزان الذي استخدمه رأس معين أثناء حساب التمثيل.

لكن لا يجوز الاستنتاج مباشرة أن:

**ارتفاع وزن الانتباه يعني أن هذا الرمز هو السبب الذي جعل النموذج يتخذ قرارًا معينًا.**

لذلك تعامل مصفوفة الانتباه بوصفها أداة فحص للنموذج، وليست إثباتًا سببيًا كاملًا لتفسير قراراته.

---

# Day 1 Validation

## 22. Core markers

Notebook 01:

`DAY1_NOTEBOOK1_CORE=PASS`

Notebook 02:

`DAY1_NOTEBOOK2_CORE=PASS`

Distinction evidence:

- `DISTINCTION_CLITIC_TEST=PASS`
- `DISTINCTION_THREE_SEEDS=PASS`
- `DISTINCTION_TOKENIZER_COMPARISON=PASS`
- `BILINGUAL_TRUNCATION_MEASUREMENT=PASS`
- `DAY1_DISTINCTION_REPRODUCIBLE=PASS`
- `DISTINCTION_MASK_SEMANTICS=PASS`

---

## 23. Automated tests

تم تشغيل اختبارات Day 1 معًا:

`$env:PYTHONPATH="src"; python -m pytest -q tests/test_day1_preprocessing.py tests/test_day1_tokenization.py tests/test_day1_attention.py`

النتيجة:

`.......... [100%]`

`10 passed in 0.16s`

---

# Evidence

## 24. Main evidence paths

- `notebooks/01_text_processing_tokenization.ipynb`
- `notebooks/02_attention_transformers.ipynb`
- `src/bayan/preprocessing.py`
- `src/bayan/tokenization.py`
- `tests/test_day1_preprocessing.py`
- `tests/test_day1_tokenization.py`
- `tests/test_day1_attention.py`
- `DECISIONS.md`
- `PROGRESS.md`
- `README.md`

---

## 25. Evidence commits

من أهم التغييرات التي توثق Day 1:

- `46bda67` — reproducible Notebook 01 Distinction evidence.
- `c12b501` — clean-run verification for Notebook 01.
- `dfc4083` — tokenizer decision evidence.
- `3b1c903` — Arabic clitic automated test.
- `de53b08` — Notebook 01 metadata cleanup.
- `fb647d6` — decision evidence aligned with the clean run.
- `1701704` — progress evidence aligned with the clean run.
- `46b0b6b` — professional README with measured Gate A evidence.
- `24db4e4` — Notebook 02 attention and transformer evidence.

---

# Limitations

## 26. Known Day 1 limitations

1. بيانات Tokenizer الحالية صغيرة واصطناعية.
2. لا تثبت Token Fertility وحدها جودة المهمة النهائية.
3. لم يظهر قطع في العينة الحالية حتى عند `max_length=32`، لكن ذلك لا يضمن عدم ظهوره في البيانات النهائية.
4. قياسات زمن الترميز الحالية ليست Benchmark إنتاجيًا.
5. بعض الاختصارات العربية قد تحتاج قواعد تقسيم جمل إضافية.
6. Attention weights ليست تفسيرًا سببيًا كاملًا.
7. المقارنات الحالية لا تحل محل تقييم downstream tasks.
8. Gates B–E لم تُنفذ بعد.
9. لم يُعتمد أي نموذج بوصفه نموذج الإنتاج النهائي.
10. سيُعاد فحص القرارات بعد تجميد البيانات وظهور المقاييس النهائية.

---

# Conclusion | الخلاصة

اكتمل Gate A بدليل قابل لإعادة الفحص يشمل:

- معالجة النصوص بنسختين.
- إخفاء البيانات الاصطناعية الحساسة.
- معالجة عربية محافظة.
- قياسات Tokenizer ثنائية اللغة.
- اختبار اللواصق العربية.
- تجربة ثلاث بذور.
- Scaled Dot-Product Attention.
- Masks.
- Multi-Head Attention.
- Encoder Layer.
- Forward pass فعلي بالعربية والإنجليزية.
- مقارنة NumPy وPyTorch.
- اختبارات آلية ناجحة.

الحالة الحالية:

`Gate A = PASSED`

والمرحلة التالية للمشروع:

`Gate B — Classification, NER, and QA`
