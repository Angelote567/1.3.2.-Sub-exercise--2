"""
Appendix 12.1 – Assigned Licenses
Probabilistic generation for all software licenses in the assigned_licenses field.
Each license is an independent boolean: the employee either has it or not.
Source: Survey basis (professor's original code).
No dictionaries used – values and weights are kept in separate lists.

Result is stored as list[str] containing only the licenses the employee has assigned.

Licenses and assignment rates:
    Microsoft 365           : 80%
    Google Workspace        : 45%
    Slack                   : 50%
    Zoom                    : 55%
    Jira                    : 45%
    Confluence              : 35%
    Notion                  : 30%
    GitHub                  : 65%
    GitLab                  : 25%
    Bitbucket               : 15%
    Adobe Creative Cloud    : 30%
    Figma                   : 35%
    Visual Studio Pro       : 25%
    JetBrains               : 30%
    Docker Desktop          : 40%
    AWS Console             : 45%
    Azure Portal            : 40%
    Salesforce              : 30%
    HubSpot                 : 20%
    SAP                     : 15%
    Tableau                 : 18%
    Power BI                : 30%
    Miro                    : 25%
    Monday.com              : 15%
    Asana                   : 18%
    Trello                  : 22%
"""

import random
from dotenv import load_dotenv
import os
load_dotenv()
n_samples = int(os.getenv("N_SAMPLES"))



LICENSE_VALUES = [
    "Microsoft 365",
    "Google Workspace",
    "Slack",
    "Zoom",
    "Jira",
    "Confluence",
    "Notion",
    "GitHub",
    "GitLab",
    "Bitbucket",
    "Adobe Creative Cloud",
    "Figma",
    "Visual Studio Professional",
    "JetBrains",
    "Docker Desktop",
    "AWS Console",
    "Azure Portal",
    "Salesforce",
    "HubSpot",
    "SAP",
    "Tableau",
    "Power BI",
    "Miro",
    "Monday.com",
    "Asana",
    "Trello",
]

# Probability (%) of having each license assigned – independent per license
LICENSE_RATES = [
    80, 45, 50, 55, 45, 35, 30, 65, 25, 15,
    30, 35, 25, 30, 40, 45, 40, 30, 20, 15,
    18, 30, 25, 15, 18, 22,
]

BOOL_VALUES = [True, False]


# ---------------------------------------------------------------------------
# Individual generators
# ---------------------------------------------------------------------------

def generate_assigned_licenses() -> list:
    """Return a list of license names assigned to the employee."""
    licenses = []
    for license_name, rate in zip(LICENSE_VALUES, LICENSE_RATES):
        has_license = random.choices(BOOL_VALUES, weights=[rate, 100 - rate], k=1)[0]
        if has_license:
            licenses.append(license_name)
    return licenses


# ---------------------------------------------------------------------------
# Batch generator
# ---------------------------------------------------------------------------

def generate_assigned_licenses_batch(n: int) -> list:
    """Return a list of n assigned_licenses lists."""
    return [generate_assigned_licenses() for _ in range(n)]


# ---------------------------------------------------------------------------
# Quick smoke-test: run this file directly to verify all distributions
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    SAMPLE_SIZE = n_samples

    results = generate_assigned_licenses_batch(SAMPLE_SIZE)

    print(f"Sample size: {SAMPLE_SIZE:,}\n")
    print(f"{'License':<30} {'With license':>13}  {'Observed %':>10}  {'Expected %':>10}")
    print("-" * 68)

    for license_name, rate in zip(LICENSE_VALUES, LICENSE_RATES):
        count = sum(1 for r in results if license_name in r)
        print(f"{license_name:<30} {count:>13}  {count/SAMPLE_SIZE*100:>9.2f}%  {rate:>9}%")

    print()
    avg_licenses = sum(len(r) for r in results) / SAMPLE_SIZE
    print(f"Average number of licenses per employee: {avg_licenses:.2f}")