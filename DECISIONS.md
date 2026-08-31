# DECISIONS — Bayan

يوثّق هذا الملف القرارات الهندسية المرتبطة بالبيانات والنماذج والبحث والتقييم والخدمة.

## D-001 — Bilingual preprocessing

**Decision:** الحفاظ على مسار موحّد train/eval/serve، مع Unicode normalization، إزالة الكشيدة والتشكيل المستخدم في profile، توحيد صور الألف/الياء حيث يفرضه profile، وضبط المسافات وPII masking.

**Why:** منع drift بين التدريب والتقييم والخدمة، وتحسين invariance في العربية.

**Risk:** التطبيع المفرط قد يحذف فروقًا لغوية نافعة في بيانات واقعية.

## D-002 — Canonical notebook

**Decision:** `notebooks/bayan_capstone.ipynb` هو المرجع الرئيسي للتشغيل النهائي، بينما تبقى الدفاتر التاريخية دليلًا على تطور المشروع.

**Why:** تقليل تعارضات البيئة وتوفير Clean Run واحد Day 1–Day 4.

## D-003 — Task baseline and Transformer

**Decision:** الاحتفاظ بـTF-IDF baseline ثم مقارنة مسار Transformer عليه.

**Measured smoke:**
- Topic delta: `+0.858`
- Sentiment delta: `+0.663`

**Boundary:** النتيجة على acceptance suites اصطناعية ولا تعني production quality.

## D-004 — NER alignment

**Decision:** استخدام `word_ids()` وتعيين `-100` للـspecial tokens والـcontinuation subwords.

**Measured smoke:** entity-F1 `1.000`.

**Additional decision:** postprocessing lexicon مبني من Train فقط؛ لا تدخل labels من Validation/Test في القاموس.

## D-005 — QA no-answer

**Decision:** استخدام null/CLS score مع constrained valid span.

**Measured smoke:** `20/20` no-answer cases.

**Boundary:** اختبار تعليمي اصطناعي، وليس بديلًا عن Frozen QA set رسمي.

## D-006 — Semantic retrieval

**Decision:** FAISS candidate retrieval + bilingual concept canonicalization + reranking.

**Measured smoke:**
- Recall@10 `1.000`
- MRR@10 `1.000`

**Reason:** مسار baseline lexical وحده أضعف في cross-language matching.

## D-007 — Behavioural evaluation

**Decision:** قياس Invariance وMFT صراحة وعدم الاكتفاء بالمقاييس التقليدية.

**Measured smoke:**
- Invariance `1.000`
- MFT `1.000`

## D-008 — Error analysis

**Decision:** توليد جدول من 100 حالة للمراجعة مع taxonomy أولية و3 إصلاحات مرتبة.

**Boundary:** التصنيف الآلي لا يُقدّم على أنه مراجعة بشرية. يتم اعتماد manual review منفصل إذا كان شرط T9 حرفيًا.

## D-009 — Serving path

**Decision:** FastAPI مع `/health` و`/v1/classify`، ودعم ar/en وinvalid input وPII canary.

## D-010 — Performance budget

**Target:** HTTP p99 ≤ 40ms at concurrency 16.

**Measured:** `32.907 ms` في Colab باستخدام FastAPI + ASGI transport.

**Decision:** لا نعتبر هذا دليل lab-CPU نهائيًا إذا كان rubric يفرض CPU محددًا؛ يعاد القياس على البيئة الرسمية قبل release.

## D-011 — Measured extension

**Extension:** bilingual concept canonicalization + reranking.

**Before/after delta:** `+0.88` Top-1.

**Decision:** `KEEP`.

## D-012 — ONNX/INT8

**Decision:** `NOT ADOPTED IN FINAL PATH`.

**Reason:** لا يوجد في الـcanonical clean run قياس before/after موثق للجودة والlatency والحجم يبرر التحويل. عدم الادعاء أفضل من إضافة optimisation غير مقاس.

## D-013 — Release evidence

لا يتم إنشاء `submission-v1.0` إلا بعد:
- validator،
- T9 manual review عند الحاجة،
- T10 official-environment check عند الحاجة،
- presentation،
- public/private-window verification.

**Training context tag:** #SDAIA
