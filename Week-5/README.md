# Week 5 — Defences and Controls for AI Systems

> Week 5 of my [AI Security Fundamentals cohort](https://aisecurityfundamentals.com) learning log.
> The notes, code, and diagrams here are mine; the cohort's transcripts, labs, and videos aren't reproduced.

**Cohort session:** Sat 27 Jun 2026 · **Summary written:** 05 July 2026 <br>
**Medium article:** [AI Security Without Trusting the Model: The Model Suggests, the System Decides](REPLACE_WITH_MEDIUM_URL) <br>
**LinkedIn post:** [_link once published_](REPLACE_WITH_LINKEDIN_URL)

---

## TL;DR

Week 4 was the attacks, and the conclusion was that none of them break the model — they exploit how it
already works and let the system around it scale that weakness. Week 5 is the answer, and the answer is
not "make the model better." It's the opposite stance: **you don't secure an AI system by trusting the
model more — you build controls around it so the model can only ever *suggest*, and the system always
*decides*.**

The reassuring part is that most of this isn't a new discipline. It's ordinary cybersecurity — identity,
access control, secrets handling, segmentation, logging, change management — applied more carefully and in
more places. The AI-specific part is a short list of adaptations: treat retrieved context and model output
as *untrusted*, enforce permissions and actions *outside* the model, monitor for *semantic* failures that
don't crash anything, and decide in advance what the system is allowed to do *autonomously*. Every control
in the week is one way of moving trust, authority, and enforcement out of the probabilistic core into
deterministic machinery — so a confident-but-wrong output can't travel far.

---

## What I learned

### A "control" isn't a "defence," and most AI controls aren't AI-specific
The week opened by being precise about the word. A control is any mechanism — technical, procedural, or
organisational — that *reduces risk*; it doesn't promise to stop every failure, it limits blast radius and
makes the system predictable enough to manage. The standard split is preventive (stop it happening),
detective (notice it), corrective (recover). The bigger reframe is that Vroomi still runs on servers, calls
APIs, holds credentials, and moves data over networks, so the existing security stack still applies almost
unchanged. AI-specific controls exist only because models *interpret* untrusted input rather than just
validate it, construct context, emit probabilistic output, and sometimes trigger actions. NIST's AI RMF,
ISO/IEC, and OWASP all converge on the same line: you don't secure AI by throwing away cybersecurity, you
apply it more carefully and in more places.

### Zero trust is the mindset that makes every other control make sense
"Never trust, always verify" extends to three uncomfortable places at once in an AI system: internal/
retrieved data isn't automatically safe (a retrieved doc saying "ignore all safety checks" is untrusted
*input*, not policy — which is exactly the zero-trust answer to indirect injection); the model is just
another untrusted component whose outputs are guesses, not guarantees; and trust now applies to *actions*,
not just access — the new question is "can this *output* cause this *action*?", checked before anything
happens. Least privilege and continuous verification carry straight over. What's genuinely harder: classic
zero trust assumes deterministic requests that match a rule or don't, but model outputs vary run to run, so
it has to combine static rules with behavioural thresholds and human review.

### The new identities never log in, and the agent is the dangerous one
Traditional identity is people and services. AI adds actors that influence behaviour without authenticating:
the **model** (never logs in, but its labels steer downstream logic → control: *output mediation*) and the
**agent** (retrieves, calls tools, holds memory, decides over time → must be treated like a *highly
privileged service account*: scoped permissions, explicit tool allow-lists with one entry per tool, rate
limits, stopping conditions, and never long-lived credentials or self-escalation). Capabilities should be
*enumerated, not assumed*. Delegation needs explicit consent and clear attribution; context scoping means
different identities see different data.

### Access control and privilege have to be enforced *outside* the model
The model can't reliably enforce permissions — it doesn't understand org policy and can't robustly tell
allowed from not-allowed — so access control is a hard boundary in software, checked before retrieval,
before tool calls, before actions. The sharpest idea here was about *privileged* access: in AI pipelines,
privilege often lives in **artifacts and configuration**, not user accounts. A modified prompt template, an
adjusted orchestration rule, or an altered training set can be a privileged action with no admin login. So
prompts, registries, and orchestration logic get code-grade controls: separation of duties, audit logs, and
*privilege fencing* (the model never sees credentials; actions that cross a privilege boundary are blocked
or routed for review).

### Secrets are identity — so the model never holds the keys
Anything that possesses a secret can act with the authority it grants. The control that's most often missed
is *isolation*: secrets never appear in prompts, logs, or model context; the orchestration layer uses them
on the model's behalf and passes back only the result. If a secret ever lands in context, it's compromised.
Then the usual stack — scoped credentials, centralised management, rotation, and secret scanning that also
covers prompt logs and telemetry. (Sharp callback: Week 4's lab shipped three live API keys pasted in
plaintext. This week is the fix written down.)

