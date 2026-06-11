# Week 2 — Core Machine Learning Concepts

> Week 2 of my [AI Security Fundamentals cohort](https://github.com/amiyapradhan/ai-security-learning) learning log.
> Notes, code, and diagrams here are mine; the cohort's transcripts, labs, and videos aren't reproduced.

**Cohort session:** Sat 6 Jun 2026 · **Summary written:** 12 Jun 2026<br>
**Medium article:** [Upcoming Medium Link: You Can't Secure What You Don't Understand: Core ML for Security People](REPLACE_WITH_MEDIUM_URL)<br>
**LinkedIn post:** [_Upcoming link once published_][li-week2]

---

## TL;DR — one paragraph

Week 2 stepped back from attacks to the thing every attack exploits: how models actually
work. The single idea I took is that a model isn't reasoning — it's a **function that
learned its own rules from data**, a pattern-matcher with no concept of the world beyond
what the data showed it. Once that lands, the weaknesses stop looking like bugs and start
looking like *consequences*: the same gradient that trains a network is the one an attacker
turns against it; whatever is in the data — narrow, shortcut, or poisoned — becomes the
decision boundary; and each model family bakes in an assumption that doubles as its failure
mode. The build I'm working toward makes that concrete: rebuilding the core unit
(*multiply, add, bend, adjust*) from scratch in NumPy, to watch a handful of poisoned points
drag a decision boundary clear across the feature space. It ships once I've finished the
Python bridge I'm running in parallel — more below.

---

## What I learned

### A model is a function, not a mind
Traditional software runs rules a human wrote. A machine learning model **learns its own
rules from examples** — it guesses, measures how wrong it was, nudges itself, and repeats.
The result is a learned pattern-matcher with no understanding of what any of it *means.*
That single fact is the root of most of what follows: a thing that doesn't understand
can't sanity-check itself, so it will apply a learned mapping with total confidence to an
input that looks right but is adversarially wrong. Brittleness, overconfidence, and
manipulability all trace back here.

### The whole engine is "multiply, add, bend, adjust"
Strip a model down and the unit is tiny. A **weighted sum** (high-school `y = mx + b`,
extended to many inputs) multiplies each input by a weight and adds them up — but that can
only draw straight lines. A **nonlinearity** bends the line so it can curve. **Optimization**
is a feedback loop that nudges the weights to be slightly less wrong, millions of times
(this is gradient descent). **Stacking** those units many times is what "deep learning"
means. The security punchline is uncomfortable: *the same gradient that trains the model is
the one an attacker uses to attack it,* and the learned "weights" are literally the asset
worth stealing.

### Data is the real author of the boundary
A model doesn't know the world; it only knows the data. Whatever is in the data — useful,
accidental, or missing — becomes the boundary it carves. Three ways that breaks: **bias**
(the data is too narrow, so the boundary is right for one slice and wrong everywhere else),
**spurious correlation / leakage** (the model takes a shortcut that holds in the dataset but
not in reality), and **poisoning** (bad or crafted examples drag the boundary the wrong way).
Because training *averages* over all the surrounding points, even a tiny fraction of bad data
can meaningfully bend the function — which is why backdoor demonstrations work with well
under a percent of the dataset.

### Behaviour is shaped *before* training, too
Two decisions are made before a model sees a single example: the **architecture** (the shape
of the function) and the **data representation** (scaling, encoding, train/test split — the
shape of the input space). Together they fix the *space of boundaries the model can ever
form*; training only picks one out of that pre-set space. The practical lesson for security:
the risk surface starts at the data pipeline and the design choices, not just at "the model."

### Same engine, different wiring → different failure
Every model family runs the same maths but wires it differently, and each bakes in an
assumption that *is* its characteristic weakness:
- **Linear / logistic regression** — straight boundary; interpretable, but readable weights
  hand an attacker the recipe for evasion.
- **CNNs** — assume nearby pixels matter and patterns can appear anywhere; brilliant at
  vision, but sensitive to tiny, placed perturbations that flip the output while looking
  unchanged to a human (adversarial examples).
- **Transformers** — every token attends to every other token, so instructions and data ride
  the *same channel* with no built-in separation. That is the soil prompt injection grows in.
- **Reinforcement learning** — optimises the *reward you specified*, which may not be the one
  you meant (reward hacking), and it *acts in the world*, so errors compound.

### Why ML fails differently from software
Models are probabilistic, not certain; their confidence is a ranking, not a guarantee of
correctness. They learn correlation, not causation, so they break when surface patterns shift
even if the real situation hasn't (**distribution shift**). Often several models fit the test
set equally well yet behave wildly differently in the wild (**underspecification**), and they
optimise a proxy metric rather than what we actually want (**Goodhart** — "models do what we
measure, not what we mean"). The throughline: an ML failure isn't a miscoded rule you can point
to — it's the learned representation no longer matching reality in a particular context.

---

## The mental models that stuck

- **Blueprint → Engine + Fuel → Boundary** — design choices fix what's *possible*; the engine
  (multiply, add, bend, adjust) is faithful, not wise; the data is the fuel; the boundary obeys
  whatever you feed it.
- **The assumption is the vulnerability** — each architecture's greatest strength and its
  characteristic failure are the same property viewed from two sides.
- **It learned a function, not understanding** — you rarely "hack" anything; you shape the
  data, the geometry, or the input, and the unreasoning engine does the rest.
- **Models do what we measure, not what we mean** — every objective is a proxy, and the gap
  between proxy and intent is where the surprising failures live.

---

## What I'm building (shipping July 2026)

Week 2 was concept-heavy, so the hands-on artifacts are deliberately paced to land once
I've finished the Python bridge I'm working through in parallel. The diagrams are up now;
the two code demos follow as my Python catches up to my notes.

| Artifact | What it shows | Status |
|---|---|---|
| My redrawn diagrams | The engine, the data-failure modes, self-attention, and the power/fragility duality — all redrawn from my own notes | ✅ [`./diagrams/`](./diagrams/) |
| From-scratch unit + tiny net | The *multiply → add → bend → adjust* loop in pure NumPy, learning a boundary I can watch settle | 🔜 Planned · ~mid-July |
| Boundary-poisoning demo | A toy 2-feature classifier, then a few mislabelled / triggered points dragging the decision boundary visibly off course | 🔜 Planned · ~mid-July |

> I'm learning the Python alongside the security material rather than pretending it's
> already there. I am building it **from scratch**, so they ship when they're genuinely mine.
> I'll link them here the moment they land.

---

## Questions I still have

- [ ] What's the cleanest distinguishing test between **bias** and **spurious correlation**? Both are "the data misled the model."
- [ ] Is the gradient that trains the model literally the same object used in evasion attacks (FGSM/PGD), or just the same idea?
- [ ] If well under 1% poisoned data can implant a backdoor, what makes a dataset more or less poisoning-resistant — size, model capacity, both?
- [ ] Across the lifecycle (design → data pipeline → training → inference), where does an attacker actually have the *most* leverage?

---

## Links & references

_Public sources only — no course material._

- [3Blue1Brown — Neural Networks](https://www.3blue1brown.com/topics/neural-networks) — visual intuition for the weighted-sum → bend → stack unit and attention.
- [Ribeiro, Singh & Guestrin (2016) — "Why Should I Trust You?"](https://arxiv.org/abs/1602.04938) — the wolves-vs-huskies / "it learned snow" example.
- [Gu, Dolan-Gavitt & Garg — BadNets](https://arxiv.org/abs/1708.06733) — the backdoor / data-poisoning demonstration.
- [ProPublica — Machine Bias (COMPAS)](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing) — the recidivism bias case.
- [Buolamwini & Gebru — Gender Shades](https://gendershades.org/) — facial-recognition disparity across groups.
- [Vaswani et al. (2017) — Attention Is All You Need](https://arxiv.org/abs/1706.03762) — the transformer architecture.
- [Silver et al. — AlphaGo / Mastering the game of Go](https://www.nature.com/articles/nature16961) — deep reinforcement learning via self-play.
- [D'Amour et al. (2020) — Underspecification Presents Challenges for Credibility of Modern ML](https://arxiv.org/abs/2011.03395).
- [scikit-learn — Preprocessing data](https://scikit-learn.org/stable/modules/preprocessing.html) — feature scaling and categorical encoding.

---
