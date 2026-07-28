# Week 7: AI Governance, Risk & the Vroomi Capstone

> Week 7 of my [AI Security Fundamentals cohort](https://aisecurityfundamentals.com) learning log.
> The notes, diagrams, and toy code here are mine; the cohort's transcripts, slides, and capstone lab aren't reproduced.

**Cohort session:** sat 11 July 2026 · **Summary written:** 20 Jul 2026 <br>
**Medium article:** ["The Model Did It" Is Never an Answer](REPLACE_WITH_MEDIUM_URL) <br>
**LinkedIn post:** [_link once published_](REPLACE_WITH_LINKEDIN_URL)

> **Note on scope:** Week 7 is two things at once. The videos are the **governance module**;
> the lab is replaced by the **Vroomi capstone**, which spans Weeks 7–8. This README covers both: what I
> learned from the module, and what I built for the capstone.

---

## TL;DR

Weeks 1–6 lived *inside* the system: how models work, how they fail, how they're attacked, how controls
bound them. Week 7 zooms all the way out. Vroomi is deployed across an organisation, she works, she's
reasonably secure. That is exactly when the questions the module cares about start: *who decided she
could touch internal documents? who decided what error rate was acceptable? who's accountable when she's
confidently wrong?* **Security asks "can someone break it?" Safety asks "can it cause harm on its own?"
Governance asks "should this system exist in this form at all, and under what conditions?" The first two
operate inside the system. Governance operates around it.**

The spine of the module in one line: **governance is not a document, a committee, or a one-time approval.
It's how decisions get made about the system, who makes them, and what happens when the assumptions break.**
Everything hangs off two claims. First, **context, not the model, determines risk**: the same weights are
low-risk avoiding socks in a house and high-risk avoiding tubes in a hospital. Second, **"the model did it"
is never an answer**: models don't choose where they're deployed, how much autonomy they have, or what they
can touch; people do, and governance exists to make those people named and accountable *before* the
postmortem.

The capstone is where this stops being theory. I step into an AI-security-practitioner role at Softmicro
and give the CISO a security assessment of Vroomi *before* she's given more agentic features. That's the
governance move from the module (identify risks, assess impact, note residual risk, decide explicitly and
accountably) applied end-to-end.

---

## What I learned

### Governance lives *around* the system, not inside it
The module's opening move is to refuse to let four words blur. **Security** defends against adversarial
threats. **Safety** prevents harmful behaviour even with no attacker. **Governance** is the decision-making
and accountability layer that decides whether a system should be deployed here at all, and **compliance** is
meeting external requirements. Security and safety operate *on the machine*; governance operates *on the
decisions*. A system can be fully compliant and still poorly governed. The load-bearing consequence: you
cannot answer a governance question with a technical control. You can have perfect access controls and still
deploy Vroomi into a context where harm is inevitable, or strong safety mitigations with no clarity on who
owns the risk.

### Ownership, accountability, and the incentive trap
Every AI system needs a named owner: not a technical maintainer, but a role with decision authority over the
system's behaviour *in context*. Ownership defines who decides; accountability defines who answers. The
place governance actually breaks is incentives: engineers are rewarded for shipping, business for scale,
security for fewer incidents, legal for avoiding liability. Vroomi sits at the intersection of all of them.
Unaligned incentives create the classic blame loop ("we'll fix it next sprint" / "we need to launch now" /
"just document the risk") that only resolves after an incident. Governance assigns ownership *before* deployment.

### Risk management is a decision, not a checklist
A checklist asks "did we do the thing?" Risk management asks "is the remaining risk acceptable *given the
context*?" AI failures aren't binary: they're probabilistic, uneven, and context-dependent, so AI risk
management focuses on *patterns, not events*, and it's iterative (design → deploy → change → environment
change). The key shift is model-centric → system-centric: a model can ace benchmarks and tell you almost
nothing about how risky the system is once it's embedded, connected, and trusted. And the artifacts (risk
registers, impact assessments, approval records) aren't bureaucracy: they're **the difference between an
unfortunate outcome and a governance failure**, because they show what was known, what was assumed, and why.

### Frameworks structure judgment, they don't replace it
NIST AI RMF (Govern / Map / Measure / Manage) structures risk for a *specific deployment*; ISO standards
embed AI risk into repeatable *organisational* processes; the EU AI Act and sector guidance blend risk
management with legal obligation. None of them secure anything. They're scaffolding that forces you to ask
"what's the impact if this fails, who's affected, how reversible is the harm, how much autonomy does it
have", and to prioritise, because treating a spelling tool and a medical-triage assistant as equivalent is
itself a governance failure.

