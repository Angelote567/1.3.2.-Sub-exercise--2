"""
Section 6.1 - Marital Status (Estado Civil)
HR Synthetic Database - Universidad San Jorge

Distribution based on:
- Eurostat: EU Labour Force Survey
- OIT / UN Demographic Yearbook

Values and weights:
    Single       35%
    Married        45%
    Divorced    12%
    Widowed          5%
    Cohabiting   3%
"""

import random
from dotenv import load_dotenv
import os
load_dotenv()
n_samples = int(os.getenv("N_SAMPLES"))


# --- Data (no dicts: parallel lists) ---

MARITAL_VALUES = [
    "Single",
    "Married",
    "Divorced",
    "Widowed",
    "Cohabiting",
]

MARITAL_WEIGHTS = [35, 45, 12, 5, 3]  # Must sum to 100


# --- Generator function ---

def generate_marital_status() -> str:
    """
    Returns a single marital status value sampled
    according to the defined percentage distribution.
    """
    return random.choices(MARITAL_VALUES, weights=MARITAL_WEIGHTS, k=1)[0]


def generate_marital_status_batch(n: int) -> list[str]:
    """
    Returns a list of n marital status values sampled
    according to the defined percentage distribution.

    Args:
        n: Number of records to generate.

    Returns:
        List of n marital status strings.
    """
    return random.choices(MARITAL_VALUES, weights=MARITAL_WEIGHTS, k=n)


# --- Quick validation ---

if __name__ == "__main__":
    SAMPLE_SIZE = n_samples 

    results = generate_marital_status_batch(SAMPLE_SIZE)

    print(f"Sample size: {SAMPLE_SIZE:,}\n")
    print(f"{'Value':<20} {'Expected':>10} {'Observed':>10}")
    print("-" * 42)

    for value, weight in zip(MARITAL_VALUES, MARITAL_WEIGHTS):
        observed = results.count(value) / SAMPLE_SIZE * 100
        print(f"{value:<20} {weight:>9}%  {observed:>9.2f}%")

    print("\nSingle record example:", generate_marital_status())
