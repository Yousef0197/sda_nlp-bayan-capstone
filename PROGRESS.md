# PROGRESS — Bayan Gates A–E

**Student GitHub:** https://github.com/Yousef0197
**Repository:** https://github.com/Yousef0197/sda_nlp-bayan-capstone
**Last updated:** 2026-08-30

لا توضع علامة ✅ إلا بعد وجود دليل قابل للفحص، مثل نتيجة اختبار، أو Notebook منفّذ، أو قرار موثق، أو Commit عام.

---

## Gate status

| Gate | Status | Required evidence | Commit/report links | Blocker/next action |
|---|---|---|---|---|
| A — ingest | ✅ PASSED | preprocessing/tokenisation tests + attention tests + tokenizer decision + notebooks 01/02 | [Notebook 01 clean run](https://github.com/Yousef0197/sda_nlp-bayan-capstone/commit/c12b5013ee8419db4ea4f59699fd49e3f95750c2) · [Tokenizer decision evidence](https://github.com/Yousef0197/sda_nlp-bayan-capstone/commit/dfc4083264202b25b32cbcfaac335c349591aba7) · [Arabic clitic test](https://github.com/Yousef0197/sda_nlp-bayan-capstone/commit/3b1c903) · [Decision alignment](https://github.com/Yousef0197/sda_nlp-bayan-capstone/commit/fb647d6213c6830f022d1aa03cc3d051a7eaa543) · [Notebook 02](https://github.com/Yousef0197/sda_nlp-bayan-capstone/commit/24db4e4e7b0b6816727e95471129237d46358ddc) | Day 1 documentation closed; ready for Gate B |
| B — tasks | ⬜ NOT_STARTED | classification + NER + QA evidence | — | جاهز للبدء في Gate B |
| C — search & truth | ⬜ NOT_STARTED | search metrics + slices + taxonomy | — | يأتي بعد مهام Gate B |
| D — ship | ⬜ NOT_STARTED | project benchmark + API tests + canaries | — | يأتي بعد اكتمال التقييم والبحث |
| E — submit | ⬜ NOT_STARTED | validator + demo + release tag | — | يأتي بعد اكتمال Gates A–D |

Status values:

`⬜ NOT_STARTED`

`🟨 IN_PROGRESS`

`✅ PASSED`

`🟥 BLOCKED`

---

## Gate A — Day 1 evidence

### Lab 1 — Text Processing & Tokenisation

- Unicode inspection: `PASS`
- Two-copy preprocessing contract: `PASS`
- PII masking with synthetic educational data: `PASS`
- spaCy sentence pipeline: `PASS`
- Local WordPiece demonstration: `PASS`
- IDs-to-embeddings pipeline: `PASS`
- Notebook core marker: `DAY1_NOTEBOOK1_CORE=PASS`
- Clean-run environment: `Python 3.13.15`

### Day 1 automated tests

بعد آخر تعديلات Day 1 شُغّلت الاختبارات التالية معًا:

- `tests/test_day1_preprocessing.py`
- `tests/test_day1_tokenization.py`
- `tests/test_day1_attention.py`

بالأمر:

`$env:PYTHONPATH="src"; python -m pytest -q tests/test_day1_preprocessing.py tests/test_day1_tokenization.py tests/test_day1_attention.py`

وكانت النتيجة:

`10 passed in 0.16s`

وتشمل هذه النتيجة اختبار اللصيقة العربية المضاف إلى:

`tests/test_day1_tokenization.py`

---

## Tokenizer measurements

استُخدمت في المقارنة الحالية عينة اصطناعية ثابتة من أربعة نصوص عربية وأربعة نصوص إنجليزية.

### Measured bilingual fertility

| Tokenizer | Arabic fertility | English fertility |
|---|---:|---:|
| mBERT | `2.595` | `1.299` |
| AraBERT | `1.182` | `3.714` |

أظهر AraBERT خصوبة أقل في العربية، بينما أظهر mBERT توازنًا أفضل بين العربية والإنجليزية ضمن العينة الحالية.

لا يُستخدم هذا المقياس منفردًا لإثبات جودة المهمة النهائية.

### Measured bilingual truncation

| Tokenizer | max_length | Arabic | English | Combined |
|---|---:|---:|---:|---:|
| mBERT | 32 | `0.0%` | `0.0%` | `0.0%` |
| mBERT | 64 | `0.0%` | `0.0%` | `0.0%` |
| AraBERT | 32 | `0.0%` | `0.0%` | `0.0%` |
| AraBERT | 64 | `0.0%` | `0.0%` | `0.0%` |

لم تُظهر العينة الحالية قطعًا عند `32` أو `64`.

لذلك سيُعاد قياس طول التسلسل بعد تجميد مجموعة البيانات النهائية.

### Approximate tokenisation time

في التشغيل النظيف المحفوظ:

| Tokenizer | Mean tokenisation time |
|---|---:|
| mBERT | `0.1421 ms` |
| AraBERT | `0.1631 ms` |

هذه قياسات تقريبية من Notebook وعينة صغيرة، وليست Benchmark نهائيًا للخدمة.

### Initial decision

- Tokenizer: `google-bert/bert-base-multilingual-cased`
- Initial `max_length`: `64`
- Decision status: accepted as an initial measurable decision
- Re-evaluation trigger: frozen project dataset and downstream task metrics

### Known limitation

بيانات المقارنة الحالية تعليمية اصطناعية وصغيرة.

خصوبة الترميز ومعدل القطع والزمن التقريبي لا تثبت، منفردة، جودة النموذج النهائية في مهام المشروع.

---

## Lab 1 — Distinction evidence

### Arabic clitic probe

اختُبرت:

`الخدمة`

وكانت نتيجة mBERT:

`['ال', '##خدمة']`

بعدد:

`2`

قطع.

واختُبرت:

`وبالخدمة`

وكانت النتيجة:

`['وب', '##ال', '##خدمة']`

بعدد:

`3`

قطع.

Marker:

`DISTINCTION_CLITIC_TEST=PASS`

كما أُضيف اختبار آلي للحالة إلى:

`tests/test_day1_tokenization.py`

### mBERT / AraBERT comparison

Marker:

`DISTINCTION_TOKENIZER_COMPARISON=PASS`

### Bilingual truncation measurement

Marker:

`BILINGUAL_TRUNCATION_MEASUREMENT=PASS`

### Three-seed toy embedding experiment

استُخدمت البذور:

- `7`
- `42`
- `2026`

وبقي شكل المخرجات في جميع الحالات:

`(2, 5, 8)`

بينما تغيرت القيم العددية الناتجة عن التهيئة العشوائية.

Marker:

`DISTINCTION_THREE_SEEDS=PASS`

### Reproducible distinction run

Marker:

`DAY1_DISTINCTION_REPRODUCIBLE=PASS`

---

## Lab 2 — Attention & Transformers

- Scaled dot-product attention: `PASS`
- Attention row sums: `PASS`
- Keep-mask behaviour: `PASS`
- Multi-head split/combine round trip: `PASS`
- Encoder layer CPU execution: `PASS`
- BERT-family checkpoint architecture inspection: completed
- Arabic and English forward passes: completed
- Token-labelled attention visualisation: completed
- Notebook core marker: `DAY1_NOTEBOOK2_CORE=PASS`

### Attention automated tests

اختبارات الانتباه جزء من التشغيل الموحد:

`10 passed in 0.16s`

ويتضمن ملف الانتباه نفسه ثلاثة اختبارات ناجحة ضمن مجموعة Day 1 الحالية.

---

## Lab 2 — Distinction evidence

قورنت دلالات القناع بين NumPy وPyTorch باستخدام keep-mask نفسه.

Measured maximum difference:

`4.441e-16`

Observed semantics:

- `True` = المفتاح يشارك في الانتباه.
- `False` = المفتاح محجوب.
- المواضع المحجوبة أخذت احتمالًا صفريًا.
- نتائج NumPy وPyTorch تطابقت ضمن دقة floating-point.

Marker:

`DISTINCTION_MASK_SEMANTICS=PASS`

---

## Runtime / run-all evidence

| Notebook | Clean run date | Core marker | GitHub link |
|---|---|---|---|
| 00 | Not run separately | runtime checks | — |
| 01 | 2026-08-30 | `DAY1_NOTEBOOK1_CORE=PASS` | https://github.com/Yousef0197/sda_nlp-bayan-capstone/blob/main/notebooks/01_text_processing_tokenization.ipynb |
| 02 | 2026-08-30 | `DAY1_NOTEBOOK2_CORE=PASS` | https://github.com/Yousef0197/sda_nlp-bayan-capstone/blob/main/notebooks/02_attention_transformers.ipynb |
| 03 | — | not run | — |
| 04 | — | not run | — |
| 05 | — | not run | — |
| 06 | — | not run | — |
| 07 | — | not run | — |
| 08 | — | not run | — |

---

## Gate A reproducibility evidence

Notebook 01 أُعيد تشغيله من جلسة نظيفة وبالترتيب.

ظهرت العلامات:

`DAY1_NOTEBOOK1_CORE=PASS`

`DISTINCTION_CLITIC_TEST=PASS`

`DISTINCTION_THREE_SEEDS=PASS`

`DISTINCTION_TOKENIZER_COMPARISON=PASS`

`BILINGUAL_TRUNCATION_MEASUREMENT=PASS`

`DAY1_DISTINCTION_REPRODUCIBLE=PASS`

كما نُظفت بيانات Notebook الوصفية القديمة، وأصبح إصدار Python المسجل:

`3.13.15`

---

## Gate A evidence commits

- `46bda67` — جعل أدلة Distinction في Notebook 01 قابلة لإعادة التشغيل من جلسة نظيفة.
- `c12b501` — التحقق من التشغيل النظيف لـ Notebook 01.
- `dfc4083` — توثيق قرار المرمّز والقياسات داخل Notebook 01.
- `3b1c903` — إضافة اختبار اللصيقة العربية.
- `de53b08` — تنظيف بيانات التنفيذ الوصفية القديمة في Notebook 01.
- `fb647d6` — توحيد `DECISIONS.md` مع نتائج التشغيل النظيف الحالية.
- `24db4e4` — Notebook 02 مع أدلة الانتباه والمحولات.

---

## Gate A conclusion

Gate A requirements are supported by reproducible Day 1 evidence.

الأدلة الحالية تشمل:

- معالجة نصوص بنسختين: خامة ومهيأة للنموذج.
- إخفاء البريد والهاتف في البيانات الاصطناعية.
- فحص Unicode.
- تقسيم الجمل باستخدام spaCy مع توثيق حدوده.
- قياسات خصوبة الترميز الثنائية اللغة.
- قياسات القطع عند طولين.
- مقارنة mBERT وAraBERT.
- اختبار اللصيقة العربية `وبالخدمة`.
- تجربة ثلاث بذور للتضمينات التعليمية.
- تنفيذ آليات الانتباه ومتعدد الرؤوس وEncoder Layer.
- مقارنة دلالات القناع بين NumPy وPyTorch.
- Notebook 01 منفّذ من جلسة نظيفة.
- Notebook 02 منفّذ مع Core وDistinction evidence.
- قرار Tokenizer موثق في `DECISIONS.md`.
- اختبارات Day 1 كاملة: `10 passed in 0.16s`.
- عدم إدخال بيانات شخصية حقيقية أو مفاتيح مصادقة أو أوزان نماذج إلى تجارب Day 1.

### Day 1 documentation closure

اكتملت مراجعة توثيق Day 1 وإغلاقها.

تشمل أدلة الإغلاق الحالية:

- تحديث `README.md` بأدلة Gate A المقاسة.
- إضافة التقرير `reports/day1_report.md`.
- مراجعة اتساق الروابط والقياسات والـ commits.
- التحقق من نجاح اختبارات Day 1: `10 passed in 0.16s`.
- توثيق أدلة Core وDistinction.

Gate A مغلق توثيقيًا وتقنيًا، والمشروع جاهز للانتقال إلى Gate B.
---


## Day 1 — Official Explore / Distinction extensions

بعد إغلاق Gate A الأساسي، أُكملت عناصر Explore وDistinction الرسمية الإضافية وحُفظت أدلتها في الدفترين.

### Notebook 01

- `DAY1_EXPLORE_LOCAL_VS_MBERT_5=PASS`
- `DAY1_EXPLORE_PROFILE_COMPARISON=PASS`
- `DAY1_DISTINCTION_DIALECT_SLICE=PASS`
- `DAY1_NOTEBOOK1_OFFICIAL_EXTENSIONS=PASS`
- Evidence commit: `f86bd66` — `feat(day1): complete notebook 01 explore and distinction`

### Notebook 02

- `DAY1_CORE_CHANGE_V=PASS`
- `DAY1_EXPLORE_KEEP_MASK=PASS`
- `DAY1_EXPLORE_PADDING_MASK=PASS`
- `DAY1_DISTINCTION_SDPA_MULTI_SEED=PASS`
- `DAY1_DISTINCTION_T_SQUARED=PASS`
- `DAY1_NOTEBOOK2_DECISION_PROMPT=PASS`
- `DAY1_NOTEBOOK2_OFFICIAL_EXTENSIONS=PASS`
- Multi-seed NumPy/PyTorch SDPA maximum difference: `3.331e-16`
- Evidence commit: `65a0fb1` — `feat(day1): complete notebook 02 explore and distinction`

مراجعة JSON للدفترين أثبتت أن كل مجموعة إضافات موجودة في خلية واحدة فقط وأن معرّفات الخلايا فريدة؛ لا توجد خلايا مكررة تحتاج إلى حذف.


## Final release

- Final commit: not created yet
- Release/tag `submission-v1.0`: not created yet
- Validator pre-tag report: not run yet
- Validator `--require-tag` report: not run yet
- Private-window visibility check: not performed yet
- Remaining limitation: Gates B–E and final project evaluation remain incomplete
