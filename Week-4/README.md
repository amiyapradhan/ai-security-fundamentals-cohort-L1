# Week 4 — Attacking AI Systems

> Week 4 of my [AI Security Fundamentals cohort](https://aisecurityfundamentals.com) learning log.
> The notes, code, and diagrams here are mine; the cohort's transcripts, labs, and videos aren't reproduced.

**Cohort session:** Sat 20 Jun 2026 · **Summary written:** 01 July 2026 <br>
**Medium article:** [AI Attacks Were Never About Breaking the Model](https://articles.amiyapradhan.com/ai-attacks-were-never-about-breaking-the-model-6a24d3a7f3cc) <br>
**LinkedIn post:** [AI Attacks Were Never About Breaking the Model](https://www.linkedin.com/posts/amiyapradhan_aisecurity-llmsecurity-adversarialml-share-7477964766364282880-4BY5/)

---

## TL;DR

The risk in an AI system lives in the wiring around the model, not in the weights. Week 4 was about
how attackers turn that into concrete exploits — and I expected a list of new techniques to memorise.
That's not what it is. Almost every attack this week is a trust assumption baked into the system —
about what the model reads, what it's told to trust, and what it's allowed to do — being pushed on
deliberately, and in almost every case the model is doing exactly what it was built to do while it
happens.

That reframe is the whole week. An evasion attack isn't the model malfunctioning — it's the model
correctly reporting what it was shown, where what it was shown was chosen to land on the wrong side
of a boundary. Prompt injection isn't a parser bug — it's the model treating injected text as
instructions because it has no way to tell instructions from data. Data poisoning isn't sabotage of
the code — it's the training process doing its job on inputs someone got to choose. None of these
break the model. They exploit three facts about how models work: they minimise a loss rather than
chase correctness, they generalise rather than reason, and their confidence is an artifact of
training rather than a measure of truth. The disturbing part is the second-order effect — the system
we built around the model to make it useful doesn't fix any of those weaknesses, it *scales* them.

---

## What I learned

### These attacks aren't new — the target is the decision, not the code
The week opened by killing the idea that AI attacks are a fresh category. People have manipulated
statistical decision systems for decades: gaming search rankings, dressing spam up to slip past a
filter, structuring transactions to stay under a fraud threshold. None of that touches source code.
It works by understanding how an automated system decides and then feeding it inputs that make it
decide wrong. A model is just the newest and most capable decision system to point that technique at.
Once I had that framing, everything after it stopped looking like a bag of tricks and started looking
like one idea applied to different surfaces.

### Evasion: a perfectly valid input that's still adversarial
The first surface is the model's own input space. Because a classifier carves its input into regions
with decision boundaries, and because those boundaries are an approximation of the real ones, there's
always space between "where the boundary is" and "where it should be." Evasion lives in that gap. The
canonical demo is still the 2014 panda that becomes a gibbon (Goodfellow, Shlens, and Szegedy):
add a tiny, calculated perturbation along the gradient — the FGSM recipe is literally
`x + ε · sign(∇loss)` — and the model flips to high confidence on the wrong label while the image
looks unchanged to a human. The unsettling properties are that it can be a one-pixel change, it can
transfer to models the attacker never saw (black-box), it can target a *specific* wrong answer, and
it leaves no trace, because nothing went wrong — the model evaluated the input it was handed exactly
as designed. I reproduced a small version of this with FGSM in the lab and watched confidence move
with epsilon.

### Steering the output without touching the model
The next surface is generation itself. A language model samples from a probability distribution; it
doesn't *choose* an answer, it draws one. So anything that shifts that distribution steers the output
without any access to weights or code: the order you put instructions in, priming a role or an
authority, anchoring the model semantically near the answer you want, shaping how confident it sounds.
This is the same family as prompt injection but quieter — no obvious "ignore previous instructions,"
just a context arranged so the most probable continuation is the one you wanted.

### Training-time attacks: poisoning, backdoors, and persistence
Move upstream of inference and you get to the data. Poison the training set — flip labels, plant a
spurious correlation, or hide a backdoor that stays dormant until a specific trigger appears — and the
model learns the corrupted pattern as faithfully as any real one. Two things made this stick. First,
persistence: once a backdoor is in the weights, it survives; you can't grep it out, and clean-data
accuracy can look perfect while the trigger still works. Second, scale through reuse: everyone
fine-tunes from the same handful of base models, so one poisoned upstream artifact propagates to every
system that builds on it.

### Model artifacts are executable code, not data files
This was the most concrete "oh no" of the week. A serialized model — a pickle checkpoint — is data
*and* code, and loading it executes that code. So `torch.load` on a file someone handed you is running
their program, not just reading their weights. This is the seam where ML attacks meet classic
software supply chain, and it reframes a model download as exactly the kind of thing you'd never do
with a random executable.

### Privacy: models don't forget
A separate class of attack doesn't change behaviour at all — it extracts. Membership inference asks
"was this record in your training set?" and reads the answer off the model's unusually high confidence
on data it has seen before. Training-data extraction goes further and pulls memorised content back
out. The framing I'm keeping is that a trained model is a lossy store of its training data, and you
can't make it forget — the information is in the parameters.

### Prompt injection is the pivot of the whole week
Everything above is, in some sense, model-level. Prompt injection is where it becomes *system*-level,
and the course built the week around that hinge. Direct injection — a user typing a malicious
instruction — is a model problem. Indirect injection is the dangerous one: the malicious instruction
rides in through content the system *retrieved* — a document, a web page, a tool's output — and the
model, unable to separate that from its real instructions, follows it. The reach is the difference.
A direct injection compromises one conversation; an indirect one compromises every request that
retrieves the poisoned source. The public examples make it real: the early Bing chat ("Sydney")
leaking its own rules, browsing agents acting on instructions hidden in pages, the Chevy dealer bot
talked into absurd commitments.

### RAG, tools, APIs, and A2A are amplifiers, not new attacks
Once injection is on the table, the rest of the architecture stops being neutral. Retrieval *is*
control — whoever decides what gets retrieved decides what the model treats as true, and the quiet
assumptions (retrieved means safe, relevant means trustworthy, ordering doesn't matter, truncation
won't drop the safety instruction) are each an attack. Tools and APIs turn a compromised decision into
a real-world action. MCP and A2A standardise how tools and agents connect, which also standardises a
transitive-trust problem: agent A trusts agent B, B was injected, now A is acting on it. None of these
invent a new attack. They take the model-level ones and give them range.

### Soft DoS and supply chain: failure without a break-in
Two system-level attacks that don't look like attacks. Soft (compute) DoS exploits that inference cost
is input-dependent — a prompt that maximises token generation or triggers heavy tool use can run up
real money and latency without flooding anything, which is why heuristics beat hard limits here and
why it's hard to detect. Supply chain is the same logic widened: the danger arrives through a
dependency you trusted — a base model, a dataset, a package, a managed service — and it spreads
through trust relationships, not intrusion.

### The case studies that made it concrete
Six real incidents anchored the abstractions: **EchoLeak** (CVE-2025-32711, a zero-click data
exfiltration in Microsoft 365 Copilot found by Aim Labs — indirect injection with no user click at
all); **malicious Hugging Face models** using pickle payloads, and the PickleScan research showing
even the scanner could be evaded; the **California EDD / ID.me** unemployment fraud, where automated
identity verification was defeated not by breaking the tech but by understanding the process around it
(verification is a gate, not a wall); **Bing "Sydney"**, where the rules were enforced in language
rather than code and leaked the moment someone asked the right way; a **rogue MCP server** proof of
concept against Cursor, where tool discovery became an instruction channel; and **anti-malware model
poisoning** (Kaspersky's neural-net research, and Skylight Cyber's bypass of a commercial ML detector),
where the training pipeline itself was the perimeter.

### The first-principles close
The wrap-up tied all of it to three properties of how models work: they optimise a **loss**, not
correctness; they **generalise**, they don't reason; and their **confidence** is a number produced by
training, not a measure of being right. Hold those three up against any attack from the week and it
falls out as a consequence rather than a surprise.

---

## A few framings I want to keep

- An attack isn't separate from the architecture — it's a trust assumption from the design being
  pushed on deliberately. Map the assumptions and you've mapped most of the attacks.
- Under attack, the model usually behaves *exactly as designed*. That's the problem, not a
  malfunction — there's no bug to fix because nothing broke.
- The system around the model doesn't repair the model's weaknesses. Retrieval, tools, automation,
  and scale take a weakness that was harmless in isolation and give it reach.
- Model artifacts are executable code. Loading an untrusted checkpoint is running an untrusted
  program.

---

## What I built this week

| Artifact | What it is | Where |
|---|---|---|
| Redrawn attack diagrams | My own versions of the week's core figures — the evasion decision-boundary gap, direct vs. indirect prompt injection through retrieval, the amplifier chain (how retrieval, tools, and A2A give one compromise reach), and the first-principles map (loss / generalisation / confidence → the attack each one enables) — drawn from my notes as SVGs, with PNG exports for publishing | [`./diagrams/`](./diagrams/) |
| Model-attack experiments | Ran the two model-level labs: a backdoor data-poisoning attack (a small white-square trigger that flips the model's output while clean accuracy stays high) and an FGSM evasion attack (watched confidence collapse as ε grew), and noted *why* each works rather than just that it does | _my own notes; the provided lab code isn't reproduced_ |
| System-attack experiments | Drove the same toy vacuum system through the system-level labs: retrieval poisoning (a blatant injected "manual" vs a subtle "community-verified best practice" one), a private-context exfiltration attempt, prompt-framing overrides, and an A2A propose→critique→arbitrate flow | _my own notes_ |
| Governance-collapse note | A write-up of the A2A task where the final action collapsed to a conservative default — not because the critic reasoned that the action was unsafe, but because its output didn't match the exact word the arbitration rule was checking for. Software governed; it just governed on a brittle string match | _my own notes_ |
| Soft-DoS cost note | Notes on why inference cost is input-dependent, and why this makes economic/latency DoS hard to catch with the uptime-style monitoring that worked for ordinary software | _my own notes_ |

> The cohort lab gave us the system and the attacks to run against it. What's here is my own redraws,
> my own notes on why each attack lands, and my own observations from actually running them. The lab
> code and the cohort's notebooks aren't reproduced.

---

## Questions I still have

- [ ] Indirect prompt injection: is there an actual *defence* end-to-end, or is the honest answer that
      it's only ever mitigated? If the model can't separate instructions from data, the fix can't live
      in the model — so where's the strongest place to enforce it?
- [ ] "Never load untrusted model artifacts" is correct, but is it *enforceable* across a team that
      pulls from Hugging Face daily? Does moving to SafeTensors actually close the seam, or just narrow it?
- [ ] Soft DoS: how do you set a cost ceiling that stops an adversarial prompt without breaking a
      legitimate heavy workload? Where does that limit even sit?

---

## Links & references

_Public sources only — no course material._

- [Goodfellow, Shlens & Szegedy (2014) — Explaining and Harnessing Adversarial Examples](https://arxiv.org/abs/1412.6572) — the FGSM paper and the panda→gibbon example.
- [CVE-2025-32711 (EchoLeak)](https://nvd.nist.gov/vuln/detail/CVE-2025-32711) — the zero-click M365 Copilot exfiltration found by Aim Labs.
- [Trail of Bits — Exploiting ML models with pickle file attacks](https://blog.trailofbits.com/2024/06/11/exploiting-ml-models-with-pickle-file-attacks-part-1/) — why loading a checkpoint can execute code.
- [JFrog — zero-day vulnerabilities in PickleScan](https://jfrog.com/blog/unveiling-3-zero-day-vulnerabilities-in-picklescan/) — even the scanner can be evaded.
- [Hugging Face — SafeTensors](https://github.com/huggingface/safetensors) — the safer serialization format the case study points to.
- [DOJ (USAO-EDCA) — sentencing in the California unemployment fraud scheme](https://www.justice.gov/usao-edca/pr/new-jersey-man-sentenced-675-years-prison-schemes-steal-california-unemployment) — automated verification defeated by understanding the process.
- [ID.me — fighting the new face of identity theft](https://network.id.me/article/fighting-the-new-face-of-identity-theft/) — the verifier's own account.
- [The Zvi — Sydney and Bing](https://thezvi.substack.com/p/ai-1-sydney-and-bing) — analysis of the early Bing chat prompt-leak incident.
- [Securelist — MCP abused in supply-chain attacks](https://securelist.com/model-context-protocol-for-ai-integration-abused-in-supply-chain-attacks/117473/) — rogue MCP server analysis.
- [CSO — rogue MCP servers can take over Cursor's built-in browser](https://www.csoonline.com/article/4089046/rogue-mcp-servers-can-take-over-cursors-built-in-browser.html) — the Cursor proof of concept.
- [Securelist — confusing anti-malware neural networks](https://securelist.com/how-to-confuse-antimalware-neural-networks-adversarial-attacks-and-protection/102949/) — Kaspersky on poisoning malware detectors.
- [Skylight Cyber — "Cylance, I Kill You"](https://skylightcyber.com/2019/07/18/cylance-i-kill-you/) — bypassing a commercial ML malware detector.
- [OWASP — Top 10 for LLM Applications](https://genai.owasp.org/) — prompt injection, data/model poisoning, excessive agency, unbounded consumption.
- [MITRE ATLAS](https://atlas.mitre.org/) — the adversarial-ML technique catalogue these attacks map onto.

---

## Boundary note

This summary is my own writing and my own diagrams. It doesn't reproduce the cohort's transcripts,
slides, lab code, or videos. The aim is to make the course look worth taking, not to stand in for it.
