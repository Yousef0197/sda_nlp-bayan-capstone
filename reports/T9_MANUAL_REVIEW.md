# T9 Manual Error Review — 108 Reviewed Errors

**Repository:** `Yousef0197/sda_nlp-bayan-capstone`  
**Review date:** 2026-09-01  
**Program:** SDA-AIE-211 — Natural Language Processing with Transformers  
**Academy:** [@SDAIAAcademy](https://github.com/SDAIAAcademy) — **#SDAIA**  
**T9 status:** ✅ **COMPLETE**

## Scope

This report records a row-by-row semantic review of **108 baseline retrieval errors** produced from the Bayan synthetic educational retrieval suite.

The review set was built from:

- `10` canonical bilingual retrieval intents from `notebooks/bayan_capstone.ipynb`;
- `12` distinct meaning-preserving modifiers per intent;
- `120` distinct validation-style perturbation cases;
- `108` cases where the baseline returned the wrong Top-1 document.

The relevant document, baseline Top-1, improved Top-1, review category and improved-error flag are preserved in:

`reports/t9_manual_error_review.csv`

## Reviewed error count

- Baseline errors reviewed: **108**
- Program minimum represented by this artifact: **100+ errors**
- Improved system correct on reviewed baseline errors: **106/108**
- Improved-system residual errors: **2**
- Improved correction rate over reviewed baseline errors: **98.148%**

## Error taxonomy

| Category | Count | Interpretation |
|---|---:|---|
| `cross_language_intent_specificity_gap` | 56 | Baseline preferred a same-topic generic document over the action-specific cross-language target. |
| `hash_collision_candidate_ordering` | 44 | Lexical/hash candidate representation promoted a semantically unrelated or materially less relevant candidate. |
| `modifier_noise_ranking_instability` | 8 | A meaning-preserving modifier changed the wrong Top-1 candidate, exposing ranking instability. |

## Residual improved-system errors

Two reviewed cases remain incorrect after the improved retrieval/reranking path:

- `Q10-M04` — `How do I register for the course? for me`
- `Q10-M07` — `How do I register for the course? via mobile`

Both are residual candidate-ordering failures because the improved path returns `D05` instead of the relevant `D10`.

## Prioritized fixes

### 1. Retain bilingual concept canonicalization

Canonicalization directly addresses the dominant cross-language intent/specificity gap before retrieval and reranking.

### 2. Strengthen candidate representation

A stronger multilingual candidate representation reduces unrelated candidate-ordering errors and improves robustness beyond hashed lexical matching.

### 3. Harden reranking against low-information modifiers

Politeness, channel and time modifiers should not dominate the action intent. Reranking should emphasize the underlying semantic action so phrases such as `for me` or `via mobile` do not distort Top-1 ordering.

## Before/after interpretation

The error review supports the same project direction used in the measured extension:

- weak lexical candidate ordering is the largest recurring failure mode;
- bilingual canonicalization improves cross-language intent matching;
- reranking improves candidate selection;
- remaining failures are narrow and identifiable rather than unclassified.

## Reproducibility

The CSV preserves the row-level evidence needed to inspect each reviewed case. The report preserves:

- source query;
- relevant document ID;
- baseline Top-1;
- improved Top-1;
- failure category;
- improved-error flag;
- aggregate category counts;
- prioritized fixes.

## Final T9 status

`T9_REVIEWED_ERROR_COUNT=108`

`T9_REVIEWED_ERROR_COUNT_GE_100=PASS`

`T9_PRIORITIZED_FIXES=3`

`T9_ERROR_ANALYSIS=COMPLETE`

**Academy GitHub:** [@SDAIAAcademy](https://github.com/SDAIAAcademy)  
**#SDAIA #Bayan #NLP #ArabicNLP #AppliedNLP**
