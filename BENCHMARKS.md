# BENCHMARKS — Bayan

**Project:** Bayan — Bilingual Applied NLP Capstone  
**Program:** SDA-AIE-211 — Natural Language Processing with Transformers  
**Academy:** [@SDAIAAcademy](https://github.com/SDAIAAcademy) — **#SDAIA**  
**Benchmark status:** ✅ **COMPLETE**

## Benchmark objective

T10 requires a measured optimisation/service path with a benchmark ladder, parity/quality reasoning, tail latency and concurrency evidence. The project preserves both the formal optimisation notebook and a real HTTP measurement artifact.

Primary evidence:

- `notebooks/08_optimization_serving.ipynb`
- `notebooks/bayan_capstone.ipynb`
- `src/bayan/benchmarking.py`
- `src/bayan/serving.py`
- `tests/test_day4_benchmarking.py`
- `tests/test_day4_serving.py`
- `reports/t10_local_cpu_http_benchmark.json`

## Formal Notebook 08 benchmark ladder

`notebooks/08_optimization_serving.ipynb` implements the full measurement contract:

1. capture runtime/device/library versions;
2. define a budget before selecting a candidate;
3. warm up before timed measurements;
4. use repeated measurements;
5. report p50/p95/p99;
6. report throughput;
7. track approximate process RSS start/observed peak;
8. audit sequence lengths and batching/padding choices;
9. preserve a PyTorch FP32 reference;
10. export/check ONNX and evaluate ONNX Runtime;
11. verify numerical/prediction parity;
12. evaluate dynamic INT8 as a candidate;
13. measure quality tax;
14. preserve FP32 rollback/fallback;
15. execute service/startup canaries.

This provides the required optimisation ladder rather than selecting a candidate from one latency number.

## Integration service measurement

The integration notebook records an ASGI service measurement at concurrency `16` with `128` measured requests and HTTP p99 `32.907 ms`.

This confirms the integrated API path and provides an additional reproducible service measurement.

## Real HTTP measurement

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

### Latency results

| Metric | Result |
|---|---:|
| HTTP p50 | `19.172 ms` |
| HTTP p95 | `24.805 ms` |
| HTTP p99 | `27.903 ms` |
| HTTP mean | `18.340 ms` |

Program numeric target:

`HTTP p99 <= 40 ms` at concurrency `16`

Measured result:

`27.903 ms`

Target comparison:

`27.903 < 40.000`

**T10 latency target:** ✅ PASS

## Throughput and memory

The formal Notebook 08 benchmark path records:

- `throughput_items_s`;
- approximate process RSS start;
- observed process RSS peak.

These measurements are part of the formal candidate-comparison schema and are interpreted together with latency, parity and quality tax.

## Prediction parity

The integration benchmark checks direct vs cached prediction parity and records:

`Prediction parity = 1.0`

Observed prediction changes on the measured parity cases:

`0`

This verifies that the measured caching optimisation did not change predictions on the parity suite.

## ONNX / INT8 decision framework

The optimisation notebook includes:

- FP32 baseline;
- ONNX export/check;
- ONNX Runtime candidate;
- INT8 candidate;
- output parity checks;
- quality-tax calculation;
- speed/size comparison;
- rollback decision.

An optimisation candidate is adopted only when it preserves the defined quality/parity budget and improves the selected performance objective.

## Rollback policy

The FP32 reference is preserved as the fallback path. If a candidate fails parity, quality tax, startup canaries or the performance budget, the service can revert to the reference implementation without changing the API contract.

## Reproducibility

Run the formal benchmark notebook from a clean runtime and preserve the generated small report with the exact environment and commit. The standalone real-HTTP JSON already records the environment and measured latency values for the documented run.

## Distinction evidence

The benchmark package strengthens the project through:

- explicit benchmark design;
- warm-up and repeated measurements;
- tail latency rather than mean-only reporting;
- concurrency `16` evidence;
- throughput and memory instrumentation;
- parity and quality-tax checks;
- ONNX/INT8 candidate comparison;
- rollback reasoning;
- reproducible environment documentation.

## Final benchmark status

**Benchmark ladder:** ✅ COMPLETE  
**p50/p95/p99:** ✅ COMPLETE  
**Concurrency 16 measurement:** ✅ COMPLETE  
**HTTP p99 target:** ✅ PASS  
**Throughput/memory instrumentation:** ✅ COMPLETE  
**Parity/quality tax:** ✅ COMPLETE  
**ONNX/INT8/rollback path:** ✅ COMPLETE  
**T10:** ✅ COMPLETE

**Academy GitHub:** [@SDAIAAcademy](https://github.com/SDAIAAcademy)  
**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
