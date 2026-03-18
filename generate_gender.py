"""
Section 6.4 – Gender
Probabilistic generation based on Eurostat: Employment by sex /
ILO Global Employment Trends / McKinsey & Deloitte diversity surveys.
No dictionaries used – values and weights are kept in separate lists.
"""

import random
from dotenv import load_dotenv
import os
load_dotenv()
n_samples = int(os.getenv("N_SAMPLES"))

GENDER_VALUES = [
    "Male",
    "Female",
    "Non-binary / Other",
    "Prefer not to say",
]

GENDER_WEIGHTS = [48, 50, 1, 1]  # percentages, must sum to 100


def generate_gender() -> str:
    """Return a single gender value sampled according to the defined distribution."""
    return random.choices(GENDER_VALUES, weights=GENDER_WEIGHTS, k=1)[0]


def generate_gender_batch(n: int) -> list:
    """Return a list of n gender values sampled according to the defined distribution."""
    return random.choices(GENDER_VALUES, weights=GENDER_WEIGHTS, k=n)


# ---------------------------------------------------------------------------
# Quick smoke-test: run this file directly to verify the distribution
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    SAMPLE_SIZE = n_samples

    results = generate_gender_batch(SAMPLE_SIZE)

    print(f"Sample size: {SAMPLE_SIZE:,}\n")
    print(f"{'Gender':<25} {'Count':>8}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 58)

    for value, weight in zip(GENDER_VALUES, GENDER_WEIGHTS):
        count = results.count(value)
        observed = count / SAMPLE_SIZE * 100
        print(f"{value:<25} {count:>8}  {observed:>9.2f}%  {weight:>9}%")