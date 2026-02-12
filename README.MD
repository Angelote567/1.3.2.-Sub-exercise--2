// We are on line 57


EmployeeProfile (profile):

**employee_id**: str --> It is not a mathematical value, it is an identifier. Representing it as text avoids misinterpretations. In addition, the ID usually has a format (prefixes by country, company, center, etc.), and if we use int we lose that flexibility; it also avoids format issues such as leading zeros, among others.
**first_name**: str --> A name is text and may include accents, spaces, and compound names. Storing it as str prevents data loss and respects international formatting.
**last_name**: str --> Same reasoning as for the first name.
**id_document**: str (DNI/NIE/passport) --> It contains letters, different country formats, and sometimes separators. An int would break NIE/DNI values with letters and lose zeros/structure. As a legal identifier, it should be treated as text (even if validated with regex).
**birth_date**: date (datetime.date) --> Although conceptually it can be described as “date”, Python does not have a native type with that exact name, so the date class from the datetime module is used. This choice allows age range queries, temporal calculations, and efficient sorting in MongoDB. datetime.datetime is not used because the birth time adds no value in the HR context and would introduce unnecessary complexity to the data model.
**address**: str --> It is a free-form and inherently “messy” string (abbreviations, special characters, etc.). It could be modeled as a dict (street, number, etc.), but for synthetic HR data and 1.5M records it usually adds noise and increases size. str is simple and realistic.
**city**: str --> 
**province**: str
**postal_code**: str (better as str to avoid losing leading zeros)
**phone**: str
**email**: str
**marital_status**: str (or controlled enum/string)
**dependents**: int
**job_title**: str
**department**: str
**work_center**: str
**job_group**: str
**hire_date**: date
**contract_type**: str (e.g. Permanent/Temporary/Intern)
**workday**: str (Full-time/Part-time)
**schedule**: str (e.g. "9-18", "Shifts", etc.)
**probation_period**: str (or int months; recommended: int months)
**applicable_collective_agreement**: str


employee_id: str
first_name: str
last_name: str
id_document: str
birth_date: str | datetime

address: str
city: str
province: str
postal_code: str
phone: str
email: str
marital_status: str

dependents: int
job_title: str
department: str
work_center: str
job_group: str

hire_date: str | datetime
contract_type: str
workday: str
schedule: str
probation_period: str
applicable_collective_agreement: str


Compensation
base_salary_monthly: float
allowances: float
extra_payments: int
extra_payments_prorated: bool
deductions: float
withholding_rate: float
bank_account_iban: str
estimated_company_cost: float
compensation_notes: str

Documentation
contract_signed: bool
contract_addenda: list[str]  # or list[dict] if storing metadata
id_copy: bool
degrees_certificates: list[str]
resume_cv: bool
gdpr_policies_signed: bool
code_of_ethics_signed: bool
osh_informed: bool
medical_clearance: bool
image_use_authorization: bool
last_documentation_update_date: str | datetime

History
history: JSON //Delivery date, event_type, delivered/received, description

We changed the event structure to a JSON inside history

OSH (PRL)
role_risk_factors: str
osh_training_received: bool
osh_training_date: str | datetime
ppe_issued: bool
ppe_details: str
medical_fitness: str
medical_exam_date: str | datetime
osh_notes: str

SocialSecurity
ss_affiliation_number: str
ss_enrollment_date: str | datetime
contribution_group: str
withholding_rate_ss: float
applicable_bonuses: list[str]  # or list[dict] if storing details

Resources
laptop_assigned: bool
mobile_phone_assigned: bool
access_card_assigned: bool
other_assets: list[str]  # or list[dict]
asset_delivery_date: str | datetime
asset_return_date: str | datetime | None
system_accesses: list[str]
assigned_licenses: list[str]

Exit
termination_date: str | datetime | None
termination_reason: str | None
exit_interview_done: bool
severance_delivered: bool
employer_certificate_delivered: bool
assets_recovered: bool
exit_comments: str
