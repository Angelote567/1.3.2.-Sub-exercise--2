"""
Appendix 12.1 – Documentation
Probabilistic generation for all boolean fields in the Documentation block.
Source: Professor's original code.
No dictionaries used – values and weights are kept in separate lists.

Fields:
    contract_signed         : 100% True
    id_copy                 : 98% True, 2% False
    resume_cv               : 98% True, 2% False
    gdpr_policies_signed    : 100% True
    code_of_ethics_signed   : 100% True
    osh_informed            : 100% True
    image_use_authorization : 55% True, 45% False
"""

import random
from dotenv import load_dotenv
import os
load_dotenv()
n_samples = int(os.getenv("N_SAMPLES"))



# ---------------------------------------------------------------------------
# Values and weights – one pair per field
# ---------------------------------------------------------------------------

BOOL_VALUES = [True, False]

CONTRACT_SIGNED_WEIGHTS          = [100, 0]
ID_COPY_WEIGHTS                  = [98, 2]
RESUME_CV_WEIGHTS                = [98, 2]
GDPR_POLICIES_SIGNED_WEIGHTS     = [100, 0]
CODE_OF_ETHICS_SIGNED_WEIGHTS    = [100, 0]
OSH_INFORMED_WEIGHTS             = [100, 0]
IMAGE_USE_AUTHORIZATION_WEIGHTS  = [55, 45]


# ---------------------------------------------------------------------------
# Individual generators
# ---------------------------------------------------------------------------

def generate_contract_signed() -> bool:
    return random.choices(BOOL_VALUES, weights=CONTRACT_SIGNED_WEIGHTS, k=1)[0]

def generate_id_copy() -> bool:
    return random.choices(BOOL_VALUES, weights=ID_COPY_WEIGHTS, k=1)[0]

def generate_resume_cv() -> bool:
    return random.choices(BOOL_VALUES, weights=RESUME_CV_WEIGHTS, k=1)[0]

def generate_gdpr_policies_signed() -> bool:
    return random.choices(BOOL_VALUES, weights=GDPR_POLICIES_SIGNED_WEIGHTS, k=1)[0]

def generate_code_of_ethics_signed() -> bool:
    return random.choices(BOOL_VALUES, weights=CODE_OF_ETHICS_SIGNED_WEIGHTS, k=1)[0]

def generate_osh_informed() -> bool:
    return random.choices(BOOL_VALUES, weights=OSH_INFORMED_WEIGHTS, k=1)[0]

def generate_image_use_authorization() -> bool:
    return random.choices(BOOL_VALUES, weights=IMAGE_USE_AUTHORIZATION_WEIGHTS, k=1)[0]


# ---------------------------------------------------------------------------
# Batch generators
# ---------------------------------------------------------------------------

def generate_contract_signed_batch(n: int) -> list:
    return random.choices(BOOL_VALUES, weights=CONTRACT_SIGNED_WEIGHTS, k=n)

def generate_id_copy_batch(n: int) -> list:
    return random.choices(BOOL_VALUES, weights=ID_COPY_WEIGHTS, k=n)

def generate_resume_cv_batch(n: int) -> list:
    return random.choices(BOOL_VALUES, weights=RESUME_CV_WEIGHTS, k=n)

def generate_gdpr_policies_signed_batch(n: int) -> list:
    return random.choices(BOOL_VALUES, weights=GDPR_POLICIES_SIGNED_WEIGHTS, k=n)

def generate_code_of_ethics_signed_batch(n: int) -> list:
    return random.choices(BOOL_VALUES, weights=CODE_OF_ETHICS_SIGNED_WEIGHTS, k=n)

def generate_osh_informed_batch(n: int) -> list:
    return random.choices(BOOL_VALUES, weights=OSH_INFORMED_WEIGHTS, k=n)

def generate_image_use_authorization_batch(n: int) -> list:
    return random.choices(BOOL_VALUES, weights=IMAGE_USE_AUTHORIZATION_WEIGHTS, k=n)


# ---------------------------------------------------------------------------
# Quick smoke-test: run this file directly to verify all distributions
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    SAMPLE_SIZE = n_samples

    fields = [
        ("contract_signed",         generate_contract_signed_batch,         CONTRACT_SIGNED_WEIGHTS),
        ("id_copy",                  generate_id_copy_batch,                  ID_COPY_WEIGHTS),
        ("resume_cv",                generate_resume_cv_batch,                RESUME_CV_WEIGHTS),
        ("gdpr_policies_signed",     generate_gdpr_policies_signed_batch,     GDPR_POLICIES_SIGNED_WEIGHTS),
        ("code_of_ethics_signed",    generate_code_of_ethics_signed_batch,    CODE_OF_ETHICS_SIGNED_WEIGHTS),
        ("osh_informed",             generate_osh_informed_batch,             OSH_INFORMED_WEIGHTS),
        ("image_use_authorization",  generate_image_use_authorization_batch,  IMAGE_USE_AUTHORIZATION_WEIGHTS),
    ]

    print(f"Sample size: {SAMPLE_SIZE:,}\n")
    print(f"{'Field':<28} {'Value':<6} {'Count':>8}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 68)

    for field_name, batch_fn, weights in fields:
        results = batch_fn(SAMPLE_SIZE)
        for value, weight in zip(BOOL_VALUES, weights):
            count = results.count(value)
            observed = count / SAMPLE_SIZE * 100
            print(f"{field_name:<28} {str(value):<6} {count:>8}  {observed:>9.2f}%  {weight:>9}%")
        print()