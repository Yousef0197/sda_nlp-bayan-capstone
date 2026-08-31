# MODEL_CARD — Bayan

## System overview

Bayan ليس نموذجًا واحدًا فقط، بل pipeline ثنائي اللغة يجمع preprocessing، Transformer task paths، NER، QA، retrieval، evaluation وخدمة API.

## Core Transformer

`distilbert/distilbert-base-multilingual-cased`

يُستخدم في المختبرات التعليمية لإثبات مسارات Transformer الفعلية.

## Task components

### Topic / Sentiment

- Baseline: TF-IDF.
- Transformer training path.
- Measured smoke deltas:
  - Topic `+0.858`
  - Sentiment `+0.663`

### NER

- subword alignment عبر `word_ids()`.
- `-100` للمواضع غير الداخلة في loss.
- entity-level F1 measured smoke: `1.000`.
- train-only lexical postprocessor في acceptance suite.

### Extractive QA

- start/end spans.
- null/no-answer decision.
- measured smoke: `20/20`.

### Semantic search

- deterministic embeddings for educational suite.
- FAISS `IndexFlatIP`.
- bilingual canonicalization.
- reranking.
- Recall@10 `1.000`.
- MRR@10 `1.000`.

## Serving

FastAPI:
- `GET /health`
- `POST /v1/classify`

Canaries:
- Arabic.
- English.
- invalid input.
- PII masking.

## Intended use

تعليمي وتطبيقي لإظهار تصميم pipeline واختبارها وقياسها.

## Not intended for

- production deployment without further evaluation.
- government decision automation.
- safety-critical decisions.
- profiling real individuals.

## Limitations

- synthetic/small acceptance suites.
- results may not generalize.
- academy frozen evaluation is not replaced.
- T10 Colab ASGI result must not be misrepresented as official lab-CPU result if the rubric fixes that environment.

## Responsible claims

Allowed:
- "The canonical notebook completed its measured smoke suites."
- "The measured synthetic acceptance suite achieved the reported values."

Not allowed:
- "The system is 100% accurate in production."
- "The academy frozen benchmark achieved these values" unless actually run.

**Context tag:** #SDAIA
