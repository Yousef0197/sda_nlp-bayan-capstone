# Reports

هذا المجلد يحفظ أدلة القياس الصغيرة والقابلة للمراجعة بصيغ JSON/CSV/Markdown. لا تُرفع أوزان النماذج أو checkpoints أو secrets أو بيانات غير عامة.

**Reports status:** ✅ **COMPLETE**

## Day 1

- `day1_report.md`

Includes tokenizer fertility, truncation evidence, attention interpretation and Day 1 architectural decisions.

## Day 2 measured runs

Preserved diagnostic reports:

- `smoke/day2_classification_metrics.json`
- `smoke/day2_ner_qa_metrics.json`

These files preserve the exact results of short measured runs, including weaker outcomes, so different training protocols remain auditable rather than overwritten.

## T9 — error analysis

Evidence:

- `T9_MANUAL_REVIEW.md`
- `t9_manual_error_review.csv`

Recorded results:

- baseline errors reviewed row by row: `108`;
- improved path correct on reviewed baseline errors: `106/108`;
- residual improved errors: `2`;
- prioritized fixes: `3`.

Error categories:

- cross-language intent/specificity gap: `56`;
- hash collision/candidate ordering: `44`;
- modifier-noise ranking instability: `8`.

**T9 status:** ✅ COMPLETE

## T10 — real HTTP benchmark

Evidence:

- `t10_local_cpu_http_benchmark.json`

Recorded run:

- Windows 11 CPU environment;
- 8 logical CPUs;
- concurrency `16`;
- warm-up `32` requests;
- measured `128` requests;
- p50 `19.172 ms`;
- p95 `24.805 ms`;
- p99 `27.903 ms`;
- mean `18.340 ms`.

Notebook 08 contains the complete benchmark ladder for throughput, memory, FP32, ONNX, INT8, parity, quality tax and rollback.

**T10 status:** ✅ COMPLETE

## Evidence interpretation

Each report should be interpreted together with its:

- data source;
- split/evaluation protocol;
- model/checkpoint;
- runtime/environment;
- metric definition;
- associated notebook or source path.

This structure keeps the measured evidence reproducible, reviewable and traceable to the code that produced it.

## Final status

**Day 1 evidence:** ✅ COMPLETE  
**Day 2 measured reports:** ✅ COMPLETE  
**T9 error analysis:** ✅ COMPLETE  
**T10 benchmark evidence:** ✅ COMPLETE  
**Reports package:** ✅ COMPLETE

**Academy GitHub:** [@SDAIAAcademy](https://github.com/SDAIAAcademy)  
**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
