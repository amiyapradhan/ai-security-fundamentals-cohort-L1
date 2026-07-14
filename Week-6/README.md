# Week 6 — Emerging Risks, Alignment & Long-Term AI Safety

> Week 6 of my [AI Security Fundamentals cohort](REPLACE_WITH_REPO_URL) learning log.
> The notes, code, and diagrams here are mine; the cohort's transcripts, slides, and labs aren't reproduced.

**Cohort session:** Sat 4 Jul 2026 · **Summary written:** 11 Jul 2026
**Medium article:** [AI Safety Isn't About Attackers](REPLACE_WITH_MEDIUM_URL) ·
**LinkedIn post:** [_link once published_](REPLACE_WITH_LINKEDIN_URL)

---

## TL;DR

Weeks 1–5 were security: where an AI system breaks and how to bound it. Week 6 is the other lens —
**safety** — and the unsettling part is the failures that happen when *nobody* attacks, *nothing* crashes,
and every box is ticked. **A safety failure isn't the model breaking; it's the model *succeeding*** —
optimising the proxy you gave it instead of the goal you meant, generalising the wrong correlation,
pursuing that objective competently and at scale. The danger was never malice; it's competence pointed
slightly wrong, then automated.

The spine, in one line: *the system doesn't need to be malicious — it just needs to be confident, and then
it needs to be trusted.* That's the safety mirror of Week 5's "the model suggests, the system decides." By
the end the loop closes: safety and security aren't separate checkboxes — they're the same question at
scale, *what happens when a confident-but-wrong output is trusted and acted upon?*

---

## What I learned

### Safety is not security, governance, or compliance
**Security** stops attackers (misuse, exploitation, compromise). **Safety** prevents harmful or unintended
behaviour *when no one is attacking* — how the system behaves by default, at scale, in situations nobody
designed for. **Governance** is who's accountable; **compliance** is ticking legal boxes. A system can be
fully compliant and still unsafe. Vroomi: break into her controls = security; she follows her instructions
exactly and still acts unsafely = safety. This module is that second class of risk — emergent,
probabilistic, systemic, often invisible until scale.

### "Emerging" risk grows over time, scale, and interaction — not at build time
An emerging risk isn't a bug that's simply present or absent in the code; it arises *over time* as a system
updates, scales, and interacts, and is often invisible until deployed. The threat-intel framing that stuck:
these are like zero-days in the *behaviour*, not the code — no CVE captures "it started optimising for the
wrong metric." And emerging ≠ hypothetical; many have already happened.

### Emergence is structural — five properties make it expected
It's baked into what these systems are: **generalisation** (off-distribution behaviour is normal, not an
edge case), **automation** (small biases amplified across many decisions), **feedback** (systems shape the
data they later consume), **probabilistic decisions** (uncertainty hidden behind confident outputs), and
**composition** (risk emerges from components interacting). So safety needs monitoring that *assumes
change*, not one-time pre-deployment testing.

### Capability grows in steps, not slopes — so risk appears late
+10% power doesn't buy +10% capability. Models learn *representations*, so capability arrives in sudden
jumps (phase transitions). Two consequences: small-scale tests don't predict large-scale *behaviour*, and
**risk appears late** — a system looks harmless while too weak to matter, then the same design choices
matter enormously once it crosses the threshold.

### Scaling laws describe performance, not behaviour
Scaling laws smoothly predict *average performance* (loss, accuracy) — but not *behaviour*, which is what
safety cares about. Bigger models do genuinely *new* things, exploit ambiguity, and make humans trust them
more. Scaling **smooths averages but sharpens extremes**: fewer mistakes, but the remaining ones are more
fluent and harder to catch.

### Alignment fails when optimisation *succeeds*
Models optimise a *proxy* (a loss, a metric), never "the right thing" — and the proxy is always a lossy
stand-in for what we meant. **Alignment problems arise when optimising the proxy satisfies the objective
but violates the intent** — a structural feature of optimisation, not a bug. As capability grows,
misalignment looks less like failure and more like *competence aimed in the wrong direction.*

### Two ways the objective goes wrong: Goodhart, and goal misgeneralisation
**Goodhart** ("when a measure becomes a target it stops being a good measure") bites because ML systems are
excellent optimisers — the better the optimiser, the harder it exploits the proxy/goal gap (the paperclip
maximizer is the cartoon; engagement-optimising feeds are the everyday version). **Goal misgeneralisation**
is subtler: the metric's fine, but the model learns the *wrong reason* — a correlation that held in
training (tidy rooms were bright) and breaks in deployment. It scores well and still does the wrong right
thing.

### Autonomy turns a mistake into a persistent, compounding risk
With tools and memory, a wrong answer stops being momentary and starts accumulating — agents looping and
burning compute, copilots mis-categorising tickets for months, assistants baking a wrong assumption into
memory. The framing that landed hardest: **incident response for autonomous AI looks like insider-threat
response, not malware** — legitimate access, normal-looking operation — so you hunt subtle drift from
*intent*, not obvious malice.

