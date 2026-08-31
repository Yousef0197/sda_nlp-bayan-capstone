# EVALUATION_REPORT — Bayan

## Evaluation policy

- القياسات المعلنة مصدرها الـcanonical notebook.
- جميع النتائج الواردة في هذا التقرير ناتجة من تشغيل المشروع فعليًا.
- لا يُستخدم Test في model/threshold selection.
- الحزم الحالية synthetic acceptance suites.
- `ACADEMY_FROZEN_EVAL_REPLACED=False`.

## Results

| Test | Result | Threshold represented in notebook |
|---|---:|---:|
| Topic delta vs baseline | `+0.858` | ≥ `+0.08` |
| Sentiment delta vs baseline | `+0.663` | ≥ `+0.08` |
| NER entity-F1 | `1.000` | ≥ `0.80` |
| QA no-answer | `20/20` | ≥ `17/20` |
| Recall@10 | `1.000` | ≥ `0.80` |
| MRR@10 | `1.000` | ≥ `0.70` |
| Invariance | `1.000` | ≥ `0.95` |
| MFT | `1.000` | ≥ `0.90` |
| HTTP p99 | `32.907 ms` | ≤ `40 ms` |
| Extension delta | `+0.88` | positive before/after |

## Slices

البحث الدلالي يحسب شرائح بحسب اللغة:
- Arabic.
- English.

ويحسب bootstrap confidence intervals داخل مسار Day 3.

## Behavioural tests

### Invariance

يتحقق من ثبات نتيجة البحث تحت تغييرات مثل:
- المسافات.
- علامات الترقيم.
- التشكيل.
- normalization variants.

Measured: `1.000`.

### MFT

يغطي minimum functionality مثل:
- email masking.
- phone masking.
- Arabic normalization.
- retrieval expectations.

Measured: `1.000`.

## Error analysis

تم تجهيز `100` حالة من baseline مقابل improved retrieval مع:
- automatic error flag.
- language.
- expected document.
- baseline top-1.
- improved top-1.
- taxonomy أولية.

الإصلاحات المرتبة:
1. bilingual concept canonicalization.
2. FAISS + reranking.
3. unified train/eval/serve Arabic profile.

### Human-review boundary

لا يُقدَّم التصنيف الآلي على أنه مراجعة بشرية. إذا كان T9 يتطلب "قراءة وتصنيف" يدويًا، يجب توثيق human sign-off قبل Gate E.

## Interpretation

الأرقام المرتفعة لا تعني 100% production accuracy، لأنها ناتجة من synthetic educational suites.

## Remaining validation

- official frozen evaluation إذا كانت منفصلة.
- official lab CPU benchmark إذا كان مطلوبًا حرفيًا.
- submission validator.
- release tag.

**Training context:** #SDAIA
