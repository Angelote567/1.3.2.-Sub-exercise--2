// Estamos en la línea 57


EmployeeProfile (perfil):

employee_id: int (único)
first_name: str
last_name: str
id_document: str (DNI/NIE/passport)
birth_date: date
address: str
city: str
province: str
postal_code: str (mejor str para no perder ceros)
phone: str
email: str
marital_status: str (o enum/string controlado)
dependents: int
job_title: str
department: str
work_center: str
job_group: str
hire_date: date
contract_type: str (ej. Permanent/Temporary/Intern)
workday: str (Full-time/Part-time)
schedule: str (ej. "9-18", "Turnos", etc.)
probation_period: str (o int meses; recomendado: int meses)
applicable_collective_agreement: str

Compensation (compensación)
base_salary_monthly: float
allowances: float (o dict si queréis desglose; ahora está como número)
extra_payments: int (0, 2, 3…)
extra_payments_prorated: bool
deductions: float (o dict si queréis desglose)
withholding_rate: float (porcentaje IRPF, ej. 15.0)
bank_account_iban: str
estimated_company_cost: float
compensation_notes: str

Documentation (documenación)
contract_signed: bool
contract_addenda: list[str] (o list[dict] si guardáis metadatos)
id_copy: bool
degrees_certificates: list[str]
resume_cv: bool
CV: JSON # En caso de existir resume_cv -> CV
gdpr_policies_signed: bool
code_of_ethics_signed: bool
osh_informed: bool
medical_clearance: bool
image_use_authorization: bool
last_documentation_update_date: datetime

History (historial)
history: JSON //Fecha "de entregado", tipo_evento, entregado/recibido, descripcion

Hemos cambiado el evento por un JSON en el history 

OSH / PRL
role_risk_factors: str (o list[str] si queréis varios)
osh_training_received: bool
osh_training_date: date/datetime (o None si no recibido)
ppe_issued: bool
ppe_details: str (o list[str])
medical_fitness: str (Fit/Restricted/Unfit)
medical_exam_date: date/datetime (o None)
osh_notes: str
SocialSecurity
ss_affiliation_number: str
ss_enrollment_date: date/datetime
contribution_group: str (o int si es numérico en vuestro modelo)
withholding_rate_ss: float (en tu comentario pone IRPF %, pero esto suele ser % SS; dejadlo float)
applicable_bonuses: list[str] (o list[dict] si hay importes/fechas)
Resources (recursos/activos)
laptop_assigned: bool
mobile_phone_assigned: bool
access_card_assigned: bool
other_assets: list[str] (o list[dict] con asset_tag, model, etc.)
asset_delivery_date: date/datetime (o None)
asset_return_date: date/datetime (o None)
system_accesses: list[str] (ej. ["O365","ERP"])
assigned_licenses: list[str]

Exit (salida)
termination_date: date/datetime (o None si activo)
termination_reason: str (o None)
exit_interview_done: bool
severance_delivered: bool
employer_certificate_delivered: bool
assets_recovered: bool
exit_comments: str

Nota rápida (para evitar líos)
Fechas: mejor datetime/date (consultas por rango y filtros funcionan muy bien).
postal_code y phone: str.
Campos “desglosables” (allowances, deductions) si queréis más realismo: podéis cambiarlos a dict tipo:
{"transport": 80, "meal": 120} (pero entonces hay que acordarlo en grupo).
Si quieres, te lo convierto en una definición tipo Pydantic / dataclasses para que el equipo programe con tipado claro y validación automática.