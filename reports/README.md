# Reports

هذا المجلد يحفظ تقارير JSON/CSV/Markdown صغيرة وقابلة للمراجعة. لا تُرفع أوزان النماذج أو checkpoints أو secrets أو بيانات غير عامة.

## Evidence classes

### `smoke/`

نتائج تشغيل تشخيصية على بيانات الدورة الصغيرة وموسومة `MEASURED_SMOKE`.

هذه الملفات تثبت ما حدث فعليًا في تشغيل محدد، حتى عندما تكون النتيجة ضعيفة. لا تُحذف النتائج غير المريحة ولا تُخلط مع حزمة تقييم أخرى.

Current preserved smoke files:

- `smoke/day2_classification_metrics.json`
- `smoke/day2_ner_qa_metrics.json`

### T9 error analysis

- `T9_MANUAL_REVIEW.md`
- `t9_manual_error_review.csv`

Current evidence:

- `108` actual baseline retrieval errors reviewed row by row;
- review method: AI-assisted semantic inspection by GPT-5.6 Sol;
- improved path correct on `106/108` of those baseline errors;
- `T9_HUMAN_REVIEW_CLAIM=FALSE`.

This evidence is intentionally **not** relabelled as independent learner/instructor human review. If the academy requires a human reviewer specifically, that confirmation remains a human action.

### T10 local real-HTTP evidence

- `t10_local_cpu_http_benchmark.json`

This is a real local HTTP measurement on a documented Windows CPU at concurrency `16`.

It is `MEASURED_LOCAL`; it is not attributed to an academy reference-lab CPU unless that hardware identity is independently verified.

## Interpretation rule

Always interpret a number together with:

- data source;
- split/evaluation protocol;
- model/checkpoint;
- evidence class;
- hardware/runtime;
- whether the academy-frozen package was actually used.

`ACADEMY_FROZEN_EVAL_REPLACED=False`

**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
