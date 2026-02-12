// Estamos en la línea 57


EmployeeProfile (perfil):
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


Compensation (compensación)
base_salary_monthly: float
allowances: float
extra_payments: int
extra_payments_prorated: bool
deductions: float
withholding_rate: float
bank_account_iban: str
estimated_company_cost: float
compensation_notes: str

Documentation (documenación)
contract_signed: bool
contract_addenda: list[str]  # o list[dict] si guardas metadatos
id_copy: bool
degrees_certificates: list[str]
resume_cv: bool
gdpr_policies_signed: bool
code_of_ethics_signed: bool
osh_informed: bool
medical_clearance: bool
image_use_authorization: bool
last_documentation_update_date: str | datetime

History (historial)
history: JSON //Fecha "de entregado", tipo_evento, entregado/recibido, descripcion

Hemos cambiado el evento por un JSON en el history 

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
applicable_bonuses: list[str]  # o list[dict] si guardas detalles

Resources
laptop_assigned: bool
mobile_phone_assigned: bool
access_card_assigned: bool
other_assets: list[str]  # o list[dict]
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

