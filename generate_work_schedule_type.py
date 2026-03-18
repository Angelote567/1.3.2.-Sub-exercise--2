"""
Section 6.3 – Work Schedule Type
Probabilistic generation based on Eurostat: Full-time and part-time employment / ILO.
No dictionaries used – values and weights are kept in separate lists.
"""

import random
from dotenv import load_dotenv
import os
load_dotenv()
n_samples = int(os.getenv("N_SAMPLES"))


WORK_SCHEDULE_VALUES = [
    "Full-time",
    "Part-time",
]

WORK_SCHEDULE_WEIGHTS = [78, 22]  # percentages, must sum to 100


def generate_work_schedule() -> str:
    """Return a single work schedule type sampled according to the defined distribution."""
    return random.choices(WORK_SCHEDULE_VALUES, weights=WORK_SCHEDULE_WEIGHTS, k=1)[0]


def generate_work_schedule_batch(n: int) -> list:
    """Return a list of n work schedule values sampled according to the defined distribution."""
    return random.choices(WORK_SCHEDULE_VALUES, weights=WORK_SCHEDULE_WEIGHTS, k=n)


# ---------------------------------------------------------------------------
# Quick smoke-test: run this file directly to verify the distribution
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    SAMPLE_SIZE = n_samples

    results = generate_work_schedule_batch(SAMPLE_SIZE)

    print(f"Sample size: {SAMPLE_SIZE:,}\n")
    print(f"{'Work Schedule':<15} {'Count':>8}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 48)

    for value, weight in zip(WORK_SCHEDULE_VALUES, WORK_SCHEDULE_WEIGHTS):
        count = results.count(value)
        observed = count / SAMPLE_SIZE * 100
        print(f"{value:<15} {count:>8}  {observed:>9.2f}%  {weight:>9}%")