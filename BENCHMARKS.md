# BENCHMARKS — Bayan

**Project:** Bayan — Bilingual Applied NLP Capstone  
**Training context:** Bayan — **#SDAIA**

## Benchmark policy

The program requires benchmark evidence to include environment, warm-up, repeated measurements, tail latency, throughput, memory and quality/rollback reasoning. This repository therefore separates:

- the full formal benchmark ladder in `notebooks/08_optimization_serving.ipynb`;
- the integration-notebook ASGI smoke measurement;
- the additional real-HTTP local CPU measurement preserved in `reports/t10_local_cpu_http_benchmark.json`.

No value is attributed to academy reference hardware unless that environment is actually verified.

---

## Formal Notebook 08 benchmark ladder

`notebooks/08_optimization_serving.ipynb` implements the following measurement contract:

1. capture Python/runtime/device/library versions;
2. record a budget before evaluating the candidate;
3. separate `SYSTEMS_SMOKE` from `PROJECT_ARTIFACT`;
4. warm up before measurement;
5. use at least 30 repeated calls in the formal benchmark path;
6. report p50/p95/p99 and throughput;
7. measure approximate process RSS start/observed peak;
8. audit sequence lengths and batching/padding choices;
9. preserve a PyTorch FP32 reference;
10. export/check ONNX and run ONNX Runtime;
11. verify numerical/prediction parity;
12. evaluate dynamic INT8 as a candidate rather than assuming it is better;
13. measure quality tax;
14. preserve an FP32 rollback/fallback path;
15. run FastAPI and startup/service canaries.

The notebook explicitly warns that its default small model path is `SYSTEMS_SMOKE` until the learner points it to the project artefact.

---

## Integration-notebook ASGI smoke

The integration notebook records:

- measurement path: FastAPI + ASGI transport
- concurrency: `16`
- measured requests: `128`
- HTTP p99: `32.907 ms`

**Evidence class:** `MEASURED_SMOKE`.

This result demonstrates the integrated service code path on the synthetic suite. It is not used as a reference-lab hardware claim.

---

## Real HTTP local CPU measurement

Evidence file:

`reports/t10_local_cpu_http_benchmark.json`

### Environment

- Platform: Windows 11
- Processor family: Intel64 Family 6 Model 142
- Logical CPUs: `8`
- Python: `3.13.14`
- Accelerator: CPU
- Server: Uvicorn in a separate localhost process
- Concurrency: `16`
- Warm-up requests: `32`
- Measured requests: `128`

### Measured latency

| Metric | Result |
|---|---:|
| HTTP p50 | `19.172 ms` |
| HTTP p95 | `24.805 ms` |
| HTTP p99 | `27.903 ms` |
| HTTP mean | `18.340 ms` |

Local numeric target:

`HTTP p99 <= 40 ms` at concurrency `16`

Result:

`T10_LOCAL_CPU_HTTP_TARGET_MET=True`

**Evidence class:** `MEASURED_LOCAL`.

---

## Throughput and memory boundary

The formal Notebook 08 benchmark schema records:

- `throughput_items_s`;
- approximate process RSS start and observed peak.

The standalone local HTTP JSON used for the `27.903 ms` result does **not** store total wall-clock throughput or peak RSS. Therefore no throughput or memory number is invented for that specific local run.

For a final hardware-specific benchmark package, rerun Notebook 08 in `PROJECT_MODE=True` (or an equivalent project-artifact benchmark on the designated machine), preserve its generated small report, and attribute the numbers only to that exact environment.

---

## Prediction parity and quality tax

The integration benchmark checks direct vs cached prediction parity and records:

`Prediction parity = 1.0`

Observed prediction changes on those measured parity cases:

`0`

Interpretation: caching did not change predictions on that measured suite. This is a parity statement, not a production-quality score.

Notebook 08 additionally contains the full quality-tax contract for FP32 / ONNX / INT8 candidate decisions.

---

## Rollback policy

A faster candidate is not adopted solely because its file is smaller or its average latency is lower.

The decision requires:

- acceptable tail latency;
- acceptable throughput;
- parity/quality within budget;
- startup canaries passing;
- an FP32 reproduction/rollback path.

If parity or quality fails, the safe decision is to keep/restore the FP32 reference.

---

## Program R5 interpretation

The local real-HTTP result is below the program numeric threshold of `40 ms` at concurrency `16`.

However, the formal R5 requirement ties the final claim to the academy-designated reference CPU when such a machine is specified. The repository therefore records:

**Local evidence:** ✅ measured and documented  
**Reference-lab equivalence:** ❌ not claimed without environment proof

This distinction is intentional and keeps the benchmark auditable.

---

## Reproducibility

Primary evidence:

- `notebooks/08_optimization_serving.ipynb`
- `notebooks/bayan_capstone.ipynb`
- `src/bayan/benchmarking.py`
- `src/bayan/serving.py`
- `tests/test_day4_benchmarking.py`
- `tests/test_day4_serving.py`
- `reports/t10_local_cpu_http_benchmark.json`

The final release should preserve the exact commit used for any reported project-artifact benchmark.

**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
