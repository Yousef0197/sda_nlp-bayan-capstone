# BENCHMARKS — Bayan

## Project

**Bayan — Bilingual Applied NLP Capstone**

**Status:** ✅ COMPLETE

**Training context:** Bayan — #SDAIA

---

## Benchmark overview

يوثّق هذا الملف نتائج قياس الأداء والخدمة في المشروع، مع التركيز على زمن الاستجابة، التوازي، وثبات النتائج.

---

## Classification parity

تم التحقق من تطابق النتائج بين مسار التنفيذ الأساسي والمسار المحسّن.

### Result

- Prediction parity: `1.000`

**Status:** ✅ PASS

---

## HTTP Benchmark

### Configuration

- Framework: FastAPI
- Concurrency: `16`
- Measured requests: `128`
- Warm-up requests: `32`

### Result

- HTTP p99: `32.907 ms`

### Threshold

- Required p99: ≤ `40 ms`

**Status:** ✅ PASS

---

## FastAPI checks

تم اختبار:

- `GET /health`
- `POST /v1/classify`
- Arabic requests
- English requests
- Invalid input
- PII masking
- Startup/API canaries

**Status:** ✅ PASS

---

## Measured Extension

### Extension

Bilingual concept canonicalization + reranking

### Before / After

- Top-1 improvement: `+0.88`

### Decision

`KEEP`

**Status:** ✅ PASS

---

## Final benchmark summary

| Check | Result | Status |
|---|---:|---|
| Prediction parity | `1.000` | ✅ PASS |
| Concurrency | `16` | ✅ PASS |
| HTTP p99 | `32.907 ms` | ✅ PASS |
| FastAPI health/classify | Complete | ✅ PASS |
| Arabic/English requests | Complete | ✅ PASS |
| Invalid input handling | Complete | ✅ PASS |
| PII canary | Complete | ✅ PASS |
| Measured extension | `+0.88` | ✅ PASS |

---

## Final status

**Benchmarking:** ✅ COMPLETE  
**Serving checks:** ✅ COMPLETE  
**Performance threshold:** ✅ PASS  
**Measured extension:** ✅ PASS  

**BENCHMARKS — COMPLETE**

**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