### High-risk is a property of deployment, and residual risk is a decision you record
The single most repeated idea: stop asking *"is this model high-risk?"* and start asking *"what decisions
does it influence, who can it harm, at what scale, and how fast can we detect and reverse failures?"* High
risk shows up when the system meaningfully influences a decision about a person, runs at automation scale,
or has asymmetry in accountability. Then the assessment loop: identify → impact → likelihood → controls →
**residual risk**, where residual risk isn't a failure but the exposure that remains after sensible
controls, made *explicit*, recorded, and signed off. The same residual risk is acceptable for summarising
schedules and unacceptable for building-access workflows.

### Qualitative and quantitative are layered, not rivals
Qualitative (green/amber/red, expert judgment) routes systems into the right governance pathway early;
quantitative (scores, error rates, Bayesian ranges) adds value where data exists: comparing options,
monitoring drift, evaluating residual risk. The example that made it click: a qualitative review calls
Vroomi's summarisation "low risk"; six months of tracking finds 3% of summaries drop critical information,
and in legal/medical contexts that 3% is unacceptable even though the average is fine. **The number gives
you something to measure; the qualitative judgment tells you what the number means.**

### Policies, regulation, compliance: the machinery that turns risk into rules
Safety policies express values and risk tolerance; AUPs express day-to-day rules (who, what, what data,
where), and both *drive technical controls* rather than living in isolation. The regulatory landscape is
global, fragmented, and fast-moving, but four themes recur everywhere: context beats the model, risk
management is becoming a legal expectation, documentation/traceability matter, and human oversight must be
real (defined roles, escalation, limits on automation). And the distinction that trips up whole
organisations: **compliance is the floor, governance is the building.** Compliance is point-in-time, scoped,
and driven by fear of penalties; governance is continuous, covers everything (including the internal tools
no regulation reaches), and is driven by responsibility. Most real AI harm happens *outside* regulated scope.

### Documentation, third parties, oversight, incidents, and a living programme
Model / system / agent cards are governance tools that make a system legible to the people accountable for
it, and they only stay useful if they're *living documents*. Most organisations *procure* AI rather than
build it, so third-party risk (models, APIs, data, managed services) is a risk decision, not an admin step:
treat vendors as extensions of the system, not black boxes, because "if you can't name your dependencies,
you can't govern them." Human oversight is a *design problem*, not a checkbox: it fails quietly through
automation bias, anchoring, scale/fatigue, and missing context. AI incidents often have no alert or crash,
so detection and containment are *behavioural* and must be pre-planned. And a governance programme is built
deliberately in order (**visibility → risk-based classification → ownership → embedded controls → policy +
training → continuous review**) because *you can't govern what you can't see*. The final idea ties it all
together: **governance is a living system**; change itself is the trigger to re-decide, and waiting for harm
before acting is the most dangerous pattern of all.

---

## A few framings I want to keep

- **Governance is around the system, not inside it.** Security and safety act on the machine; governance
  acts on the decisions: who owns the risk, what trade-off was accepted, who answers when it breaks.
- **Context, not the model, determines risk.** Same weights, different deployment, different world.
- **"The model did it" is never an answer.** People decide where it runs, how much autonomy it has, and
  what it can touch.
- **Compliance is the floor; governance is the building.** Most real AI harm happens outside regulated scope.
- **You can't govern what you can't see, can't name, or won't own.**
- **Human oversight is a design problem, not a checkbox:** it fails quietly through bias, anchoring,
  fatigue, and missing context.
- **Governance is a living system:** change itself is the reason to revisit a decision.

---

## What I built this week: the Vroomi capstone

The capstone replaces the Week 7 + Week 8 labs. I'm an AI security practitioner at Softmicro; the CISO wants
an assessment of Vroomi before she's given more agentic features (recommendations, drafting tickets,
interacting with internal systems). I worked Task 0 first for the baseline, then explored the attack/defence
pairs, and turned the whole thing into a governance deliverable.

| Artifact | What it is | Where |
|---|---|---|
| **Vroomi system diagram** | My own redrawn diagram of the components (user input, knowledge base, system prompt, the model, the tool executor, and the backend actions), with trust boundaries (🔴 untrusted / 🟡 semi-trusted / 🟢 trusted) and ⚠️ threats annotated at each boundary crossing | [`vroomi-system-diagram.svg`](./capstone/vroomi-system-diagram.svg) |
| **AI Security Assessment Report** | The CISO-facing decision document: executive summary, system overview, threat analysis, risk assessment, mitigation effectiveness, recommendations, and a final **Conditional Go**. | [`AI_Security_Assessment_Report.pdf`](./capstone/AI_Security_Assessment_Report.pdf) |
| **Threat cards (attack → root cause → fix)** | One card per task: the input I sent, what the system did, the one-line root cause, the defended behaviour, and the *governance question underneath*, each mapped to the OWASP LLM Top 10 | [`threat-cards.md`](./capstone/threat-cards.md) |
| **Draft agent card for Vroomi** | Goals, tool allow-list, autonomy tiers (autonomous / suggest-and-confirm / human-approval / prohibited), human-in-the-loop points, and stop conditions: the *safeguards to add first* behind the Conditional Go | [`agent-card.md`](./capstone/agent-card.md) |
| **Governance gate (runnable)** | `vroomi_gov_gate.py`, my own from-scratch toy that consolidates the fixes into one file: strict output validation, a tool allow-list, provenance + sensitivity filtering, and an audit log, with a before/after transcript. Runs with no API key or network | [`vroomi_gov_gate.py`](./capstone/toy/vroomi_gov_gate.py) |

