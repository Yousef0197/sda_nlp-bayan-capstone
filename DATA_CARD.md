# DATA_CARD — Bayan

**Project:** Bayan — Bilingual Applied NLP Capstone  
**Program:** SDA-AIE-211 — Natural Language Processing with Transformers  
**Academy:** [@SDAIAAcademy](https://github.com/SDAIAAcademy) — **#SDAIA**  
**Data card status:** ✅ **COMPLETE**

## Data purpose

تدعم بيانات **Bayan** خط معالجة ثنائي اللغة بالعربية والإنجليزية يشمل:

- text preprocessing and PII masking;
- topic and sentiment classification;
- Named Entity Recognition;
- extractive Question Answering;
- semantic search and reranking;
- sliced and behavioural evaluation;
- error analysis and API canaries.

البيانات مخصصة للتعلم والتقييم القابل لإعادة الإنتاج، وليست بيانات مستفيدين حقيقية أو مجموعة إنتاجية.

## Source and provenance

**Source:** synthetic educational fixtures supplied for the Bayan course workflow and preserved under `data/sample/` in this repository.  
**Data type:** synthetic educational data.  
**Languages:** Arabic and English.  
**External third-party dataset:** none.  
**Sensitive real-user data:** none intentionally included.  
**Repository snapshot reviewed:** 2026-09-01.

### Usage and licensing scope

The dataset files are course-provided synthetic educational material used for the **SDA-AIE-211** learning and assessment workflow. No separate third-party dataset licence is asserted because no external dataset is redistributed by this project. Reuse outside the course/repository context should follow the applicable course and repository permissions.

## File inventory

| File | Records / examples | Purpose |
|---|---:|---|
| `data/sample/bayan_day1_sample.csv` | `12` | bilingual preprocessing/tokenization sample |
| `data/sample/bayan_day2_classification.csv` | `40` | topic + sentiment classification and grouped splits |
| `data/sample/bayan_day2_ner.jsonl` | `12` sentences | BIO labels and subword-alignment experiments |
| `data/sample/bayan_day2_qa.json` | `10` questions | extractive QA including no-answer cases |
| `data/sample/bayan_day3_arabic.csv` | `20` | Arabic profiles, MSA/Gulf/Arabizi and channel variation |
| `data/sample/bayan_day3_cases.csv` | `24` cases | bilingual semantic-search corpus |
| `data/sample/bayan_day3_queries.jsonl` | `18` queries | validation/test retrieval relevance cases |
| `data/sample/bayan_day3_predictions.csv` | `36` predictions | sliced evaluation, Macro-F1, confidence and paired comparisons |

A more granular day-by-day description is preserved in `data/DATA_CARD.md`.

## Schema

### Day 1 sample

`bayan_day1_sample.csv`

| Field | Meaning |
|---|---|
| `case_id` | synthetic case identifier |
| `language` | `ar` or `en` |
| `text` | synthetic text |
| `topic` | educational topic label |

### Day 2 classification

`bayan_day2_classification.csv`

| Field | Meaning |
|---|---|
| `example_id` | synthetic example identifier |
| `group_id` | grouping key used to reduce near-duplicate leakage |
| `split` | train / validation / test assignment |
| `language` | Arabic or English |
| `text` | synthetic input text |
| `topic` | topic label |
| `sentiment` | sentiment label |

### Day 2 NER

`bayan_day2_ner.jsonl`

Each record contains:

- `split`;
- `language`;
- `tokens`;
- `ner_tags` using BIO-style entity labels.

### Day 2 QA

`bayan_day2_qa.json`

Each example contains:

- `id`;
- `split`;
- `language`;
- `context`;
- `question`;
- `answer_text`;
- `answer_start`.

The file is explicitly marked `synthetic: true`.

### Day 3 Arabic profiles

`bayan_day3_arabic.csv`

Fields:

`record_id, language, variant, channel, topic, text`

The `variant` field is an educational annotation for profile analysis; it is not presented as an output from a production dialect classifier.

### Day 3 retrieval corpus

`bayan_day3_cases.csv`

Fields:

`case_id, language, variant, topic, summary, resolution`

### Day 3 retrieval queries

`bayan_day3_queries.jsonl`

Each query contains:

- `query_id`;
- `split`;
- `query`;
- `language`;
- `retrieval_mode`;
- `relevant_case_ids`.

The retrieval set includes both monolingual and cross-lingual relevance cases.

### Day 3 evaluation predictions

`bayan_day3_predictions.csv`

Fields:

`example_id, split, language, variant, length_bucket, topic, prediction_a, prediction_b, text`

These fields support language/variant/length slices and paired comparisons.

## Split and leakage policy

Where task data uses train/validation/test splits, the project keeps the roles separate:

- **Train:** fit model parameters.
- **Validation:** model/epoch/threshold decisions and development checks.
- **Test:** final held-out evaluation only.

For the classification fixture, `group_id` is used to keep related examples together and reduce leakage across splits. Retrieval query files also carry explicit `split` values. Test data is not used for repeated model or threshold selection.

## Privacy and integrity

The project uses synthetic educational records and intentionally excludes real citizen/customer data.

Privacy and repository controls include:

- synthetic email/phone examples only for PII masking canaries;
- email and phone masking tests;
- no `.env` file;
- no API keys or credentials;
- no real names, identity numbers, private complaints or institutional secrets;
- no committed model weights, checkpoints or large ONNX artefacts;
- reusable preprocessing and PII tests under `tests/`.

## Evaluation coverage

The dataset package supports measurement of:

- Macro-F1 and baseline deltas;
- entity-level NER F1;
- QA span/no-answer behaviour;
- Recall@10 and MRR@10;
- Arabic/English and other documented slices;
- confidence intervals and paired comparisons;
- invariance and Minimum Functionality Tests;
- error analysis;
- API canaries and benchmark workloads.

## Recorded project results

| Area | Result |
|---|---:|
| Topic Macro-F1 delta vs baseline | `+0.858` |
| Sentiment Macro-F1 delta vs baseline | `+0.663` |
| NER entity-level F1 | `1.000` |
| QA no-answer | `20/20` |
| Recall@10 | `1.000` |
| MRR@10 | `1.000` |
| Invariance | `1.000` |
| MFT | `1.000` |

The metrics are interpreted together with the exact notebook/report and runtime that produced them rather than as universal production-quality estimates.

## Limitations

1. The datasets are deliberately small and synthetic.
2. They do not represent the full dialect, domain, demographic or temporal distribution of real Saudi service text.
3. Small training/evaluation sets can produce high variance between runs.
4. Synthetic performance does not establish production accuracy.
5. Any production use would require governed representative data, refreshed privacy review, distribution-shift monitoring and task-specific validation.

## Final status

**Source/provenance:** ✅ COMPLETE  
**File inventory and fields:** ✅ COMPLETE  
**Split/leakage policy:** ✅ COMPLETE  
**Privacy controls:** ✅ COMPLETE  
**Evaluation coverage:** ✅ COMPLETE  
**Limitations:** ✅ COMPLETE  
**DATA CARD:** ✅ COMPLETE

**Academy GitHub:** [@SDAIAAcademy](https://github.com/SDAIAAcademy)  
**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
