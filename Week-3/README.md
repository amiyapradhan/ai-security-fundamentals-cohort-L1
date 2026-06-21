# Week 3 — Working With AI Systems

> Week 3 of my [AI Security Fundamentals cohort](https://github.com/amiyapradhan/ai-security-learning) learning log.
> Notes, code, and diagrams here are mine; the cohort's transcripts, labs, and videos aren't reproduced.

**Cohort session:** Sat 13 Jun 2026 · **Summary written:** 21 Jun 2026<br>
**Medium article:** [Securing AI as a System: Why the Model Is the Least of Your Problems](UPCOMING_MEDIUM_URL)<br>
**LinkedIn post:** [_link once published_](UPCOMING_LINKEDIN_URL)

---

## TL;DR — one paragraph

Week 2 was about the model in isolation; Week 3 takes it out of the lab and wires it into a
real system — and the unit of analysis changes completely. The single idea I took away is that
**risk doesn't live in the model; it lives in the interactions around it.** A model only emits
signals. What makes those signals dangerous is everything bolted on: inputs are *assembled* from
sources the model can't tell apart, context is *retrieved and injected* to become the model's
entire world, orchestration turns probabilities into automated actions, tools let it change
state in other systems, and outputs are treated downstream as authoritative fact. Wrap that in
access control, monitoring, logging, and guardrails — all human-designed control points, none of
them guarantees — and you get the week's punchline: **a known model weakness becomes a
vulnerability the moment a system trusts and acts on it at scale.** And these systems fail
*without crashing* — no error, no alert, just a confident wrong decision propagating quietly.

---

## What I learned

### The reframe: stop securing the model, start securing the system
A model produces an output — a label, a score, some text. On its own that's inert. The risk
appears when a *design choice* causes that output to be **trusted, automated, or amplified.** An
odd prediction sitting in a log is harmless; the same prediction auto-creating a ticket,
reordering a queue, or messaging a customer is not. The standards bodies (OECD, ISO, the EU AI
Act) all converge on the same shape: an AI *system* takes inputs, performs inference, and
produces outputs that influence real or virtual environments. The model is one box inside that
system, and most of the attack surface is in the wiring, not the weights.

### Inputs are assembled, and interfaces aren't neutral
The biggest correction of the week: **"input" is not "the prompt."** A single model call fuses
user text, system instructions, conversation history, retrieved documents, database records,
config — and even the outputs of other models — into one blob. The model can't tell which part
came from where; to it, it's all just tokens. Trust exists only in the surrounding logic. And
*how* those inputs arrive matters too: a chat box, a structured API, and a batch pipeline impose
different validation, state, and rate limits, so the **same model behaves differently depending
on how it's accessed.** A lot of "weird AI behaviour" is really input-construction behaviour with
the model working perfectly.

### Context construction is where the model's reality is built
Before the model is called, the system decides what it will *see* — retrieving from document
stores, databases, ticketing systems, or knowledge bases and injecting the result. The model
reasons over that injected context as if it were the whole world (it's a robot vacuum trusting a
handed-to-it map). RAG makes this concrete: a query is embedded, matched against a vector store,
and the top chunks are stitched into the prompt. That splits *knowledge storage* from
*generation* and introduces brand-new trust boundaries — vector-store integrity, embedding
quality, retrieval logic — none of which live in the model. Whoever controls retrieval controls
what the model treats as ground truth.

### Where signals become actions: orchestration, tools, outputs
**Orchestration** is the human-written control logic between model calls — the thresholds,
routing, and stop-conditions that turn a probability into a decision. **Tools** let the model
*propose* an action that the system then executes (the model never runs the tool itself), which
expands capability from "advise" to "act, change state, and affect other systems" — and standards
like MCP and A2A are how that tool/agent sprawl gets coordinated. **Outputs** then propagate:
downstream systems treat them as authoritative, strip the uncertainty, trigger workflows, and
even feed them back as future context. A tiny difference in output — crossing a threshold — can
become a large, persistent, self-reinforcing consequence.

### The cross-cutting layers wrap the whole pipeline
Four controls sit across every component: **access control** (who/what can see context, use
tools, and act — which also bounds how autonomous an agent can be), **monitoring** (because
uptime tells you nothing about *semantic* failure), **logging / memory / retention** (the
forensic trail, and the memory that shapes future behaviour), and **guardrails** at the input,
context, output, and action layers. The lesson is **defense in depth**: every layer is imperfect,
so they overlap — and the dangerous gap is a guardrail applied at the user interface but *not* at
a downstream integration, which gives a false sense of safety while a bypass path stays open.

### Why these systems fail differently — and why humans in the loop aren't a fix
A model weakness (distribution shift, poor calibration, spurious correlations) is well understood
on its own. It becomes a **vulnerability** when a system trusts and acts on it under automation
and scale — uncertainty gets treated as a signal for action. These failures rarely look like
exploits: no payload, no crash, just behaviour drifting into wrong/biased/unsafe while every
dashboard stays green. And "human in the loop" is a control point, not a safety switch —
engineered badly it adds **automation bias** and **anchoring**, scaling the model's mistakes
through human endorsement while looking like oversight on paper.

---

## The mental models that stuck

- **Secure the pipeline, not the algorithm in the middle** — the model is one box; risk is born
  where signals are assembled, trusted, and acted upon.
- **The map is the world** — the model reasons over whatever context the system injects, so
  whoever controls retrieval controls the model's ground truth.
- **Weakness × automation × scale × trust = vulnerability** — a known model limitation turns into
  a security problem only once a system acts on it, automatically, at volume.
- **It fails without failing** — AI-system failures are semantic, not technical; no crash, no
  alert, just a confident wrong decision that propagates and loops back on itself.

---

## What I built this week

| Artifact | What it does | File |
|---|---|---|
| Redrawn reference architecture | The whole AI-system pipeline — inputs → interface → context → orchestration → model → tools → outputs — plus the two threat models (runtime trust zones and the build-to-serve lifecycle), redrawn from my notes as clean SVGs | [`./diagrams/`](./diagrams/) |
| Context & agent diagrams | My own redraws of information-retrieval / RAG, MCP + A2A, the agentic loop, and the concentric **defense-in-depth** guardrail model | [`./diagrams/`](./diagrams/) |
| Trust-boundary walk-through | A written pass over the pipeline that annotates every arrow as a trust hand-off and maps where system *design* (not implementation) creates the vulnerability | [`./trust-boundary-map/`](./trust-boundary-map/) |
| System-control experiments | Drove one toy vacuum system from an identical starting state — a rules baseline, then three LLM providers, then MCP and an A2A propose→critique→arbitrate flow — and recorded where the providers diverged, where a one-line software arbitration rule (not the model) decided the outcome, and how the same input at fixed temperature still returned different actions | _my own observations; the provided lab code isn't reproduced_ |

> The cohort lab worked from a provided system. My artifacts are my **own redraws, my own
> threat-model annotations, and my own observations from driving it**. The provided lab code isn't reproduced.

---

## Questions I still have

- [ ] The model can't tell instructions from data — so is instruction-vs-data separation
      achievable end-to-end, or only *mitigable*? Where's the strongest place to enforce it?
- [ ] If retrieval can pull attacker-influenced context (RAG), which control actually catches it,
      and where does it sit on the pipeline?
- [ ] For an agentic loop, what's the minimum set of stop-conditions and step-limits before I'd
      let it call a *state-changing* tool?
- [ ] Given automation bias and anchoring, when is a "human in the loop" a *net negative* control
      — and what would make me remove it rather than add it?

---

## Links & references

_Public sources only — no course material._

- [OECD — Recommendation on Artificial Intelligence](https://oecd.ai/en/ai-principles) — the "influences real or virtual environments" definition.
- [EU AI Act (Regulation (EU) 2024/1689)](https://artificialintelligenceact.eu/) — the AI-system definition (Art. 3) and human-oversight requirement (Art. 14).
- [NIST AI Risk Management Framework (AI 100-1)](https://www.nist.gov/itl/ai-risk-management-framework) — lifecycle / systemic-risk framing and oversight as a designed property.
- [OWASP — Top 10 for LLM Applications](https://genai.owasp.org/) — prompt injection, sensitive-info disclosure, excessive agency: the threats this architecture sets up.
- [MITRE ATLAS](https://atlas.mitre.org/) — adversarial threat landscape mapped onto the system.
- [Anthropic — Model Context Protocol (MCP)](https://modelcontextprotocol.io/) — standardising how tools and context are described to models.
- [Linux Foundation — Agent2Agent (A2A) Protocol](https://a2a-protocol.org/) — the open standard for agent-to-agent coordination (originally Google, donated to the Linux Foundation in 2025).
- [Lewis et al. (2020) — Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) — the retrieve-then-generate pattern behind RAG.
- [ISO/IEC 23894:2023 — AI risk management](https://www.iso.org/standard/77304.html) — structured integration of oversight.

---
