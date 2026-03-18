"""
Appendix 12.1 – Resources
Probabilistic generation for all percentage-based fields in the Resources block.
Source: Professor's original code (INE ICT Companies Survey 2024 / Eurostat).
No dictionaries used – values and weights are kept in separate lists.

Fields:
    laptop_assigned       : 68.4% True, 31.6% False  (source: INE ICT Survey 2024)
    mobile_phone_assigned : 80%   True, 20%   False  (source: Survey basis)
    access_card_assigned  : 95%   True, 5%    False  (source: Survey basis)
"""

import random
from dotenv import load_dotenv
import os
load_dotenv()
n_samples = int(os.getenv("N_SAMPLES"))


# ---------------------------------------------------------------------------
# Values and weights
# ---------------------------------------------------------------------------

BOOL_VALUES = [True, False]

LAPTOP_ASSIGNED_WEIGHTS       = [68.4, 31.6]
MOBILE_PHONE_ASSIGNED_WEIGHTS = [80,   20]
ACCESS_CARD_ASSIGNED_WEIGHTS  = [95,   5]


# ---------------------------------------------------------------------------
# Individual generators
# ---------------------------------------------------------------------------

def generate_laptop_assigned() -> bool:
    return random.choices(BOOL_VALUES, weights=LAPTOP_ASSIGNED_WEIGHTS, k=1)[0]


def generate_mobile_phone_assigned() -> bool:
    return random.choices(BOOL_VALUES, weights=MOBILE_PHONE_ASSIGNED_WEIGHTS, k=1)[0]


def generate_access_card_assigned() -> bool:
    return random.choices(BOOL_VALUES, weights=ACCESS_CARD_ASSIGNED_WEIGHTS, k=1)[0]


# ---------------------------------------------------------------------------
# Batch generators
# ---------------------------------------------------------------------------

def generate_laptop_assigned_batch(n: int) -> list:
    return random.choices(BOOL_VALUES, weights=LAPTOP_ASSIGNED_WEIGHTS, k=n)


def generate_mobile_phone_assigned_batch(n: int) -> list:
    return random.choices(BOOL_VALUES, weights=MOBILE_PHONE_ASSIGNED_WEIGHTS, k=n)


def generate_access_card_assigned_batch(n: int) -> list:
    return random.choices(BOOL_VALUES, weights=ACCESS_CARD_ASSIGNED_WEIGHTS, k=n)


# ---------------------------------------------------------------------------
# Quick smoke-test: run this file directly to verify all distributions
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    SAMPLE_SIZE = n_samples

    fields = [
        ("laptop_assigned",        generate_laptop_assigned_batch,        LAPTOP_ASSIGNED_WEIGHTS),
        ("mobile_phone_assigned",  generate_mobile_phone_assigned_batch,  MOBILE_PHONE_ASSIGNED_WEIGHTS),
        ("access_card_assigned",   generate_access_card_assigned_batch,   ACCESS_CARD_ASSIGNED_WEIGHTS),
    ]

    print(f"Sample size: {SAMPLE_SIZE:,}\n")
    print(f"{'Field':<26} {'Value':<6} {'Count':>8}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 65)

    for field_name, batch_fn, weights in fields:
        results = batch_fn(SAMPLE_SIZE)
        for value, weight in zip(BOOL_VALUES, weights):
            count = results.count(value)
            print(f"{field_name:<26} {str(value):<6} {count:>8}  {count/SAMPLE_SIZE*100:>9.2f}%  {weight:>9}%")
        print()