"""
Section 6.5 – Department
Probabilistic generation based on AI consultation (McKinsey, Deloitte),
SHRM benchmarks, and Eurostat R&D statistics.
No dictionaries used – values and weights are kept in separate lists.
"""

import random
from dotenv import load_dotenv
import os
load_dotenv()
n_samples = int(os.getenv("N_SAMPLES"))


DEPARTMENT_VALUES = [
    "Operations",
    "Sales / Commercial",
    "Technology / IT",
    "Customer Service",
    "Administration and Finance",
    "Human Resources",
    "Marketing",
    "Logistics",
    "R&D",
    "Legal",
    "Quality",
    "Procurement",
    "Communications / PR",
    "Security / Facilities",
    "General Management",
]

DEPARTMENT_WEIGHTS = [18, 15, 12, 10, 9, 6, 5, 5, 4, 3, 3, 3, 2, 3, 2]  # percentages, must sum to 100


def generate_department() -> str:
    """Return a single department sampled according to the defined distribution."""
    return random.choices(DEPARTMENT_VALUES, weights=DEPARTMENT_WEIGHTS, k=1)[0]


def generate_department_batch(n: int) -> list:
    """Return a list of n department values sampled according to the defined distribution."""
    return random.choices(DEPARTMENT_VALUES, weights=DEPARTMENT_WEIGHTS, k=n)


# ---------------------------------------------------------------------------
# Quick smoke-test: run this file directly to verify the distribution
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    SAMPLE_SIZE = n_samples

    results = generate_department_batch(SAMPLE_SIZE)

    print(f"Sample size: {SAMPLE_SIZE:,}\n")
    print(f"{'Department':<30} {'Count':>8}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 63)

    for value, weight in zip(DEPARTMENT_VALUES, DEPARTMENT_WEIGHTS):
        count = results.count(value)
        observed = count / SAMPLE_SIZE * 100
        print(f"{value:<30} {count:>8}  {observed:>9.2f}%  {weight:>9}%")