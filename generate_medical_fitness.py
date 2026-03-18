"""
Section 6.7 – Medical Fitness
Probabilistic generation based on EU-OSHA and INSST statistics.
No dictionaries used – values and weights are kept in separate lists.

Note: these percentages differ slightly from the OHS/OSH block in Appendix 12.1
(Fit 93% / Restricted 6% / Unfit 1%). Section 6.7 is the updated distribution
agreed by the team: Fit 88%, Fit with restrictions 9%, Unfit 2%, Pending review 1%.
"""

import random
from dotenv import load_dotenv
import os
load_dotenv()
n_samples = int(os.getenv("N_SAMPLES"))


MEDICAL_FITNESS_VALUES = [
    "Fit",
    "Fit with restrictions",
    "Unfit",
    "Pending review",
]

MEDICAL_FITNESS_WEIGHTS = [88, 9, 2, 1]  # percentages, must sum to 100


def generate_medical_fitness() -> str:
    """Return a single medical fitness status sampled according to the defined distribution."""
    return random.choices(MEDICAL_FITNESS_VALUES, weights=MEDICAL_FITNESS_WEIGHTS, k=1)[0]


def generate_medical_fitness_batch(n: int) -> list:
    """Return a list of n medical fitness values sampled according to the defined distribution."""
    return random.choices(MEDICAL_FITNESS_VALUES, weights=MEDICAL_FITNESS_WEIGHTS, k=n)


# ---------------------------------------------------------------------------
# Quick smoke-test: run this file directly to verify the distribution
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    SAMPLE_SIZE = n_samples

    results = generate_medical_fitness_batch(SAMPLE_SIZE)

    print(f"Sample size: {SAMPLE_SIZE:,}\n")
    print(f"{'Medical Fitness':<25} {'Count':>8}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 58)

    for value, weight in zip(MEDICAL_FITNESS_VALUES, MEDICAL_FITNESS_WEIGHTS):
        count = results.count(value)
        observed = count / SAMPLE_SIZE * 100
        print(f"{value:<25} {count:>8}  {observed:>9.2f}%  {weight:>9}%")