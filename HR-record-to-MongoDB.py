
from pymongo import MongoClient

def create_hr_record(
    # ----- EMPLOYEE PROFILE -----
    employee_id, first_name, last_name, id_document, birth_date,
    address, city, province, postal_code, phone, email, marital_status,
    dependents, job_title, department, work_center, job_group,
    hire_date, contract_type, workday, schedule, probation_period,
    applicable_collective_agreement,

    # ----- COMPENSATION -----
    base_salary_monthly, allowances, extra_payments, extra_payments_prorated,
    deductions, withholding_rate, bank_account_iban, estimated_company_cost,
    compensation_notes,

    # ----- DOCUMENTATION -----
    contract_signed, contract_addenda, id_copy, degrees_certificates, resume_cv,
    gdpr_policies_signed, code_of_ethics_signed, osh_informed, medical_clearance,
    image_use_authorization, last_documentation_update_date,

    # ----- HISTORY -----
    history,  # List of events, each like: {'date':..., 'event_type':..., 'description':..., ...}

    # ----- OCCUPATIONAL SAFETY & HEALTH (OSH / PRL) -----
    role_risk_factors, osh_training_received, osh_training_date, ppe_issued,
    ppe_details, medical_fitness, medical_exam_date, osh_notes,

    # ----- SOCIAL SECURITY -----
    ss_affiliation_number, ss_enrollment_date, contribution_group,
    withholding_rate_ss, applicable_bonuses,

    # ----- RESOURCES -----
    laptop_assigned, mobile_phone_assigned, access_card_assigned, other_assets,
    asset_delivery_date, asset_return_date, system_accesses, assigned_licenses,

    # ----- EXIT -----
    termination_date, termination_reason, exit_interview_done,
    severance_delivered, employer_certificate_delivered,
    assets_recovered, exit_comments
):
    """
    Builds a MongoDB-ready document with all fields from the Excel model.

    Notes:
    - Dates can be strings (e.g., '2025-03-15') or datetime objects; MongoDB
      will store them as-is. Prefer datetime objects for querying.
    - Booleans (e.g., contract_signed) should be True/False.
    - Numeric fields (e.g., base_salary_monthly, withholding_rate) should be numeric.
    """

    record = {
        "EmployeeProfile": {
            "EmployeeID": employee_id,
            "FirstName": first_name,
            "LastName": last_name,
            "IDDocument": id_document,  # DNI/NIE/Passport
            "BirthDate": birth_date,
            "Address": address,
            "City": city,
            "Province": province,
            "PostalCode": postal_code,
            "Phone": phone,
            "Email": email,
            "MaritalStatus": marital_status,
            "Dependents": dependents,
            "JobTitle": job_title,
            "Department": department,
            "WorkCenter": work_center,
            "JobGroup": job_group,
            "HireDate": hire_date,
            "ContractType": contract_type,
            "Workday": workday,
            "Schedule": schedule,
            "ProbationPeriod": probation_period,
            "ApplicableCollectiveAgreement": applicable_collective_agreement,
        },

        "Compensation": {
            "BaseSalaryMonthly": base_salary_monthly,
            "Allowances": allowances,
            "ExtraPayments": extra_payments,
            "ExtraPaymentsProrated": extra_payments_prorated,
            "Deductions": deductions,
            "WithholdingRate": withholding_rate,  # IRPF %
            "BankAccountIBAN": bank_account_iban,
            "EstimatedCompanyCost": estimated_company_cost,
            "Notes": compensation_notes,
        },

        "Documentation": {
            "ContractSigned": contract_signed,
            "ContractAddenda": contract_addenda,
            "IDCopy": id_copy,
            "DegreesCertificates": degrees_certificates,
            "ResumeCV": resume_cv,
            "GDPRPoliciesSigned": gdpr_policies_signed,
            "CodeOfEthicsSigned": code_of_ethics_signed,
            "OSHInformed": osh_informed,  # PRL informed
            "MedicalClearance": medical_clearance,
            "ImageUseAuthorization": image_use_authorization,
            "LastDocumentationUpdateDate": last_documentation_update_date,
        },

        # History is kept as a list of dictionaries
        "History": history,

        "OSH": {
            "RoleRiskFactors": role_risk_factors,
            "OSHTrainingReceived": osh_training_received,
            "OSHTrainingDate": osh_training_date,
            "PPEIssued": ppe_issued,
            "PPEDetails": ppe_details,
            "MedicalFitness": medical_fitness,
            "MedicalExamDate": medical_exam_date,
            "Notes": osh_notes,
        },

        "SocialSecurity": {
            "AffiliationNumber": ss_affiliation_number,  # NAF
            "EnrollmentDate": ss_enrollment_date,
            "ContributionGroup": contribution_group,
            "WithholdingRate": withholding_rate_ss,  # IRPF %
            "ApplicableBonuses": applicable_bonuses,
        },

        "Resources": {
            "LaptopAssigned": laptop_assigned,
            "MobilePhoneAssigned": mobile_phone_assigned,
            "AccessCardAssigned": access_card_assigned,
            "OtherAssets": other_assets,
            "AssetDeliveryDate": asset_delivery_date,
            "AssetReturnDate": asset_return_date,
            "SystemAccesses": system_accesses,
            "AssignedLicenses": assigned_licenses,
        },

        "Exit": {
            "TerminationDate": termination_date,
            "TerminationReason": termination_reason,
            "ExitInterviewDone": exit_interview_done,
            "SeveranceDelivered": severance_delivered,
            "EmployerCertificateDelivered": employer_certificate_delivered,
            "AssetsRecovered": assets_recovered,
            "Comments": exit_comments,
        },
    }
    return record

