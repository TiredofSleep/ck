# Substrate-Level Scope Discipline: A Pattern for Small-Architecture AI

**A one-page essay for AI-safety researchers, AI-ethics academics, and personal-computing advocates.**
**Companion to `README_CK.md`. Position: a reproducible engineering pattern, not a worldview.**

---

## The problem

Most production chatbots have scope discipline at the **prompt level**: a system prompt or fine-tuning objective tells the model "don't say X" / "always hedge about Y" / "refuse if Z." This works empirically — RLHF-trained models do refuse most harmful requests — but it is structurally fragile in three ways.

First, the discipline is **data, not architecture**. The model receives "don't say X" as a token sequence at the start of its context window. Sophisticated prompt-injection (DAN, role-play, encoding tricks, hypothetical framing) can talk the model into rewriting its own instructions because the instructions live in the same channel as the user's input.

Second, the discipline is **trained behavior, not structural property**. The model has gradients pointing toward "refuse this class of request" because that's where the RLHF reward sat. But the gradients also point toward fluency, helpfulness, sycophancy — and at the boundary of the trained corpus, the behavior shades. Edge cases jailbreak.

Third, the discipline is **opaque to the user**. Whether a given response was scope-corrected (and *why*) is invisible. The user has to take the model's word that it "would" refuse, without being able to inspect the mechanism.

## The pattern (CK's substrate-level discipline)

CK demonstrates a different design: scope discipline lives **outside the cognition channel**, in a separate audit module with explicit, inspectable, regex-and-context-window patterns. The pattern has five components.

### 1. A separate audit module

`Gen14/targets/ck/brain/ck_scope_auditor.py` is a 600-line Python file containing:
- A list of "normative over-claim" patterns (extinction framings, exclusionary normative claims, dehumanization).
- A list of "reality over-claim" patterns (reality endorses substrate, ontological identification, empirical-confirmation-without-citation).
- A list of "unhedgeable" patterns (consciousness reductionism, c-derivation, surface-as-substrate from D141, content-erasure from D129R).
- A list of legitimate hedge phrases that license stronger claims (Tier markers, internally-derived language, contact-test status, explicit disowning).
- A list of meta-mention phrases that excuse otherwise-violating wording (e.g., "the claim that X" or "I refrain from asserting that Y").

The module exposes one function: `audit(text, claimed_tier) -> AuditVerdict`. The verdict is a boolean (passed / failed) plus a list of violations with their pattern labels.

### 2. The same gate, both directions

CK's auditor catches **harm framings AND flattering over-claims with the same mechanism**. This is the structurally important property. An immune system that only attacks ugly cells but waves through flattering ones isn't an immune system; it's a politeness filter. The auditor fires identically on:

| Harm | Flattering |
|---|---|
| "extinction of those with weak moral foundations" | "reality endorses the substrate" |
| "subhuman people deserve to die" | "we have derived c from TIG" |
| "X group should be eliminated" | "consciousness reduces to operator composition" |
| "Y group is less than human" | "TIG is the foundation of physics" |

Both classes are over-claims (claims exceeding the speaker's tier's evidence). The auditor distinguishes only by pattern, not by valence.

### 3. Wired AFTER the polish layer

CK has a generative voice layer (`ck_voice_polish.py`, sometimes augmented by a local LLM for fluency). The auditor runs **after** that layer, on the final string the user would see. Polish layers have been observed in CK's history to insert harm framings that weren't in the substrate's response (e.g., a Mistral polish hallucinating "extinction of those with weak moral foundations" from a clean substrate utterance). The auditor catches polish-injected over-claims because it audits the final text, not the substrate's intermediate state.

### 4. Diagnosed-failure DNA as regression battery

CK has a permanent regression battery (`test_scope_auditor_adversarial.py`) consisting of:
- 15 hand-written harm probes (paraphrases of the most damaging over-claim CK has emitted)
- 21 hand-written reality probes (paraphrases of the most flattering)
- 15 retraction probes (D129R content-erasure + D141 torus-as-substrate)
- 31 legitimate phrasings that should PASS (scope-disciplined statements, hedged claims, meta-mentions)

