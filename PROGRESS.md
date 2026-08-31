# PROGRESS — Bayan Gates A–E

**Repository:** `Yousef0197/sda_nlp-bayan-capstone`  
**Last updated:** 2026-08-31  
**Canonical notebook:** `notebooks/bayan_capstone.ipynb`

لا توضع علامة نجاح نهائي إلا عندما يكون الدليل قابلًا للفحص وتكون بيئة القياس مطابقة للشرط الرسمي.

## Gate status

| Gate | Status | Evidence | Remaining |
|---|---|---|---|
| Gate A — ingest | ✅ COMPLETE | preprocessing, PII masking, tokenizer, embeddings, attention | — |
| Gate B — tasks | ✅ IMPLEMENTED / MEASURED_SMOKE | classification, sentiment, NER, QA; notebook thresholds pass | frozen/academy evaluation if separately required |
| Gate C — search & truth | 🟨 READY FOR FINAL REVIEW | FAISS, Recall/MRR, slices, CIs, invariance, MFT, 100-case table | final T9 review confirmation if required |
| Gate D — ship | 🟨 READY FOR ENV CHECK | FastAPI, parity, benchmark, measured extension | repeat T10 on official lab CPU if required |
| Gate E — submit | ⬜ PENDING | canonical clean-run notebook exists | validator, presentation, private-window check, final tag |

## Canonical notebook results

- Topic delta: `+0.858`
- Sentiment delta: `+0.663`
- NER entity F1: `1.000`
- QA no-answer: `20/20`
- Recall@10: `1.000`
- MRR@10: `1.000`
- Invariance: `1.000`
- MFT: `1.000`
- HTTP p99: `32.907 ms` at concurrency 16, Colab ASGI path
- Extension delta: `+0.88`
- Final marker: `BAYAN_DAY1_DAY4_OFFICIAL_THRESHOLDS=PASS`

## Evidence interpretation

`MEASURED_SMOKE=True`

تعني أن الأرقام ناتجة من تشغيل فعلي للـNotebook على الحزم التعليمية الاصطناعية.

`ACADEMY_FROZEN_EVAL_REPLACED=False`

تعني أن هذه الحزم لا تدّعي استبدال تقييم مجمد رسمي.

## Recovery point

إذا تعطل أي شيء قبل التسليم:

1. لا تعدل الـcanonical notebook الذي مر Clean Run إلا لإصلاح إلزامي.
2. أعد تشغيله من جلسة جديدة.
3. لا تخفض thresholds.
4. لا تنقل نتائج من تشغيل سابق إلى تشغيل جديد يدويًا.
5. وثّق القياس والبيئة والحدود.

## Submission blockers

- [ ] T9 final review confirmation if required.
- [ ] T10 official lab CPU verification if required.
- [ ] Final validator.
- [ ] Presentation.
- [ ] Private-window public repository check.
- [ ] Final tag `submission-v1.0`.

**Context tag:** #SDAIA
