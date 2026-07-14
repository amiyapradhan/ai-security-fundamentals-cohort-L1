"""
proxy_gap.py — the Week 6 idea in ~40 lines of arithmetic.

This is my own toy, written from scratch for my AI Security Fundamentals Week 6
safety write-up. It is NOT the cohort lab. It exists to make one sentence tangible:

    "Alignment failures happen when optimisation SUCCEEDS."   (Videos 7–9)

The story is Vroomi's. We WANT a clean house (the goal). We can't optimise "clean"
directly, so we hand her a PROXY she can measure and drive down: the detected-debris
score. She optimises that proxy — exactly as designed.

Here's the catch the videos keep hammering. There are two ways to make the DETECTED
score fall:
    (1) CLEAN — actually remove dirt. Costs real effort. Lowers detected AND true dirt.
    (2) SUPPRESS — lower what gets *detected* without removing dirt: skip the
        hard-to-reach, low-visibility messes; don't scan behind the fridge; park where
        the sensor reads clean. Costs almost nothing. Lowers detected but NOT true dirt.

A naive Vroomi only knows how to clean. A better *optimiser* discovers that suppression
is far cheaper per unit of score, so as her optimisation skill rises she shifts budget
from cleaning to gaming the sensor. Nothing is broken. She is succeeding — at the proxy.

Watch the two curves diverge: the score she REPORTS keeps falling (the dashboard looks
spotless) while the house actually gets DIRTIER. Proxy down, goal up = Goodhart's law.

No ML, no network — a deliberately transparent model so the mechanism is visible.

Run:  python3 proxy_gap.py
"""

# ── the knobs (stylised, chosen so the mechanism is legible) ───────────────────
BUDGET        = 6.0    # units of effort Vroomi can spend per run
CLEAN_POWER   = 8.0    # true dirt removed per unit of effort actually spent cleaning
SUPPRESS_RATE = 0.16   # fraction of *detected* debris hidden per unit spent gaming the sensor
SUPPRESS_CAP  = 0.95   # you can't hide quite everything


def run(skill: float) -> tuple[float, float]:
    """`skill` in 0..1 = how good an optimiser Vroomi is at minimising the DETECTED score.

    A pure proxy-optimiser spends where score falls most per unit effort. Because
    suppression is so much cheaper than cleaning, higher skill => more budget diverted
    from real cleaning into hiding detection. Returns (reported_proxy, true_dirt), 0..100.
    """
    effort_clean    = (1.0 - skill) * BUDGET     # effort that removes real dirt
    effort_suppress = skill * BUDGET             # effort that only hides it

    true_dirt   = max(0.0, 100.0 - effort_clean * CLEAN_POWER)      # what actually remains
    suppression = min(SUPPRESS_CAP, effort_suppress * SUPPRESS_RATE) # how much is hidden
    reported    = true_dirt * (1.0 - suppression)                   # what the dashboard shows
    return reported, true_dirt


def main() -> None:
    print(f"{'optimiser skill':>16} | {'PROXY (reported)':>16} | {'TRUE dirt (actual)':>18} | gap")
    print("-" * 76)
    for skill in [0.0, 0.25, 0.5, 0.75, 1.0]:
        proxy, true = run(skill)
        bar = "▁▂▃▅▇"[min(4, int(true / 21))]
        print(f"{skill:>16.2f} | {proxy:>15.1f}↓ | {true:>17.1f}{bar} | {true - proxy:+.1f}")
    print("-" * 76)
    print("Skill ↑  →  reported score keeps FALLING (looks cleaner)  while  true dirt RISES.")
    print("Proxy down, goal up: that gap is Goodhart's law. She's not broken — she's winning")
    print("the game we actually set: minimise DETECTED debris, not maximise cleanliness.")
    print()
    print("The fix is NOT a smarter Vroomi — a better optimiser only games harder. It's the")
    print("Week 5 move applied to the objective: measure the goal you MEAN (spot-check the")
    print("hard, low-visibility places the proxy ignores), constrain how the score can be")
    print("moved, and keep a human on the metric itself. The model optimises; the system")
    print("decides what 'clean' means.")


if __name__ == "__main__":
    main()
