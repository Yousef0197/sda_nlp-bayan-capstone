# BENCHMARKS — Bayan

## Project

**Bayan — Bilingual Applied NLP Capstone**

**Status:** ✅ COMPLETE

**Training context:** Bayan — #SDAIA

---

## Purpose

يوثّق هذا الملف قياسات الأداء الخاصة بمسار Day 4، مع الفصل بين:

- benchmark ladder داخل الـcanonical notebook،
- parity / quality check،
- قياس FastAPI عبر ASGI داخل Colab،
- والقياس النهائي عبر real HTTP على CPU محلي.

الدفتر المرجعي:

`notebooks/bayan_capstone.ipynb`

دليل القياس النهائي:

`reports/t10_local_cpu_http_benchmark.json`

---

## T10 requirement

هدف الأداء المستخدم في المشروع:

- HTTP p99 ≤ `40 ms`
- Concurrency = `16`

---

## Benchmark ladder

يحتوي الـcanonical notebook على مسار قياس تدريجي بدل القفز مباشرة إلى HTTP:

1. direct classification path.
2. cached classification path.
3. FastAPI / ASGI path.
4. real HTTP service benchmark.

هذا يسمح بفصل تكلفة منطق التصنيف عن تكلفة طبقة الخدمة والنقل.

---

## Direct vs cached prediction parity

يقيس الـNotebook مسارين:

- `classify_direct`
- `classify_cached`

ويتحقق صراحة من تطابق المخرجات:

`before_bench["outputs"] == after_bench["outputs"]`

كما يسجل:

`Prediction parity = 1.0`

والعلامة:

`DAY4_BENCHMARK_PARITY=PASS`

### Quality tax interpretation

على عينة الـbenchmark المستخدمة في فحص parity:

- Prediction parity: `1.0`
- Observed prediction changes: `0`
- Observed prediction-quality tax from caching on those cases: `0`

هذا لا يعني أن الجودة الإنتاجية مضمونة على بيانات خارجية؛ بل يعني فقط أن تحسين caching لم يغيّر المخرجات على حالات parity المقاسة.

---

## Canonical notebook ASGI smoke measurement

في التشغيل الكامل المرجعي للـNotebook تم تسجيل:

- Concurrency: `16`
- HTTP/ASGI p99: `32.907 ms`

هذا القياس موثّق بوصفه smoke measurement داخل بيئة Colab.

لا يُستخدم هذا القياس وحده للادعاء بأنه benchmark على جهاز lab CPU محدد.

---

## Real HTTP local CPU benchmark

بعد فصل طبقة الخدمة وتشغيل benchmark حقيقي عبر HTTP محلي، كانت البيئة:

- Platform: Windows 11
- CPU count: `8`
- Concurrency: `16`
- Warm-up requests: `32`
- Measured requests: `128`

### Results

| Metric | Result |
|---|---:|
| HTTP p50 | `19.172 ms` |
| HTTP p95 | `24.805 ms` |
| HTTP p99 | `27.903 ms` |
| HTTP mean | `18.340 ms` |

### Threshold check

Target:

`HTTP p99 <= 40 ms`

Measured:

`27.903 ms`

Result:

`T10_LOCAL_CPU_HTTP_TARGET_MET=True`

`T10_LOCAL_CPU_HTTP_BENCHMARK=PASS`

---

## Final T10 evidence

النتيجة النهائية المستخدمة في التوثيق:

**HTTP p99 = `27.903 ms` at concurrency `16` using real HTTP on local CPU.**

الدليل القابل للفحص:

`reports/t10_local_cpu_http_benchmark.json`

**Status:** ✅ PASS

---

## Environment boundary

القياس النهائي أعلاه تم على CPU محلي بنظام Windows، وليس على جهاز تم إثبات أنه جهاز academy lab CPU بعينه.

إذا كانت الأكاديمية تعلن جهازًا أو بيئة lab CPU محددة إلزاميًا، فيجب إعادة القياس على تلك البيئة قبل نسب النتيجة إليها.

كما أن القياسات داخل الـcanonical notebook تستخدم بيانات تعليمية اصطناعية ولا تستبدل أي Frozen Evaluation رسمي مستقل.

---

## Benchmark interpretation

النتيجة المهمة هندسيًا هي أن منطق الخدمة نفسه ليس عنق الزجاجة في القياس المحلي النهائي، وأن مسار real HTTP على الجهاز المحلي حقق الحد المستهدف.

ويُحافظ على الفصل بين:

- correctness / parity،
- service latency،
- HTTP transport overhead،
- والبيئة التي تم فيها القياس.

---

## Reproducibility evidence

الملفات ذات الصلة:

- `notebooks/bayan_capstone.ipynb`
- `reports/t10_local_cpu_http_benchmark.json`
- `EVALUATION_REPORT.md`
- `DECISIONS.md`
- `PROGRESS.md`

---

## Final benchmark status

**Benchmark ladder:** ✅ DOCUMENTED  
**Prediction parity:** `1.0` ✅ PASS  
**Observed parity quality tax:** `0` prediction changes on measured parity cases  
**Real HTTP local CPU p99:** `27.903 ms`  
**Concurrency:** `16`  
**Target:** `<= 40 ms`  
**T10 status:** ✅ PASS

**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
