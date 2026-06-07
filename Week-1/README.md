# Week 1 — AI Threats & Threat Modelling

> Week 1 of my [AI Security Fundamentals cohort](https://github.com/amiyapradhan/ai-security-learning) learning log.
> Notes, code, and diagrams here are mine; the cohort's transcripts, labs, and videos aren't reproduced.

**Cohort session:** Sat 30 May 2026 · **Summary written:** 06 June 2026<br>
**Medium article:** [How to Map the Attack Surface of an AI System](https://medium.com/@amiyapradhan1/how-to-map-the-attack-surface-of-an-ai-system-f403eb10870c)<br>
**LinkedIn post:** [How to Map the Attack Surface of an AI System][li-week1]

---

## TL;DR — one paragraph

Week 1 was about threat modelling AI systems, and the single idea I took from it is that
"AI security" is not "model security." The model is one asset among many; most real
incidents walk in through everything built around it. The skill is mapping the attack
surface — **assets, entry points, and abuse paths** — and the most useful line on any
diagram is the one separating input you control from input you don't. To make that
concrete, I built Jori — a tiny vulnerable email assistant — and watched a crafted email
turn it into a data-exfiltration tool without anything ever crashing.

---

## What I learned

### The question changes
Traditional security asks *where's the exploitable bug?* AI threat modelling asks *where
can someone influence the meaning the system builds, and what can that influence reach?*
In the incidents I looked at, nothing malfunctioned — the code ran as written. The failure
was always misplaced trust in an input.

### Assets, entry points, abuse paths (a chain, not a list)
- **Assets** — anything harmful if misused, corrupted, or exposed. In AI systems this
  expands to the model's behaviour, its instructions, what it retrieves, user trust in
  its answers, and — critically — its tools and permissions.
- **Entry points** — anywhere influence can enter. Not just APIs: any input the system
  treats as *meaningful* (chat box, a retrieved email, an uploaded PDF, a Slack message).
- **Abuse paths** — the chain from an entry point to an asset. In AI systems it rides on
  *interpretation*, not broken code: a hidden instruction shapes how the model reads
  something → that reading drives an action → the action hits an asset.

The vulnerability lives in the **arrows** (the trust handoffs), not the boxes.

### Three frameworks, three questions
- **STRIDE** — *what kind of threat is this?* (a crafted doc that changes behaviour = tampering).
- **MITRE ATLAS** — *how do attackers actually hit AI?* (prompt injection, poisoning, evasion).
- **OWASP LLM Top 10** — *how do we build safely?* (the defenders' checklist).

ATLAS turns a vague "it did something weird" into a documented pattern:
Tactic → Technique → Vulnerability → Mitigation.

### Two real shapes of attack
- **EchoLeak (CVE-2025-32711)** — a zero-click prompt-injection case in M365 Copilot
  (Aim Labs, June 2025). A crafted email's hidden instruction got followed when Copilot
  retrieved it as context. Textbook abuse path; responsibly disclosed, no in-the-wild use.
- **Distillation against Claude** — a *different* shape. Anthropic alleged (Feb 2026)
  industrial-scale harvesting of model *outputs* via the API to train cheaper copies.
  No CVE, no malfunction — the model used exactly as designed, just not as intended.
  A reminder the surface is bigger than prompt injection.

---

## The mental models that stuck

- **Map the system, not the model** — the model is one asset among many.
- **The trust boundary is the diagram** — the line between input you control and input
  you don't; every crossing is a thing to check.
- **Trust is the attack surface, capability is the asset** — harm happens where they meet.

---

## What I built this week

| Artifact | What it does | File |
|---|---|---|
| Jori (toy target) | A ~100-line email assistant with one deliberate flaw: it obeys instructions found inside email bodies. Run it and watch a crafted email trigger an unintended `forward`. | [`./toy-target/jori.py`](./toy-target/jori.py) |
| Trust-handoff diagram | Entry-point → orchestrator → model → tool-action → asset chain | [`./diagrams/abuse-path.svg`](./diagrams/) |
| Frameworks diagram | STRIDE / MITRE ATLAS / OWASP — three questions | [`./diagrams/three-frameworks.svg`](./diagrams/) |
| ATLAS chain diagram | Tactic → Technique → Vulnerability → Mitigation | [`./diagrams/atlas-chain.svg`](./diagrams/) |

> Jori is a separate build, not the cohort lab — a clean-room way to check whether the
> attack works the way I think it does.

Run it:

```bash
python3 toy-target/jori.py
```

---

## Questions I still have

- [ ] Where exactly does threat modelling stop and architecture review begin?
- [ ] Once an AI system keeps changing, how do you keep its threat model current without
      redoing it from scratch every sprint?

---

## Links & references

- [MITRE ATLAS](https://atlas.mitre.org/) — the adversarial-ML threat knowledge base.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/) — the field's shared checklist.
- Aim Labs' EchoLeak disclosure (CVE-2025-32711) — the zero-click Copilot case.
- [li-week1]: https://www.linkedin.com/posts/amiyapradhan_aisecurity-llmsecurity-threatmodeling-share-7469170914052620288-LfZg/

