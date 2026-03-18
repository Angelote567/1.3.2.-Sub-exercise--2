"""
Appendix 12.1 – OHS / OSH (Occupational Health and Safety)
Probabilistic generation for all percentage-based fields in the OHS block.
Source: Professor's original code.
No dictionaries used – values and weights are kept in separate lists.

Fields:
    osh_training_received : 97% True, 3% False
    ppe_issued            : 25% True, 75% False
    ppe_details           : conditional on ppe_issued=True
                              Basic PPE (gloves and boots)             60%
                              Standard PPE (helmet, gloves, vest)      30%
                              Full PPE (helmet, gloves, boots, vest)   10%
    medical_fitness       : Fit 93%, Restricted 6%, Unfit 1%
                            (original code values; see Section 6.7 for updated team values)
    osh_notes             : 10–15% of employees have notes, rest None
                            → midpoint 12% used here; adjust if needed
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

OSH_TRAINING_RECEIVED_WEIGHTS = [97, 3]
PPE_ISSUED_WEIGHTS            = [25, 75]

PPE_DETAILS_VALUES  = [
    "Basic PPE (gloves and boots)",
    "Standard PPE (helmet, gloves, vest)",
    "Full PPE (helmet, gloves, boots, vest)",
]
PPE_DETAILS_WEIGHTS = [60, 30, 10]

MEDICAL_FITNESS_VALUES  = ["Fit", "Restricted", "Unfit"]
MEDICAL_FITNESS_WEIGHTS = [93, 6, 1]

OSH_NOTES_WEIGHTS = [12, 88]   # 12% have notes, 88% None (midpoint of 10–15%)


# ---------------------------------------------------------------------------
# Individual generators
# ---------------------------------------------------------------------------

def generate_osh_training_received() -> bool:
    return random.choices(BOOL_VALUES, weights=OSH_TRAINING_RECEIVED_WEIGHTS, k=1)[0]


def generate_ppe_issued() -> bool:
    return random.choices(BOOL_VALUES, weights=PPE_ISSUED_WEIGHTS, k=1)[0]


def generate_ppe_details(ppe_issued: bool) -> str | None:
    """Return PPE details only if ppe_issued is True, otherwise None."""
    if not ppe_issued:
        return None
    return random.choices(PPE_DETAILS_VALUES, weights=PPE_DETAILS_WEIGHTS, k=1)[0]


def generate_medical_fitness() -> str:
    return random.choices(MEDICAL_FITNESS_VALUES, weights=MEDICAL_FITNESS_WEIGHTS, k=1)[0]


def generate_osh_notes() -> str | None:
    """Return a placeholder note string 12% of the time, None otherwise."""
    has_note = random.choices(BOOL_VALUES, weights=OSH_NOTES_WEIGHTS, k=1)[0]
    return "OHS note recorded." if has_note else None


# ---------------------------------------------------------------------------
# Batch generators
# ---------------------------------------------------------------------------

def generate_osh_training_received_batch(n: int) -> list:
    return random.choices(BOOL_VALUES, weights=OSH_TRAINING_RECEIVED_WEIGHTS, k=n)


def generate_ppe_issued_batch(n: int) -> list:
    return random.choices(BOOL_VALUES, weights=PPE_ISSUED_WEIGHTS, k=n)


def generate_ppe_details_batch(ppe_issued_list: list) -> list:
    """Return a list of PPE details aligned with a pre-generated ppe_issued list."""
    result = []
    for issued in ppe_issued_list:
        result.append(generate_ppe_details(issued))
    return result


def generate_medical_fitness_batch(n: int) -> list:
    return random.choices(MEDICAL_FITNESS_VALUES, weights=MEDICAL_FITNESS_WEIGHTS, k=n)


def generate_osh_notes_batch(n: int) -> list:
    has_notes = random.choices(BOOL_VALUES, weights=OSH_NOTES_WEIGHTS, k=n)
    return ["OHS note recorded." if h else None for h in has_notes]


# ---------------------------------------------------------------------------
# Quick smoke-test: run this file directly to verify all distributions
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    SAMPLE_SIZE = n_samples

    print(f"Sample size: {SAMPLE_SIZE:,}\n")

    # osh_training_received
    results = generate_osh_training_received_batch(SAMPLE_SIZE)
    print(f"{'osh_training_received':<30} {'Value':<6} {'Count':>8}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 70)
    for value, weight in zip(BOOL_VALUES, OSH_TRAINING_RECEIVED_WEIGHTS):
        count = results.count(value)
        print(f"{'':30} {str(value):<6} {count:>8}  {count/SAMPLE_SIZE*100:>9.2f}%  {weight:>9}%")

    # ppe_issued
    print()
    ppe_issued_results = generate_ppe_issued_batch(SAMPLE_SIZE)
    print(f"{'ppe_issued':<30} {'Value':<6} {'Count':>8}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 70)
    for value, weight in zip(BOOL_VALUES, PPE_ISSUED_WEIGHTS):
        count = ppe_issued_results.count(value)
        print(f"{'':30} {str(value):<6} {count:>8}  {count/SAMPLE_SIZE*100:>9.2f}%  {weight:>9}%")

    # ppe_details (only among records where ppe_issued=True)
    print()
    ppe_details_results = generate_ppe_details_batch(ppe_issued_results)
    issued_count = ppe_issued_results.count(True)
    print(f"{'ppe_details (ppe_issued=True only)':<38} {'Count':>8}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 70)
    for value, weight in zip(PPE_DETAILS_VALUES, PPE_DETAILS_WEIGHTS):
        count = ppe_details_results.count(value)
        print(f"  {value:<36} {count:>8}  {count/issued_count*100:>9.2f}%  {weight:>9}%")

    # medical_fitness
    print()
    results = generate_medical_fitness_batch(SAMPLE_SIZE)
    print(f"{'medical_fitness':<30} {'Value':<12} {'Count':>8}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 75)
    for value, weight in zip(MEDICAL_FITNESS_VALUES, MEDICAL_FITNESS_WEIGHTS):
        count = results.count(value)
        print(f"{'':30} {value:<12} {count:>8}  {count/SAMPLE_SIZE*100:>9.2f}%  {weight:>9}%")

    # osh_notes
    print()
    results = generate_osh_notes_batch(SAMPLE_SIZE)
    has_note = sum(1 for v in results if v is not None)
    no_note  = SAMPLE_SIZE - has_note
    print(f"{'osh_notes':<30} {'Value':<10} {'Count':>8}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 70)
    print(f"{'':30} {'has note':<10} {has_note:>8}  {has_note/SAMPLE_SIZE*100:>9.2f}%  {'12':>9}%")
    print(f"{'':30} {'None':<10} {no_note:>8}  {no_note/SAMPLE_SIZE*100:>9.2f}%  {'88':>9}%")