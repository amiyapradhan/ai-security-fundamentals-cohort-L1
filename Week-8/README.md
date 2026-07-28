# Week 8: Bringing It All Together (Course Finale)

> Final module of my [AI Security Fundamentals cohort](https://aisecurityfundamentals.com) log. My notes only; no cohort transcripts, slides, or lab reproduced.
> **No new lab this week.** It's a consolidation module, and the Vroomi capstone (Weeks 7 and 8) is written up in my [Week 7 log](https://github.com/amiyapradhan/ai-security-fundamentals-cohort-L1/tree/main/Week-7).

**Medium:** [AI Security Isn't a Technical Problem. It's an Organisational One](REPLACE_WITH_MEDIUM_URL) <br>
**LinkedIn:** [link once live](REPLACE_WITH_LINKEDIN_URL)

---

## TL;DR

Weeks 1 to 7 built the technical pieces. Week 8 adds almost no new vocabulary; its job is to make everything
portable. Two lines carry it. One: it was always the system, not the model. Two, the one I underrated all
course: AI security is an organisational problem, not just a technical one. A business risk to be
communicated, owned, and managed. The mindset shift underneath both is from "is the model accurate?" to "is
the system reliable, safe, and resilient when its assumptions break?" You stop analysing models and start
evaluating systems.

## What I learned

- **It's the whole system.** Risk emerges from how data, interfaces, retrieval, and decision logic interact. The shift is accuracy to reliability, safety, and resilience.
- **Communicating risk is a control.** Frame every failure as financial, safety, reputational, or compliance risk, then tailor the depth to the audience.
- **A programme is progress, not perfection.** Visibility, then basic policies, then named ownership, then quick wins. Mature it from there.
- **The questions beat the answers.** Interrogate data, inputs, outputs, users, integration. Surface the assumptions, then ask what happens when they break.
- **Operationalising is adaptation, not adoption.** Don't build something new; embed NIST/ISO/OWASP into the SDLC and risk processes you already run.
- **Deployment is the start.** Monitor behaviour and user feedback, watch for signals, run a response loop that feeds every incident back into stronger controls.
- **The consultant's value is questions, not expertise.** Convene the right people, ask across boundaries, translate tech to business, stay comfortable with ambiguity.
- **Frameworks fail from application, not content.** Over-complexity, no integration, unclear ownership, docs over behaviour, applied too late, treated as static.
- **Four case studies, four maturities.** JPMorgan (integration), Samsung (reactive to structured), Microsoft (designed-in lifecycle), Anthropic (safety-first inside commercial constraints).
- **Mental models to keep.** Models learn patterns, not truth. AI fails silently, not loudly. Weakness spans data, context, and interfaces. Security is about assumptions and what breaks them. Tools don't secure systems; system design does.
- **AI and society.** Safety, security, and ethics interlock and scale to populations. The slow risk is gradual disempowerment. If you're in the room, you're shaping it.

## Field kit (what replaces the lab)

No build this week, so I turned the module into a reference I can pull up in a real review. All reworded from the module for my own use.

**Frame any failure as one of four business risks:**

| Risk | How to say it in the room |
|---|---|
| **Financial** | "This error is wired into pricing and approvals, so one wrong call at scale is real money." |
| **Safety** | "A wrong output here can drive a harmful decision, and tolerance for that is near zero." |
| **Reputational** | "This is user-facing. A bad answer spreads publicly before the incident report is written." |
| **Compliance** | "Even working perfectly, deploying it here without the right data handling is legal exposure." |

**Translate the finding into a consequence:**

| To an engineer | To the business |
|---|---|
| "Vulnerable to prompt injection." | "Someone could make it take an action we never intended, like approving a refund or exposing customer data." |
| "The system is probabilistic." | "Usually right, not always, and it sounds confident when wrong. It can look fine while being wrong." |
| "Unvalidated tool execution." | "It acts on its own output with nothing checking first, so a bad output becomes a bad action automatically." |

Then close on a framed trade-off, not a lecture: *"Deploy as-is and accept this risk, or add a control that
reduces it but slows things slightly."* Two named options; the business owns the call.

**The five questions:** for data, inputs, outputs, users, and integration, ask what happens when the
assumption (trustworthy data, well-behaved users, correct outputs, a checkpoint before action) breaks.

**Programme build order:** visibility, then policies, then ownership, then quick wins, then mature it
(standardise, deepen testing, monitor, integrate, look ahead).

## Questions I still have

- **Prioritising assumptions.** A real system has thousands. Do you only chase the ones on paths that touch high-impact actions, and how do you know you found the one that matters?
- **Catching silent failure.** What's the minimum monitoring that would actually detect a slow degradation (summaries quietly dropping 3% of critical info) before it becomes an incident?
- **The consultant without authority.** You surface a risk, frame the trade-off cleanly, and the business takes the risky option anyway. Where does responsibility actually sit?

## References

Public sources only; case-study characterisations rest on public reporting, as the module itself flags.
[NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) ·
[ISO/IEC 42001](https://www.iso.org/standard/42001) ·
[NIST CSF 2.0](https://www.nist.gov/cyberframework) ·
[OWASP Top 10 for LLMs](https://genai.owasp.org/) ·
[OWASP AIVSS](https://aivss.owasp.org/) ·
[NCSC Secure AI Development](https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development) ·
[MITRE ATLAS](https://atlas.mitre.org/) ·
[EU AI Act](https://artificialintelligenceact.eu/) ·
[Microsoft Responsible AI](https://www.microsoft.com/en-us/ai/responsible-ai) ·
[Anthropic Constitutional AI](https://www.anthropic.com/research)

---

_My own writing and a small from-scratch field kit. Doesn't reproduce cohort transcripts, slides, notebooks, or videos._