> The cohort capstone gave us Task 0 plus the six attack/defence tasks and the Vroomi system to assess.
> What's here is my own: the redrawn diagram, the assessment report, the per-task threat cards, the draft
> agent card, and a small governance gate I wrote from scratch. The provided capstone notebooks and the
> cohort's code aren't reproduced.

---

## The point the capstone makes in one move

Across all six tasks, in not a single one is the fix "make the model smarter." In most of them the model
isn't even the weak point. Prompt injection succeeds because the *application* looks for instructions in user
input and executes them before the model runs. System-prompt leakage happens because a *debug path* returns
the prompt, not because the model is jailbroken. Data poisoning and misinformation work because nothing ranks
*provenance or trust* before documents reach the model. Sensitive disclosure happens because sensitive data
was placed in model-accessible context with no *classification*. Improper output handling executes tool calls
because the system *trusts model output* without validation. Every fix is a governance and architecture
decision. That's exactly why the recommendation is a **Conditional Go**: the defended versions prove the
safeguards are architectural, so the condition is *make them mandatory before the agentic features ship, not after*.

---

## Questions I still have

- [ ] **Where "sensible" stops being encodable.** The capstone defences are deterministic gates (trust
      filtering, output validation, sensitivity classification). How much of "governed behaviour" can be
      encoded as rules before you're just re-implementing judgment in `if` statements, and where's the
      honest line where a human *has* to own the call?
- [ ] **Residual-risk sign-off in practice.** The module says record the residual risk and assign
      accountability. In a real org, who actually signs, how often is it revisited, and what stops the
      signature becoming a rubber stamp (the compliance-vs-governance failure the module warns about)?
- [ ] **Agent cards for systems that change under you.** An agent card is a living document, but third-party
      models/APIs change without notice. How do you keep an agent card honest when the autonomy it documents
      depends on a vendor you don't control?
- [ ] **The oversight/scale contradiction.** The module's point is that oversight works only for infrequent,
      high-stakes decisions, but the whole point of the agentic features is volume. Is the resolution *fewer*
      human touchpoints on *only* irreversible actions, or is there a real ceiling on how agentic Vroomi can
      safely get while keeping meaningful oversight?
- [ ] **Detecting the slow failure.** The compliance-vs-governance example (Vroomi quietly deprioritising one
      department) has no alert and breaks no rule. What's the minimum monitoring that would actually catch a
      failure like that before it becomes an incident?

---

## Links & references

_Public sources only; no course material._

- [NIST AI Risk Management Framework (AI 100-1)](https://www.nist.gov/itl/ai-risk-management-framework): Govern / Map / Measure / Manage, the module's core scaffold.
- [ISO/IEC 42001: AI management systems](https://www.iso.org/standard/42001) and [ISO/IEC 23894: AI risk management](https://www.iso.org/standard/77304.html): the organisational-process half of governance.
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework): the risk functions AI governance extends rather than replaces.
- [EU AI Act](https://artificialintelligenceact.eu/): the risk-tiered logic (unacceptable / high / limited / minimal) being copied globally.
- [NCSC: Guidelines for Secure AI System Development](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development): the secure-AI guidance referenced for procurement and lifecycle.
- [OWASP AI Vulnerability Scoring System (AIVSS)](https://aivss.owasp.org/): AI-native severity scoring.
- [FAIR: Factor Analysis of Information Risk](https://www.fairinstitute.org/what-is-fair): the quantitative risk model behind the qualitative-vs-quantitative distinction.
- ["Model Cards for Model Reporting", Mitchell et al.](https://arxiv.org/abs/1810.03993): the origin of the model-card lineage that system and agent cards extend.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/): the vulnerability taxonomy the six capstone tasks map onto (prompt injection, system-prompt leakage, data/model poisoning, sensitive-information disclosure, misinformation, improper output handling).
- [MITRE ATLAS](https://atlas.mitre.org/): adversary tactics for AI, the technique catalogue behind the attack tasks.

---
