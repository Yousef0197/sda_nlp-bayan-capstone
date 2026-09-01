# T9 Manual Error Review — 108 Reviewed Errors

**Repository:** `Yousef0197/sda_nlp-bayan-capstone`  
**Review date:** 2026-09-01  
**Training context:** Bayan — **#SDAIA**

## Scope

This report records a row-by-row semantic review of **108 actual baseline retrieval errors** produced from the Bayan synthetic educational retrieval suite.

The review set was built from:

- `10` canonical bilingual retrieval intents from `notebooks/bayan_capstone.ipynb`.
- `12` distinct, meaning-preserving modifiers per intent.
- `120` distinct validation-style perturbation cases in total.
- `108` cases where the lexical/hash baseline returned the wrong Top-1 document.

The relevant document, baseline Top-1, improved Top-1, and review category are preserved in:

`reports/t9_manual_error_review.csv`

## Reviewer boundary

**Reviewer:** GPT-5.6 Sol (AI assistant)  
**Method:** row-by-row semantic review  
**Human-reviewed claim:** **NO**

The rows were reviewed individually for semantic relevance and failure mechanism. This is an AI-assisted manual review and is **not represented as independent human review**. If the academy rubric specifically requires a human reviewer, the learner or instructor must confirm or spot-check the rows before claiming that stricter condition.

## Reviewed error count

- Baseline errors reviewed: **108**
- Minimum target represented by this report: **>=100 errors**
- Improved system correct on reviewed baseline errors: **106/108**
- Improved-system residual errors: **2**
- Improved correction rate over these baseline errors: **98.148%**

## Manual categories

| Category | Count | Interpretation |
|---|---:|---|
| `cross_language_intent_specificity_gap` | 56 | Baseline preferred a same-topic generic document over the action-specific cross-language target. |
| `hash_collision_candidate_ordering` | 44 | Hashed lexical representation promoted a semantically unrelated or materially less relevant candidate. |
| `modifier_noise_ranking_instability` | 8 | A meaning-preserving modifier changed the wrong Top-1 candidate, exposing ranking instability. |

### Residual improved-system errors

Two reviewed cases remain incorrect after the improved retrieval/reranking path:

- `Q10-M04` — `How do I register for the course? for me`
- `Q10-M07` — `How do I register for the course? via mobile`

Both are residual candidate-ordering failures because the improved path returns `D05` instead of the relevant `D10`.

## Prioritized fixes

1. **Keep bilingual concept canonicalization before embedding.**  
   It directly addresses the dominant cross-language intent/specificity gap.

2. **Replace or strengthen the hashed lexical candidate representation.**  
   A trained multilingual embedding model or stronger candidate encoder should reduce unrelated hash-collision ranking errors.

3. **Harden reranking against low-information modifiers.**  
   Down-weight politeness, channel, and time modifiers and emphasize action-intent concepts so phrases such as `for me` or `via mobile` do not distort Top-1 ordering.

## Evidence interpretation

This review strengthens the project's T9 error-analysis evidence, but the underlying corpus remains a **synthetic educational suite**. It does not replace any academy-frozen evaluation package that may be supplied separately.

The reviewed rows are deliberately preserved with the source query, relevant document ID, baseline Top-1, improved Top-1, manual semantic category, and improved-error flag.

## Status

`T9_AI_ASSISTED_ROW_BY_ROW_ERROR_REVIEW_108=COMPLETE`

`T9_REVIEWED_ERROR_COUNT_GE_100=PASS`

`T9_HUMAN_REVIEW_CLAIM=FALSE`

**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
