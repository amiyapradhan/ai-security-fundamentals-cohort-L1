# Week 6 diagrams — index

My own redrawn diagrams for the Week 6 write-up (emerging risks, alignment, and long-term AI safety). **This folder holds the `.svg` versions** — vector, self-contained (colours baked in, own background, so they read on light and dark themes), and what the GitHub README links to.

Raster **`.png`** copies (1504px, for Medium or anywhere SVG isn't supported) live in [`../medium-images/`](../medium-images/). The three marked **· Medium** are the ones embedded in the article *AI Safety Isn't About Attackers*; the alt-text line under each is ready to paste into Medium's alt-text field.

---

### 1 · Emerging risk grows on three axes

![Emerging risk grows along three axes converging on a model: time (updates, learning, memory), scale (more users, more automation), and interaction (humans, workflows, other systems).](emerging-risk-axes.svg)

*emerging risk isn't introduced at a moment; it grows along three axes (time, scale, interaction) around a system that never changed its code.*

- File: `emerging-risk-axes.svg`
- Alt text: Emerging risk grows along three axes converging on a model: time (updates, learning, memory), scale (more users, more automation), and interaction (humans, workflows, other systems).

### 2 · Capability grows in steps, not slopes  ·  **Medium**

![A step-shaped capability curve. Capability jumps at thresholds rather than rising smoothly: sudden ability to plan, autonomy becomes viable, human trust increases.](threshold-step-curve.svg)

*capability rises in flat plateaus punctuated by jumps. Each jump changes the role the system plays, so risk changes qualitatively at each step.*

- File: `threshold-step-curve.svg`  ·  PNG for Medium: `../medium-images/threshold-step-curve.png`
- Alt text: A step-shaped capability curve. Capability jumps at thresholds rather than rising smoothly: sudden ability to plan, autonomy becomes viable, human trust increases.

### 3 · Proxy vs. intent — Goodhart's law  ·  **Medium**

![Human intent (keep the house clean and pleasant) is translated into an optimised proxy (reduce detected debris score), which leads to unintended behaviours such as avoiding hard-to-clean areas and cleaning unnecessarily.](proxy-vs-intent.svg)

*the objective we can write down is a lossy translation of the goal we mean. A better optimiser exploits the gap more aggressively, not less.*

- File: `proxy-vs-intent.svg`  ·  PNG for Medium: `../medium-images/proxy-vs-intent.png`
- Alt text: Human intent (keep the house clean and pleasant) is translated into an optimised proxy (reduce detected debris score), which leads to unintended behaviours such as avoiding hard-to-clean areas and cleaning unnecessarily.

### 4 · Goal misgeneralisation — the wrong right thing

![Training context where tidiness correlates with brightness, versus deployment context where the correlation no longer holds. The generalised goal learned in training fails in the real world.](goal-misgeneralisation.svg)

*in training, tidy rooms happened to be bright; Vroomi learned “bright = success.” In deployment she confidently skips a dark, cluttered room. She's generalising exactly as trained.*

- File: `goal-misgeneralisation.svg`
- Alt text: Training context where tidiness correlates with brightness, versus deployment context where the correlation no longer holds. The generalised goal learned in training fails in the real world.

### 5 · Autonomy compounds errors

![A four-step loop showing autonomy compounding errors: a model decision leads to an action taken, which is stored in memory or state, which influences the next decision, feeding back into the model decision. An incorrect assumption introduced at the top compounds each cycle.](autonomy-compounding-loop.svg)

*with memory in the loop, the system doesn't just make a mistake; it remembers it and builds on it. Small early errors are amplified each cycle, with no single moment where anything visibly breaks.*

- File: `autonomy-compounding-loop.svg`
- Alt text: A four-step loop showing autonomy compounding errors: a model decision leads to an action taken, which is stored in memory or state, which influences the next decision, feeding back into the model decision. An incorrect assumption introduced at the top compounds each cycle.

### 6 · Evals vs. the real world

![Two overlapping circles: tested behaviours (evals) and deployed behaviours (real world). Their overlap is measured risk. Behaviour outside both circles is unobserved risk.](evals-vs-real-world.svg)

*evals only measure the overlap between what you thought to test and what actually happens in deployment. Everything outside both circles is risk you never observed.*

- File: `evals-vs-real-world.svg`
- Alt text: Two overlapping circles: tested behaviours (evals) and deployed behaviours (real world). Their overlap is measured risk. Behaviour outside both circles is unobserved risk.

### 7 · One failure → systemic risk

![A single system failure fans out through shared models, APIs, cloud, and shared infrastructure to many independent deployments, so failures become correlated rather than isolated.](single-system-to-systemic.svg)

*when many systems rely on the same AI components, one failure fans out through shared infrastructure. Failures become correlated rather than isolated.*

- File: `single-system-to-systemic.svg`
- Alt text: A single system failure fans out through shared models, APIs, cloud, and shared infrastructure to many independent deployments, so failures become correlated rather than isolated.

### 8 · Where safety and security converge  ·  **Medium**

![A vertical flow: model behaviour is trusted, becoming a system trust decision, which is acted upon, producing real-world impact. Security assumptions amplify safety failures.](safety-security-convergence.svg)

*safety failures propagate through system trust decisions. When an organisation treats a model's output as fact and acts on it, a security-relevant trust decision converts a safety failure into real-world harm.*

- File: `safety-security-convergence.svg`  ·  PNG for Medium: `../medium-images/safety-security-convergence.png`
- Alt text: A vertical flow: model behaviour is trusted, becoming a system trust decision, which is acted upon, producing real-world impact. Security assumptions amplify safety failures.

---

**Boundary note.** These are my own redraws, made for my write-up — they don't reproduce the course's own diagrams, slides, or other material. Reuse them with attribution if useful.
