# PROGRESS — Bayan Gates A–E

**Student GitHub:** https://github.com/Yousef0197
**Repository:** https://github.com/Yousef0197/sda_nlp-bayan-capstone**Last updated:** 2026-08-30

لا توضع علامة ✅ إلا بعد وجود دليل قابل للفحص، مثل نتيجة اختبار، أو Notebook منفّذ، أو قرار موثق، أو Commit عام.

---

## Gate status

| Gate | Status | Required evidence | Commit/report links | Blocker/next action |
|---|---|---|---|---|
| A — ingest | ✅ PASSED | preprocessing/tokenisation tests + attention tests + tokenizer decision + notebooks 01/02 | [Notebook 01](https://github.com/Yousef0197/sda_nlp-bayan-capstone/commit/696bb0feb30567b4e618eede8173dcbfc6c68f2d) · [Tokenizer decision](https://github.com/Yousef0197/sda_nlp-bayan-capstone/commit/e3f3a11119988f7d953f374adc805f206e281a1f) · [Notebook 02](https://github.com/Yousef0197/sda_nlp-bayan-capstone/commit/24db4e4e7b0b6816727e95471129237d46358ddc) | لا يوجد عائق — الانتقال إلى Gate B بعد إغلاق Commit اليوم الأول |
| B — tasks | ⬜ NOT_STARTED | classification + NER + QA evidence | — | البدء بعد إغلاق Gate A |
| C — search & truth | ⬜ NOT_STARTED | search metrics + slices + taxonomy | — | يأتي بعد مهام Gate B |
| D — ship | ⬜ NOT_STARTED | project benchmark + API tests + canaries | — | يأتي بعد اكتمال التقييم والبحث |
| E — submit | ⬜ NOT_STARTED | validator + demo + release tag | — | يأتي بعد اكتمال Gates A–D |

Status values: `⬜ NOT_STARTED`, `🟨 IN_PROGRESS`, `✅ PASSED`, `🟥 BLOCKED`.

---

## Gate A — Day 1 evidence

### Lab 1 — Text Processing & Tokenisation

- Unicode inspection: `PASS`
- Two-copy preprocessing contract: `PASS`
- PII masking with synthetic educational data: `PASS`
- spaCy sentence pipeline: `PASS`
- Local WordPiece demonstration: `PASS`
- IDs-to-embeddings pipeline: `PASS`
- Notebook core marker: `DAY1_NOTEBOOK1_CORE=PASS`
- Official preprocessing/tokenisation tests: `6 passed in 0.42s`

### Tokenizer measurements

Measured bilingual fertility:

| Tokenizer | Arabic fertility | English fertility |
|---|---:|---:|
| mBERT | 3.756 | 1.500 |
| AraBERT | 1.515 | 4.446 |

Measured bilingual truncation:

| Tokenizer | max_length | Arabic | English | Combined |
|---|---:|---:|---:|---:|
| mBERT | 32 | 0.0% | 0.0% | 0.0% |
| mBERT | 64 | 0.0% | 0.0% | 0.0% |
| AraBERT | 32 | 0.0% | 75.0% | 37.5% |
| AraBERT | 64 | 0.0% | 0.0% | 0.0% |

Initial decision:

- Tokenizer: `google-bert/bert-base-multilingual-cased`
- Initial `max_length`: `64`
- Decision status: provisional and measurable
- Re-evaluation trigger: frozen project dataset and downstream task metrics

Known limitation:

The current tokenizer measurements use a small educational corpus. Fertility and truncation do not, by themselves, establish downstream model quality.

### Lab 1 — Distinction evidence

- Arabic clitic probe `وبالخدمة`: `DISTINCTION_CLITIC_TEST=PASS`
- mBERT/AraBERT measured tokenizer comparison: `DISTINCTION_TOKENIZER_COMPARISON=PASS`
- Three-seed toy embedding experiment: `DISTINCTION_THREE_SEEDS=PASS`

---

## Lab 2 — Attention & Transformers

- Scaled dot-product attention: `PASS`
- Attention row sums: `PASS`
- Keep-mask behaviour: `PASS`
- Multi-head split/combine round trip: `PASS`
- Encoder layer CPU execution: `PASS`
- BERT-family checkpoint architecture inspection: completed
- Arabic and English forward passes: completed
- Token-labelled attention visualisation: completed
- Notebook core marker: `DAY1_NOTEBOOK2_CORE=PASS`
- Official attention tests: `3 passed in 0.14s`

### Lab 2 — Distinction evidence

NumPy and PyTorch mask semantics were compared using the same causal keep-mask.

Measured maximum difference between outputs:

`4.441e-16`

Observed semantics:

- `True` = key participates in attention
- `False` = key is masked
- Masked attention positions received zero probability
- NumPy and PyTorch outputs matched within floating-point precision

Marker:

`DISTINCTION_MASK_SEMANTICS=PASS`

---

## Runtime/run-all evidence

| Notebook | Clean run date | Core marker | Colab/GitHub link |
|---|---|---|---|
| 00 | Not run separately | runtime checks | — |
| 01 | 2026-08-30 | `DAY1_NOTEBOOK1_CORE=PASS` | https://github.com/Yousef0197/sda_nlp-bayan-capstone/blob/main/notebooks/01_text_processing_tokenization.ipynb |
| 02 | 2026-08-30 | `DAY1_NOTEBOOK2_CORE=PASS` | https://github.com/Yousef0197/sda_nlp-bayan-capstone/blob/main/notebooks/02_attention_transformers.ipynb |
| 03 | — | not run | — |
| 04 | — | not run | — |
| 05 | — | not run | — |
| 06 | — | not run | — |
| 07 | — | not run | — |
| 08 | — | not run | — |

---

## Gate A conclusion

Gate A requirements completed on 2026-08-30.

Evidence includes:

- passing preprocessing and tokenisation tests;
- passing attention tests;
- executed notebooks 01 and 02 with visible Core markers;
- measured bilingual tokenizer comparison;
- documented tokenizer and sequence-length decision;
- Distinction evidence for Arabic clitics, repeated embedding seeds, and NumPy/PyTorch mask semantics;
- no real personal data, model weights, or authentication secrets introduced during the Day 1 experiments.

The next project stage is Gate B.

---

## Final release

- Final commit: not created yet
- Release/tag `submission-v1.0`: not created yet
- Validator pre-tag report: not run yet
- Validator `--require-tag` report: not run yet
- Private-window visibility check: not performed yet
- Remaining limitation: Gates B–E and final project evaluation remain incomplete