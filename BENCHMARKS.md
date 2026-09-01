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

## Executed optimisation evidence in Notebook 08

The committed Notebook 08 contains an executed `SYSTEMS_SMOKE` optimisation run on CPU. It is retained as systems-level evidence for the export/quantisation/parity path and is kept distinct from the real HTTP service benchmark below.

Recorded runtime:

- Python `3.12.13`
- PyTorch `2.13.0+cpu`
- device `cpu`
- ONNX Runtime CPU provider available
- reference model `google/bert_uncased_L-2_H-128_A-2`
- warm-up `5`
- repetitions `30`
- items per model-only call `8`

### Candidate comparison

| Candidate | Size | p95 model-only | Prediction parity | Decision evidence |
|---|---:|---:|---:|---|
| PyTorch FP32 reference | `16.732 MiB` parameter state | `9.908 ms` | reference | rollback/reference path |
| ONNX FP32 | `16.788 MiB` | `6.418 ms` | `1.000` | ONNX checker + parity PASS |
| ONNX dynamic INT8 | `4.272 MiB` | `1.731 ms` | `1.000` | candidate budget PASS |

ONNX FP32 numerical parity recorded:

`max_abs_logits_diff = 1.4901161193847656e-07`

The notebook records both FP32-ORT and INT8 latency/quality/throughput budget checks as passing for this executed systems workload. The selected systems-smoke candidate is dynamic INT8. The notebook explicitly treats that systems-smoke selection as a benchmark-path decision rather than a substitute for a separately measured production-quality claim.

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

The formal benchmark helper and Notebook 08 record the measurement contract for:

- `throughput_items_s`;
- approximate `rss_start_mb`;
- `rss_peak_observed_mb`;
- `rss_observed_delta_mb`.

The RSS method is process RSS at benchmark start plus the maximum value observed during repeated calls. It is intentionally described as an approximation rather than exact tensor allocation. The candidate budget also checks minimum throughput alongside latency and quality tax.

The standalone real-HTTP JSON is the preserved evidence for the `27.903 ms` p99 run; it records its request count, concurrency and latency distribution. Candidate throughput/RSS evidence belongs to the formal Notebook 08 benchmark report and is not inferred from the standalone latency JSON.

## Prediction parity and quality tax

The optimisation evidence includes two complementary parity checks:

- ONNX FP32 prediction agreement with the PyTorch reference: `1.000`;
- INT8 prediction agreement with the FP32 reference: `1.000`.

The integration benchmark additionally records direct-vs-cached prediction parity of `1.0` with `0` observed prediction changes on its measured suite.

Candidate adoption is evaluated together with quality tax rather than speed alone.

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

The committed notebook records model/runtime versions, workload configuration, warm-up/repetition counts, hashes, artifact sizes and decision logic. The standalone real-HTTP JSON records the environment and measured latency values for the documented concurrency-16 run.

For final verification:

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src python scripts/validate_submission.py .
```

## Distinction evidence

The benchmark package strengthens the project through:

- explicit benchmark design;
- warm-up and repeated measurements;
- tail latency rather than mean-only reporting;
- concurrency `16` real-HTTP evidence;
- measured FP32 → ONNX → INT8 size/latency comparison;
- throughput and memory instrumentation;
- numerical and prediction parity;
- quality-tax checks;
- rollback reasoning;
- reproducible environment documentation.

## Final benchmark status

**Benchmark ladder:** ✅ COMPLETE  
**p50/p95/p99:** ✅ COMPLETE  
**Concurrency 16 measurement:** ✅ COMPLETE  
**HTTP p99 target:** ✅ PASS  
**Artifact size comparison:** ✅ COMPLETE  
**Throughput/memory measurement path:** ✅ COMPLETE  
**Parity/quality tax:** ✅ COMPLETE  
**ONNX/INT8/rollback path:** ✅ COMPLETE  
**T10:** ✅ COMPLETE

**Academy GitHub:** [@SDAIAAcademy](https://github.com/SDAIAAcademy)  
**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
