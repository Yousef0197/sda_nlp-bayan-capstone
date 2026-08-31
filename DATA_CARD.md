# DATA_CARD — Bayan

## Purpose

بيانات تعليمية مصممة لاختبار مسار NLP ثنائي اللغة دون استخدام بيانات شخصية حقيقية أو بيانات حساسة.

## Data type

`Synthetic educational data`

أي أن النصوص والأسماء وأمثلة الهاتف والبريد صُنعت لأغراض التدريب والاختبار.

## Languages

- Arabic
- English

## Covered tasks

- preprocessing / PII masking
- topic classification
- sentiment classification
- NER
- extractive QA
- semantic retrieval
- behavioural evaluation
- API canaries

## Privacy

لا تحتوي الحزم المقصودة على:
- بيانات مستفيدين فعلية،
- بيانات حكومية سرية،
- أسرار أو API keys.

القيم التي تشبه الهاتف والبريد أمثلة اختبارية فقط.

## Splits

حيث تُستخدم splits، يتم الفصل بين Train / Validation / Test، ويُصرَّح في الدفتر:

`TEST_USED_FOR_SELECTION=False`

## Known limitations

1. البيانات صغيرة ومصممة لغرض تعليمي.
2. بعض acceptance suites سهلة نسبيًا ومحددة البنية.
3. الأداء عليها قد يكون أعلى بكثير من بيانات واقعية غير مرئية.
4. لا يمكن استخدام هذه الأرقام لتقدير production accuracy.
5. لا تستبدل أي Frozen Evaluation رسمي للأكاديمية.

## Recommended use

- التعليم.
- smoke testing.
- pipeline validation.
- reproducibility demonstrations.

## Inappropriate use

- اتخاذ قرارات عالية الأثر.
- تقييم أشخاص حقيقيين.
- الادعاء بجهوزية إنتاجية.
- الادعاء بأن نتائج synthetic data تمثل السكان أو المستخدمين الحقيقيين.

**Context:** Bayan — #SDAIA