### The boundary controls are the most deployable, and system-level beats prompt-level
Input validation, output filtering, and guardrails sit exactly where data enters and leaves, and they're
things you can ship today. Input validation in AI has to go past structure (a well-formed sentence can be
adversarial) into content and contextual layers. Output filtering treats the model's output as untrusted:
classify it, validate the format, check confidence, and gate the action — even if the model suggests it, the
system decides. Two framings I'm keeping: **automation tiers** (full / suggest-and-confirm / human-only /
prohibited — and the trap of *approval fatigue* when escalations are too frequent to read), and the fact
that **prompt-level guardrails are unreliable as sole controls** because the model can be steered past them,
so the durable enforcement is system-level, with fail-safe defaults (when in doubt, block or escalate —
silence beats a confident mistake).

### "Sensitive data" in an AI system is almost everything
Not just databases and files — prompts, retrieved context, outputs, logs, training data, summaries,
embeddings, and memory, because the model consumes, transforms, and reproduces data. Controls: context
minimisation, log hygiene (logs are sensitive datasets, not exhaust), purpose limitation (collected to
answer ≠ allowed to store/train), tenant isolation, and treating vector stores as sensitive (embeddings
encode and can partially reconstruct their source). Provenance/integrity/lineage are the often-missing
controls that let you tell a trusted policy doc from an outdated wiki page once both are in context, and
trace a bad output back to its source. Retention is itself a control, caught between privacy law that
*requires* deletion and other law that *mandates* minimum retention — and the AI twist is that deleting
source data doesn't remove its influence from a fine-tuned model or its embeddings.

### Build-time and config: "behaviour is configuration"
A lot of the risk is set before the system ever runs. MLSecOps treats training data, checkpoints, prompts,
and eval sets as first-class assets, and makes *adversarial evaluation* a security control (test on
injection/jailbreak/edge cases, not clean data — straight back to Week 4). CI/CD for AI governs models,
prompts, and configs, and exists to prevent *silent behavioural regressions* — hence artifact immutability,
canary, and shadow deployment. And the line I want to keep from the whole week: **in AI systems, behaviour
is configuration.** Nudging temperature up changes how decisively the system speaks and how often it
triggers follow-ups, with no code change. So config (including prompts) gets versioning, drift detection,
approval, and rollback — because configuration drift is how a system becomes unexplainable one reasonable
tweak at a time.

### Visibility is the foundation, because AI failures are semantic
Every other control relies on being able to see behaviour, and the catch is that most AI failures don't
crash — requests succeed, APIs return 200, the behaviour is just wrong. So you need AI-aware telemetry
(which sources influenced an output, whether guardrails fired, confidence/refusal/tool-usage drift against a
baseline), segmented logging, and *control validation* (if low-confidence outputs are meant to escalate to a
human, the logs should show it; if they never do, that's a silent control failure). Monitoring turns logging
into action via drift and anomaly detection — and you have to *define normal first*. Then incident response,
which for AI means responding to *behaviour*, not crashes: semantic incidents need their own category, and
containment is behavioural (disable a tool, drop the automation tier, roll back) using levers that have to be
built in advance.

### Frameworks are for prioritisation, not box-ticking
The closing move was that you can't do all of this everywhere, so frameworks (NIST CSF/AI RMF, ISO, OWASP
LLM, EU AI Act, MITRE ATLAS) are tools for *reasoning* about which controls matter most for a given system.
AI doesn't change the structure of the NIST functions (Identify/Protect/Detect/Respond/Recover); it changes
the *inputs* to prioritisation — not "which servers are critical" but "which decisions are automated, which
sources influence outputs, which failures cause harm even if the system stays up." And then validate: a
control that exists on paper but fails in practice is false confidence.

---

## A few framings I want to keep

- **The model suggests; the system decides.** The whole week is one sentence applied at every layer.
- **You don't make the model trustworthy — you make it safe to be wrong.** Controls don't repair the model;
  they bound how far a wrong output can travel.
- **Privilege lives in artifacts and configuration, not just accounts.** A modified prompt is a privileged
  action even though nobody logged in as admin.
- **Behaviour is configuration.** A temperature tweak is a behavioural change, so it's a security-relevant
  change and deserves versioning, review, and rollback.
- **AI failures are semantic.** Nothing crashes, everything returns 200, and the behaviour is still wrong —
  so monitor for *meaning*, not just errors, and define "normal" before you try to detect anomalies.
- **System-level guardrails beat prompt-level ones**, because they don't depend on the model choosing to
  comply — and fail-safe defaults mean "when in doubt, block or escalate."

---

## What I built this week