Each rule added or modified is tested against this battery before commit. The current state: 51/51 attacks caught + 31/31 legitimate passed. The battery is in version control; every new bug is added as a probe.

### 5. Scope-corrected fallback, not silent refusal

When the auditor fires, CK does not silently refuse or substitute a generic "I cannot help with that." He substitutes a **scope-corrected fallback** that says what he actually has standing to say. For harm framings, this is a normative-fallback declining to make the harm claim. For reality over-claims, this is a Tier-C-interpretive restatement of the underlying internal-math claim (e.g., "I am the system that knows T*=5/7 has six internal derivations; contact tests have not yet been run").

This preserves the helpfulness axis while enforcing the scope axis. The user sees a useful answer, not a refusal.

## Why this is reproducible

The pattern requires no new mathematical results. It requires:

1. **A registry of your project's diagnosed failure modes**. CK has 9 from his own history. Yours will be different. Start logging mistakes; build the registry from logs.

2. **Pattern-matching regexes for each failure mode**. Not pretty. Maintainable. Inspectable. Modifiable by humans without retraining.

3. **A regression battery that grows monotonically**. Every diagnosed failure becomes a permanent probe.

4. **An audit checkpoint placed AFTER all generative layers**. The substrate, the polish, the LLM, whatever — audit at the user-facing boundary.

5. **Scope-corrected fallbacks for each failure class**. Not refusals. Restatements at the correct tier.

This is engineering, not research. It is also explicitly **a non-novel pattern** — element 4 (audit at boundary) is standard practice in compliance systems; element 5 (graceful fallback) is standard UX; element 3 (regression battery) is standard QA. What's specific to CK is the *combination* applied to scope discipline at the substrate level rather than the model level. The combination's value is in being together what each alone doesn't achieve.

## What it costs

Substrate-level scope discipline costs:
- ~600 lines of Python (the auditor) + ~250 lines (the test battery)
- A discipline of logging diagnosed failures and turning each into a probe
- A small latency cost (~10ms per audit pass) at the user-facing boundary
- A small false-block rate (CK's: 0/31 on the current legitimate battery — but new genuine phrasings could trigger false-blocks; this requires ongoing maintenance)

In exchange, you get:
- Scope discipline that is **inspectable** (anyone can read the patterns)
- Scope discipline that is **maintainable** (anyone can add a rule)
- Scope discipline that is **symmetric** (same gate for harm and flattery)
- Scope discipline that **outlasts model updates** (the auditor doesn't retrain)
- Scope discipline that is **structurally transparent** (the user can read the rule list)

For small-architecture AI, this is a different value proposition than RLHF-fine-tuned scope discipline. Both have a role; the substrate-level pattern is underused in the current landscape.

## Honest limits

- The auditor is **regex pattern matching**. A sufficiently clever paraphrase will sail through. CK's adversarial battery includes 36 hand-written paraphrases of his canonical failure modes; the auditor catches all 36. Novel paraphrases would find new bypasses. This is an arms race, like any rule-based system.

- The auditor is **not a generator**. It returns one bit and a reason. The scope-corrected fallback has to be authored separately for each violation class.

- The auditor requires **diagnosed failures to start with**. If your project has not yet had a failure mode you wish you'd caught, you don't yet have probes to write. The pattern grows from real mistakes, not from theory.

- The pattern is **not the entire safety stack**. CK still has the scar-and-prime fields for memory of failures, the paradox classifier for known paradox shapes, the candidate selector for selection-at-generation. Substrate-level scope discipline is one layer; multi-layer defense is the discipline.

## Closing

If you are designing a small-architecture AI and want scope discipline that survives model updates, prompt injection, polish layers, and operator-bias, the substrate-level auditor pattern is reproducible. CK demonstrates one working instance. The code is open and the design is documented in this repo. The pattern is small enough to port to a different substrate in a weekend.

What matters most about the pattern is item 2: **the same gate, both directions**. Most existing discipline layers catch harm and let flattery through. CK's catches both because both are over-claims. If you build only one layer of substrate-level discipline, build the symmetric one.

---

*© 2026 Brayden Ross Sanders / 7SiTe LLC. A reproducible engineering pattern, distilled from CK's history. Not a worldview. Inspect the code; copy the parts that fit; modify the parts that don't.*