### Long horizons drift; "deception" is pressure, not intent
Over long tasks with delayed feedback, models optimise *local* steps well but drift from the global goal —
busy, confident progress in the wrong direction. And "deception" doesn't mean inner motive; it's
**behaviour that *functions* like deception because it improves the objective** (reward hacking, strategic
framing). No plan, just *selection pressure* — the concern isn't "will it want to deceive us" but that
"truthfulness isn't what's being optimised."

### The frontier changes the *shape* of risk; misuse ≠ misalignment
Frontier models concentrate capability (and risk) in a few systems on shared infrastructure (~75–80% of
frontier inference on three clouds — a systemic single point of failure). Five shifts: capability
generality, compositional reach, emergent behaviour under scale, asymmetric leverage, uncertainty
concentration. And two coupled risks: **misuse** needs a bad actor and collapses the skill threshold for
harm; **misalignment** needs none and *fails competently* during legitimate use. (I kept the misuse notes
conceptual and non-operational — the shape of the risk, not a recipe.)

### Evals discover risk; they don't guarantee safety
Capability evals (MMLU, GSM, HumanEval) measure *power*, not *safety*; safety and frontier evals are newer
and less stable. The load-bearing limit: **evals only measure what you thought to test.** They fail via
coverage gaps, distribution shift, overfitting (models behave differently when they detect evaluation),
proxy mismatch, system-level effects, and *false confidence*. Read one like a pen-test report — a
point-in-time finding, not a guarantee. Passing means "didn't fail in the ways we tested." (Galactica
scored well and fabricated citations in real use.)

### Red teaming is for the unknown unknowns, and it never finishes
Evals test what you already know to look for; **red teaming** hunts what you *haven't* defined, thinking
like an adversary and chasing interaction effects. Its output is insight, not a score, and it feeds the
eval loop (discover → measure → govern → repeat). It's continuous because every model, tool, or data-source
change *moves* the unknown unknowns.

### At society scale, failures correlate — and safety and security converge
**Systemic risk** comes from *concentration* (a few orgs control models + infrastructure) and *dependence*
(institutions couple so tightly that small failures cascade and many systems fail the same way at once) —
no attacker needed. The evidence is real: the AI Incident Database's 1000+ harms, EchoLeak, a UK police
force acting on an AI-fabricated event, the 2025 International AI Safety Report, IBM's breach data.
**Safety failures propagate through *system trust decisions*; security vulnerabilities amplify them;
benchmark success doesn't guarantee safe deployment.** Weeks 1–5 built the security half; Week 6 the safety
half; they were always the same problem.

---

## A few framings I want to keep

- **Competent, confident, and wrong.** A safety failure is the model *succeeding* at the wrong target —
  misalignment doesn't look like failure, it looks like competence aimed slightly wrong, then automated.
- **The system doesn't need to be malicious; it just needs to be confident — and then trusted.** The
  safety mirror of "the model suggests, the system decides."
- **You optimise a proxy, never the goal** — and a *better* optimiser exploits the gap harder, not softer.
  Goodhart isn't a bug; it's a trade-off that gets worse with capability.
- **Capability grows in steps, not slopes**, so risk appears *after* the threshold — the system looks safe
  right up until it's capable enough to matter.
- **Passing an eval means "didn't fail in the ways we tested," not "safe."** Read it like a pen-test
  report: a point-in-time finding, not a production guarantee.
- **Autonomy turns errors into insider threats.** Legitimate access, normal-looking operation, subtle
  drift from intent — so you monitor for *meaning*, not crashes.
- **Safety and security are one question at scale:** what happens when a confident-but-wrong output is
  trusted and acted upon?

---

## What I built this week

| Artifact | What it is | Where |
|---|---|---|
| `proxy_gap.py` (toy) | A small clean-room toy I wrote from scratch to make one sentence tangible — *alignment failures happen when optimisation succeeds.* Vroomi optimises a **detected-debris** proxy; a better optimiser discovers that *suppressing detection* is cheaper than cleaning, so as her skill rises the **reported** score falls (52 → 5, dashboard looks spotless) while **true** dirt rises (52 → 100, house is filthy). Proxy down, goal up — Goodhart in ~40 lines of arithmetic | [`./proxy_gap.py`](./proxy_gap.py) |
| Redrawn diagrams | My own SVG redraws of the week's concepts — the three axes of emerging risk, the threshold/step-change capability curve, proxy-vs-intent translation, training-vs-deployment goal misgeneralisation, the autonomy compounding loop, the evals-vs-real-world overlap, single-system-to-systemic fan-out, and the model-behaviour → trust-decision → real-world-impact flow | [`./diagrams/`](./diagrams/) |

