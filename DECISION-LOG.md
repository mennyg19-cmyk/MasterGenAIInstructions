# Decision Log

Decisions for MasterGenAIInstructions. Newest first.

---

## 2026-10-13 Composer orchestrator + Grok/Claude post-OpenAI
**What I had to decide:** Default models after Cursor OpenAI wind-down (~Nov 2026) and expensive review loops.
**Options I considered:** (A) Composer-pool only; (B) Composer parent + Grok/Sonnet/Opus hybrid; (C) Claude-house default.
**What I chose:** **B** with UI default **Composer 2.5 Standard**; Everyday implement/Loop A = Grok 4.7; Loop B = Sonnet 5.5; Premier = Opus 5.5; walkthrough hard-locked to Composer; routine Loop C optional; Task prompt templates for handoffs. Fable dropped from defaults.
**Why:** Composer is the cheap conversational parent; Grok burns included Cursor pool for build; Claude Other pool only when dual-family/premier needed.
**Status:** DECIDED
