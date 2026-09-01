# Bayan — Bilingual Applied NLP Capstone

مشروع تطبيقي ثنائي اللغة في معالجة اللغة الطبيعية، مبني ضمن مسار **Bayan** ويغطي مختبرات الأيام الأربعة في Notebook موحّد قابل لإعادة التشغيل.

**Student:** Yousef Al-Mutiri  
**Repository:** `Yousef0197/sda_nlp-bayan-capstone`  
**Canonical notebook:** `notebooks/bayan_capstone.ipynb`  
**Open in Colab:** https://colab.research.google.com/github/Yousef0197/sda_nlp-bayan-capstone/blob/main/notebooks/bayan_capstone.ipynb

**Status:** Day 1–Day 4 implementation complete; final submission validated and tagged as `submission-v1.0`.

> **Program / البرنامج:** SDA-AIE-211 — Natural Language Processing with Transformers  
> **Instructor / المدربة:** Meaad Al-Marri | ميعاد المري  
> **Academy / الأكاديمية:** [@SDAIAAcademy](https://github.com/SDAIAAcademy) — أكاديمية سدايا

---

## Executive summary | الملخص

يبني مشروع **Bayan** خط معالجة ثنائي اللغة للعربية والإنجليزية يشمل:

- حماية البيانات ومعالجة النصوص.
- Tokenization وTransformer literacy.
- تصنيف الموضوع والمشاعر.
- NER.
- Extractive QA.
- بحثًا دلاليًا باستخدام FAISS.
- تقييمًا سلوكيًا وشرائح وثقة.
- تحليل أخطاء.
- Benchmark وخدمة FastAPI.
- امتدادًا مقاسًا قبل/بعد.

جميع بيانات التطوير والتقييم داخل الـNotebook **تعليمية اصطناعية** وليست بيانات مستفيدين حقيقية أو بيانات حكومية حساسة.

---

## Canonical clean run | التشغيل الكامل

الدفتر الرئيسي:

`notebooks/bayan_capstone.ipynb`

تم تشغيله من البداية إلى النهاية في Google Colab على T4 دون أخطاء، وانتهى بالعلامة:

`BAYAN_DAY1_DAY4_OFFICIAL_THRESHOLDS=PASS`

مع:

- `MEASURED_SMOKE=True`
- `TEST_USED_FOR_SELECTION=False`
- `ACADEMY_FROZEN_EVAL_REPLACED=False`

النتائج أدناه تجمع بين نتائج التشغيل الكامل للـNotebook على بيئة Colab والأدلة المقاسة الإضافية الموثقة داخل المستودع، مع توضيح بيئة كل قياس.

---

## Measured results | النتائج المقاسة

| Requirement | Measured result / evidence | Status |
|---|---:|---|
| T3 Topic improvement vs baseline | `+0.858` Macro-F1 | PASS |
| T3 Sentiment improvement vs baseline | `+0.663` Macro-F1 | PASS |
| T4 NER entity-level F1 | `1.000` | PASS |
| T5 QA no-answer | `20/20` | PASS |
| T7 Recall@10 | `1.000` | PASS |
| T7 MRR@10 | `1.000` | PASS |
| T8 Invariance | `1.000` | PASS |
| T8 MFT | `1.000` | PASS |
| T9 error analysis | `100` generated review cases; `20` manually reviewed errors + 3 prioritized fixes | PASS |
| T10 HTTP p99 | `27.903 ms` at concurrency 16 using real HTTP on local CPU | PASS |
| T11 FastAPI | `/health`, `/v1/classify`, ar/en, invalid input, PII canary | PASS |
| T12 measured extension | `+0.88` Top-1 delta | PASS |

### Important benchmark boundary

The final real-HTTP CPU benchmark was executed locally on Windows with 8 logical CPUs at concurrency 16.

Measured HTTP p99:

`27.903 ms`

This is below the project threshold of `40 ms`.

The earlier Colab ASGI measurement remains a smoke measurement. If the academy requires execution on a specifically designated lab CPU, that exact hardware environment has not been independently verified.

---

## Day 1 — Text processing & transformers

يشمل:

- Unicode inspection.
- PII masking.
- معالجة عربية موحّدة.
- token fertility.
- truncation.
- contextual embeddings.
- scaled dot-product attention.
- padding-mask semantics.

---

## Day 2 — Applied NLP tasks

### Topic & sentiment

- TF-IDF baseline.
- Transformer training path.
- مقارنة Macro-F1 قابلة للقياس.

### NER

- `word_ids()`.
- `-100` للـspecial tokens والـcontinuation subwords.
- optimizer step.
- entity-level precision/recall/F1.

### Extractive QA

- start/end position preparation.
- valid-span constraints.
- no-answer handling.
- اختبار 20 حالة no-answer.

---

## Day 3 — Search & evaluation

- unified train/eval/serve Arabic profile.
- Arabic canaries.
- FAISS manifest.
- retrieve + rerank.
- Recall@10 / MRR@10.
- Arabic/English slices.
- bootstrap confidence intervals.
- Invariance.
- MFT.
- 100-case generated error-review table.
- 20 errors manually reviewed and categorized.
- 3 prioritized fixes.

**T9 status:** تم إنشاء جدول من 100 حالة، ومراجعة 20 خطأ فعليًا يدويًا وتصنيفها، مع تحديد 3 إصلاحات مرتبة حسب الأولوية.

---

## Day 4 — Serving & measured extension

- benchmark ladder.
- parity check.
- FastAPI service.
- `/health`.
- `/v1/classify`.
- Arabic/English requests.
- invalid-input handling.
- startup/API canaries.
- concurrency 16 benchmark.
- measured bilingual retrieval extension.

### Extension decision

تم قياس bilingual concept canonicalization + reranking قبل/بعد.

النتيجة:

`Top-1 delta = +0.88`

القرار:

`ADOPT`

الحالة:

`PASS`

---

## Architecture | المعمارية

```mermaid
flowchart LR
    A["Arabic / English educational text"] --> B["PII masking + preprocessing"]
    B --> C["Tokenizer"]
    C --> D["Topic / Sentiment"]
    C --> E["NER"]
    C --> F["Extractive QA"]
    B --> G["Embeddings"]
    G --> H["FAISS + re-ranking"]
    D --> I["Evaluation"]
    E --> I
    F --> I
    H --> I
    I --> J["Slices + behavioural tests + errors"]
    J --> K["Benchmark"]
    K --> L["FastAPI"]
```

---

## Privacy & responsible use

- لا تُستخدم بيانات شخصية حقيقية.
- أمثلة الهاتف والبريد مصطنعة لاختبار masking.
- لا توجد مفاتيح API في المستودع.
- لا تُرفع `.env`.
- لا تُرفع model weights أو checkpoints أو caches.
- لا يُعد المشروع نظامًا إنتاجيًا لاتخاذ قرارات عالية الأثر.
- النتائج المقاسة على البيانات الاصطناعية لا تعني جودة مماثلة على بيانات واقعية غير مرئية.

---

## Reproducibility

تشغيل الدفتر:

1. افتح `notebooks/bayan_capstone.ipynb` في Colab.
2. اختر T4 GPU إذا كان متاحًا.
3. استخدم `Runtime → Restart session and run all`.
4. راقب العلامة النهائية.
5. لا تستخدم Test لاختيار seed/threshold/model.

---

## Repository documentation

- `README.md`
- `DATA_CARD.md`
- `MODEL_CARD.md`
- `EVALUATION_REPORT.md`
- `BENCHMARKS.md`
- `DECISIONS.md`
- `PROGRESS.md`
- `PROJECT_SUMMARY.json`
- `SUBMISSION.yml`
- `notebooks/bayan_capstone.ipynb`

---

## Final submission status

- Day 1–Day 4 implementation complete.
- T9 manual error-review evidence recorded.
- T10 real-HTTP local CPU benchmark recorded.
- Submission validator: `BAYAN_SUBMISSION_VALIDATOR=PASS`.
- Public GitHub repository verified in a private browser window.
- Public Colab notebook link verified in a private browser window.
- Final presentation complete.
- Final tag: `submission-v1.0`.

---

## Acknowledgement & tags

نُفذ هذا المشروع ضمن برنامج **SDA-AIE-211 — Natural Language Processing with Transformers**، بإعداد وتقديم المدربة **ميعاد المري | Meaad Al-Marri**، ضمن برامج **أكاديمية سدايا**.

GitHub: [@SDAIAAcademy](https://github.com/SDAIAAcademy)

**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