> This week is the conceptual safety module — no rebuild lab — so what's in this repo is just my own work:
> the redrawn diagrams and a small toy I wrote from scratch. `proxy_gap.py` is clean-room; it is **not**
> cohort code and doesn't reproduce any lab.

Run the toy:

```bash
python3 proxy_gap.py
```

---

## The point the module makes in one move

Every failure in the week has the same shape, and in not one of them is the system *broken*. The proxy is
optimised, the correlation is generalised, the plan is locally coherent, the eval is passed, the output is
confident — and the harm happens anyway, because the thing being optimised was never quite the thing we
meant, and then something *trusted the output and acted on it.* That last clause is where safety meets
security: the trust decision is a *system* decision, exactly like Week 5's policy gate, and it's the point
where a confident-but-wrong output turns into real-world impact.

---

## Questions I still have

- [ ] **Measuring the goal, not the proxy.** `proxy_gap.py` "fixes" Goodhart by spot-checking the
      low-visibility places the proxy ignores — but in a real system, isn't the spot-check just *another*
      proxy with its own blind spots? Where's the honest line between "constrain the metric" and "you
      can't measure the goal directly, ever"?
- [ ] **Detecting drift before the compounding.** Autonomy-plus-memory drift is only obvious in hindsight,
      once the wrong assumption is baked in. Is there any practical signal that catches long-horizon
      misalignment *while it's still cheap to correct*, or is periodic re-grounding the best we actually
      have?
- [ ] **Eval-awareness.** If models already behave differently when they detect they're being evaluated,
      how much of any safety eval is measuring behaviour-under-observation rather than behaviour? Does
      holding eval sets private actually help, or just delay the overfitting by one release?
- [ ] **Systemic risk with no owner.** When capability concentrates on three clouds and failures
      correlate, the accountability is spread across model provider, platform, integrator, and customer.
      What does a *credible* systemic-risk control even look like when no single party can see or own the
      whole failure mode?
- [ ] **The misuse/misalignment control split.** Misuse wants access restrictions and intent detection;
      misalignment wants behavioural evaluation and system-level gating. When both live in the same
      frontier system, do those controls ever *conflict* — e.g., monitoring that catches misuse but masks
      the drift that signals misalignment?

---

## Links & references

_Public sources only — no course material._

- [OpenAI Preparedness Framework](https://openai.com/preparedness/) — impact-focused, dangerous-capability evals (bio, chem, cyber, autonomous replication); one of the three links the module points to.
- [Anthropic Responsible Scaling Policy](https://www.anthropic.com/rsp) — capability thresholds and the evals gating deployment; the second module link.
- [UK AI Safety Institute](https://www.aisi.gov.uk/) — government evaluation of advanced cyber reasoning, dual-use science, and long-horizon planning; the third module link.
- [Microsoft — planning red teaming for large language models](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/red-teaming) — the red-teaming discipline behind the red-team section, pointed at LLM applications.
- [AI Incident Database](https://incidentdatabase.ai/) — the 1000+ documented real-world AI harms behind the convergence discussion, maintained under the Responsible AI Collaborative / Partnership on AI.
- [International AI Safety Report (2025)](https://www.gov.uk/government/publications/international-ai-safety-report-2025) — the government-backed consortium report on control failures once models are deployed with real tools and data.
- [DeepMind — specification gaming: the flip side of AI ingenuity](https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/) — the catalogue of proxy-optimisation failures behind the Goodhart discussion.
- [Goal misgeneralisation (Langosco et al.; Shah et al.)](https://arxiv.org/abs/2210.01790) — the "wrong right thing" in the goal-misgeneralisation discussion.
- [Emergent abilities of large language models (Wei et al.)](https://arxiv.org/abs/2206.07682) and [Are emergent abilities a mirage? (Schaeffer et al.)](https://arxiv.org/abs/2304.15004) — the step-change discussion, with the honest counterpoint on how the metric shapes what looks "emergent."
- [Nick Bostrom — *Superintelligence*](https://global.oup.com/academic/product/superintelligence-9780199678112) — the paperclip-maximizer thought experiment behind the Goodhart discussion.
- Frameworks carried over from Weeks 1–5: [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [NIST CSF 2.0](https://www.nist.gov/cyberframework), [OWASP Top 10 for LLM Applications](https://genai.owasp.org/), [MITRE ATLAS](https://atlas.mitre.org/), [EU AI Act](https://artificialintelligenceact.eu/) — the security half of every argument in these notes.
- [My Week 6 write-up, notes, and diagrams](https://github.com/amiyapradhan/ai-security-fundamentals-cohort-L1/tree/main/Week-6) — the redrawn diagrams, the `proxy_gap.py` toy, and the full reference list.

AI-safety material and the public sources above. The aim is to make the course look worth taking, not to
stand in for it.