def insert_into_mongodb(record, url="mongodb://localhost:27017/",
                        db_name="HR", collection_name="employees"):
    """
    Connects to a MongoDB instance and inserts the given record.

    Parameters:
    - record: dict, document built by create_hr_record().
    - url: MongoDB connection string. Example for Atlas:
      'mongodb+srv://<user>:<password>@<cluster>/<db>?retryWrites=true&w=majority'
    - db_name: database name.
    - collection_name: target collection.

    Returns:
    - inserted_id (ObjectId)
    """
    client = MongoClient(url)
    db = client[db_name]
    collection = db[collection_name]

    result = collection.insert_one(record)
    print(f"Record inserted with _id: {result.inserted_id}")
    return result.inserted_id


# ------------------- USAGE EXAMPLE (commented) -------------------
# Example of building a minimal record (replace ... with real values):
#
# record = create_hr_record(
#     employee_id="E001", first_name="Ana", last_name="López",
#     id_document="12345678Z", birth_date="1990-05-01",
#     address="C/ Mayor 1", city="Zaragoza", province="Zaragoza", postal_code="50001",
#     phone="+34 600 000 000", email="ana@example.com", marital_status="Single",
#     dependents=0, job_title="HR Specialist", department="HR", work_center="HQ",
#     job_group="Group II", hire_date="2023-01-15", contract_type="Permanent",
#     workday="Full-time", schedule="9-18", probation_period="2 months",
#     applicable_collective_agreement="Sector Servicios",
#
#     base_salary_monthly=1800.0, allowances=200.0, extra_payments=2,
#     extra_payments_prorated=True, deductions=0.0, withholding_rate=15.0,
#     bank_account_iban="ES9121000418450200051332", estimated_company_cost=2500.0,
#     compensation_notes="",
#
#     contract_signed=True, contract_addenda=[], id_copy=True,
#     degrees_certificates=["BA HR"], resume_cv=True, gdpr_policies_signed=True,
#     code_of_ethics_signed=True, osh_informed=True, medical_clearance=True,
#     image_use_authorization=False, last_documentation_update_date="2025-12-01",
#
#     history=[{"date": "2024-06-01", "event_type": "Promotion", "description": "Promoted to Specialist"}],
#
#     role_risk_factors="Office work", osh_training_received=True,
#     osh_training_date="2024-02-10", ppe_issued=False, ppe_details="",
#     medical_fitness="Fit", medical_exam_date="2024-02-10", osh_notes="",
#
#     ss_affiliation_number="12/1234567890", ss_enrollment_date="2023-01-15",
#     contribution_group="Group 5", withholding_rate_ss=15.0, applicable_bonuses=[],
#
#     laptop_assigned=True, mobile_phone_assigned=False, access_card_assigned=True,
#     other_assets=[], asset_delivery_date="2023-01-15", asset_return_date=None,
#     system_accesses=["O365", "ERP"], assigned_licenses=["MS365 E3"],
#
#     termination_date=None, termination_reason=None, exit_interview_done=False,
#     severance_delivered=False, employer_certificate_delivered=False,
#     assets_recovered=False, exit_comments=""
# )
#
# insert_into_mongodb(record)