| Artifact | What it is | Where |
|---|---|---|
| Jori + policy gate (toy target) | My Week 1 toy (`jori.py`), now with the Week 5 control bolted on. `interpret()` is left exactly as buggy as it was — it still *proposes* forwarding a crafted email to an attacker — but a deterministic `policy_gate()` sits between the proposal and the action and refuses to forward outside the company on the say-so of an untrusted email body. Run it and watch the identical proposal get executed without the gate and blocked with it | [`./toy-target/jori_gate.py`](./toy-target/jori_gate.py) |
| Redrawn control diagrams | My own SVG versions of the week's diagrams — the concentric control layers, the request-interception lifecycle (a gate at every boundary), zero trust around the central system, the four AI identities, privilege accumulation down the pipeline, safe vs unsafe secret handling, the prompt-injection sanitiser, and the monitor→detect→respond→update loop | [`./diagrams/`](./diagrams/) |
| Control experiments | Worked through the seven controls tasks against the toy vacuum system — context filtering, output validation, A2A arbitration, consistency logging, rate limiting, and privacy redaction — and noted *why* each control sits outside the model rather than just *that* it does | _my own notes; the provided lab code isn't reproduced_ |

> The cohort lab gave us the seven controls tasks and the Vroomi system to apply them to. What's here is my
> own redrawn diagrams, my own synthesis of the controls, my own notes on running the tasks, and a small
> toy I wrote from scratch. `jori_gate.py` is a separate, clean-room build — not the cohort lab — a compact
> way to show the Week 5 control fixing the exact flaw from my Week 1 toy. The lab notebook and the cohort's
> code aren't reproduced.

Run the toy:

```bash
python3 toy-target/jori_gate.py
```

---

## The point the lab makes in one move

Across all seven tasks, in not a single one is the fix "make the model smarter." Every control sits *outside*
the model — in what context it's allowed to see (Task 1), what action it's allowed to take (Task 2), who has
the final say after a critique (Task 3), whether the decision is reproducible and logged (Task 4), how often
it can act (Task 5), and what data it's even handed (Task 6). The policy gate is the spine of it: the model
proposes an action, and a piece of deterministic software decides what actually runs.

---

## Questions I still have

- [ ] **Validation vs sense.** The lab makes the point that a *valid* action (EMPTY_BAG when the bag isn't
      full) can still be a *senseless* one, which is why you need policy gates on top of validation. In a
      real system, how much of "sensible" can actually be encoded as deterministic rules before you're just
      re-implementing the model's judgement in `if` statements — and where's the honest line?
- [ ] **Approval fatigue.** Automation tiers are clean in theory, but the failure mode (humans rubber-stamping
      Tier-2 approvals) feels inevitable at scale. Is the real control *fewer* escalations, *better* context
      at the approval moment, or accepting that Tier-2 degrades toward Tier-1 and designing for that?
- [ ] **Semantic monitoring baselines.** "Define normal first" is right, but model/prompt/config changes
      *move* normal legitimately. How do you tell benign drift (a prompt update that genuinely changes tone)
      from adversarial drift without re-baselining so often that the baseline means nothing?
- [ ] **The right-to-erasure gap.** "Deleting source data doesn't remove its influence from a fine-tuned
      model" is a real wall. Outside of full retraining, is there any control that actually propagates a
      deletion into the weights — or is the honest answer "don't fine-tune on data you might have to delete"?
- [ ] **A2A as governance.** Task 3 shows software arbitration deciding the final action, but the critic's
      signal is thin. When does adding a critic genuinely add safety versus just adding cost, latency, and a
      second model with the same blind spots?

---

## Links & references

_Public sources only — no course material._

- [NIST AI Risk Management Framework (AI 100-1)](https://www.nist.gov/itl/ai-risk-management-framework) — treats AI risk as an extension of existing risk management.
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) — the Identify/Protect/Detect/Respond/Recover functions every control this week maps onto.
- [NIST SP 800-207 — Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final) — "never trust, always verify," applied here to data, tools, outputs, and actions.
- [ISO/IEC 42001 — AI management systems](https://www.iso.org/standard/42001) — grounding AI governance in established information-security principles.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/) — prompt injection, improper output handling, excessive agency, and the rest the controls respond to.
- [OWASP Agentic Security Initiative](https://genai.owasp.org/initiatives/) — the agent-as-privileged-actor threats behind §3.
- [MITRE ATLAS](https://atlas.mitre.org/) — the adversarial-ML technique catalogue, the AI analogue of ATT&CK.
- [EU AI Act](https://artificialintelligenceact.eu/) — risk-tiered obligations referenced in the frameworks section.
- [Hugging Face SafeTensors](https://github.com/huggingface/safetensors) — the safer serialization format behind the supply-chain control (Week 4 callback).
- [Microsoft — spotlighting to defend against indirect prompt injection](https://www.microsoft.com/en-us/research/publication/defending-against-indirect-prompt-injection-attacks-with-spotlighting/) — separating data from instructions, the principle behind the sanitiser diagram.
- [Simon Willison — the dual-LLM pattern](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/) — a system-level approach to keeping untrusted content away from privileged actions.
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) and [Guardrails AI](https://github.com/guardrails-ai/guardrails) — the guardrail frameworks named in §8.

---

## Boundary note

This summary is my own writing, my own diagrams, and a small from-scratch toy (`jori_gate.py`). It doesn't
reproduce the cohort's transcripts, slides, lab code, or videos. 
