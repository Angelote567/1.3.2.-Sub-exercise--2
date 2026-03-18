"""
Appendix 12.1 – Social Security
Probabilistic generation for all percentage-based fields in the Social Security block.
Source: Professor's original code.
No dictionaries used – values and weights are kept in separate lists.

Fields:
    contribution_group   : Group 1 (Director) 5%, Group 2 (ICT) 70%, Group 3 (Admin) 25%
    withholding_rate_ss  : float between 4.0% and 8.0% (uniform distribution)
    applicable_bonuses   : No bonus 70%, Youth Employment Bonus 10%,
                           Disability Employment Incentive 8%,
                           Long-term Unemployment Reintegration Bonus 5%,
                           Temporary Government Program 7%
                           → stored as list[str]; empty list when no bonus applies
"""

import random
from dotenv import load_dotenv
import os
load_dotenv()
n_samples = int(os.getenv("N_SAMPLES"))


# ---------------------------------------------------------------------------
# Values and weights
# ---------------------------------------------------------------------------

CONTRIBUTION_GROUP_VALUES  = ["Group 1 (Director)", "Group 2 (ICT Department)", "Group 3 (Administration)"]
CONTRIBUTION_GROUP_WEIGHTS = [5, 70, 25]

WITHHOLDING_RATE_SS_MIN = 4.0
WITHHOLDING_RATE_SS_MAX = 8.0

APPLICABLE_BONUSES_VALUES  = [
    None,                                         # No bonus
    "Youth Employment Bonus",                     # age <= 30
    "Disability Employment Incentive",
    "Long-term Unemployment Reintegration Bonus",
    "Temporary Government Program",
]
APPLICABLE_BONUSES_WEIGHTS = [70, 10, 8, 5, 7]   # percentages, must sum to 100


# ---------------------------------------------------------------------------
# Individual generators
# ---------------------------------------------------------------------------

def generate_contribution_group() -> str:
    return random.choices(CONTRIBUTION_GROUP_VALUES, weights=CONTRIBUTION_GROUP_WEIGHTS, k=1)[0]


def generate_withholding_rate_ss() -> float:
    """Return a withholding rate uniformly distributed between 4.0% and 8.0%."""
    return round(random.uniform(WITHHOLDING_RATE_SS_MIN, WITHHOLDING_RATE_SS_MAX), 2)


def generate_applicable_bonuses() -> list:
    """Return a list with the applicable bonus, or an empty list when none applies."""
    bonus = random.choices(APPLICABLE_BONUSES_VALUES, weights=APPLICABLE_BONUSES_WEIGHTS, k=1)[0]
    return [bonus] if bonus is not None else []


# ---------------------------------------------------------------------------
# Batch generators
# ---------------------------------------------------------------------------

def generate_contribution_group_batch(n: int) -> list:
    return random.choices(CONTRIBUTION_GROUP_VALUES, weights=CONTRIBUTION_GROUP_WEIGHTS, k=n)


def generate_withholding_rate_ss_batch(n: int) -> list:
    return [generate_withholding_rate_ss() for _ in range(n)]


def generate_applicable_bonuses_batch(n: int) -> list:
    raw = random.choices(APPLICABLE_BONUSES_VALUES, weights=APPLICABLE_BONUSES_WEIGHTS, k=n)
    return [[v] if v is not None else [] for v in raw]


# ---------------------------------------------------------------------------
# Quick smoke-test: run this file directly to verify all distributions
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    SAMPLE_SIZE = n_samples

    print(f"Sample size: {SAMPLE_SIZE:,}\n")

    # contribution_group
    results = generate_contribution_group_batch(SAMPLE_SIZE)
    print(f"{'contribution_group':<45} {'Count':>8}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 78)
    for value, weight in zip(CONTRIBUTION_GROUP_VALUES, CONTRIBUTION_GROUP_WEIGHTS):
        count = results.count(value)
        print(f"  {value:<43} {count:>8}  {count/SAMPLE_SIZE*100:>9.2f}%  {weight:>9}%")

    # withholding_rate_ss
    print()
    rates = generate_withholding_rate_ss_batch(SAMPLE_SIZE)
    avg   = sum(rates) / SAMPLE_SIZE
    print(f"withholding_rate_ss  →  min: {min(rates):.2f}%  max: {max(rates):.2f}%  "
          f"avg: {avg:.2f}%  (expected range: {WITHHOLDING_RATE_SS_MIN}–{WITHHOLDING_RATE_SS_MAX}%)")

    # applicable_bonuses
    print()
    bonus_lists = generate_applicable_bonuses_batch(SAMPLE_SIZE)
    flat = [lst[0] if lst else None for lst in bonus_lists]
    print(f"{'applicable_bonuses':<45} {'Count':>8}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 78)
    labels   = ["No bonus"] + [v for v in APPLICABLE_BONUSES_VALUES if v is not None]
    expected = APPLICABLE_BONUSES_WEIGHTS
    for label, weight, raw_val in zip(labels, expected, APPLICABLE_BONUSES_VALUES):
        count = flat.count(raw_val)
        print(f"  {label:<43} {count:>8}  {count/SAMPLE_SIZE*100:>9.2f}%  {weight:>9}%")