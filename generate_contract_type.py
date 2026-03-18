"""
Section 6.2 – Contract Type
Probabilistic generation based on Eurostat: Labour Market Statistics /
Ministry of Labour / EU Directives on contracts.
No dictionaries used – values and weights are kept in separate lists.
"""

import random
from dotenv import load_dotenv
import os
load_dotenv()
n_samples = int(os.getenv("N_SAMPLES"))


CONTRACT_TYPE_VALUES = [
    "Permanent",
    "Temporary",
    "Internship / Training",
    "Project-based",
]

CONTRACT_TYPE_WEIGHTS = [65, 25, 7, 3]  # percentages, must sum to 100


def generate_contract_type() -> str:
    """Return a single contract type sampled according to the defined distribution."""
    return random.choices(CONTRACT_TYPE_VALUES, weights=CONTRACT_TYPE_WEIGHTS, k=1)[0]


def generate_contract_type_batch(n: int) -> list:
    """Return a list of n contract type values sampled according to the defined distribution."""
    return random.choices(CONTRACT_TYPE_VALUES, weights=CONTRACT_TYPE_WEIGHTS, k=n)


# ---------------------------------------------------------------------------
# Quick smoke-test: run this file directly to verify the distribution
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    SAMPLE_SIZE = n_samples

    results = generate_contract_type_batch(SAMPLE_SIZE)

    print(f"Sample size: {SAMPLE_SIZE:,}\n")
    print(f"{'Contract Type':<25} {'Count':>8}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 58)

    for value, weight in zip(CONTRACT_TYPE_VALUES, CONTRACT_TYPE_WEIGHTS):
        count = results.count(value)
        observed = count / SAMPLE_SIZE * 100
        print(f"{value:<25} {count:>8}  {observed:>9.2f}%  {weight:>9}%")