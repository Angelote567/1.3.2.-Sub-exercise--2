// We are on line 57


## EmployeeProfile (profile):
- **employee_id**: str --> It is not a mathematical value, it is an identifier. Representing it as text avoids misinterpretations. In addition, the ID usually has a format (prefixes by country, company, center, etc.), and if we use int we lose that flexibility; it also avoids format issues such as leading zeros, among others.

- **first_name**: str --> A name is text and may include accents, spaces, and compound names. Storing it as str prevents data loss and respects international formatting.

- **last_name**: str --> Same reasoning as for the first name.

- **id_document**: str (DNI/NIE/passport) --> It contains letters, different country formats, and sometimes separators. An int would break NIE/DNI values with letters and lose zeros/structure. As a legal identifier, it should be treated as text (even if validated with regex).

- **birth_date**: date (datetime.date) --> Although conceptually it can be described as “date”, Python does not have a native type with that exact name, so the date class from the datetime module is used. This choice allows age range queries, temporal calculations, and efficient sorting in MongoDB. datetime.datetime is not used because the birth time adds no value in the HR context and would introduce unnecessary complexity to the data model.

- **address**: str --> It is a free-form and inherently “messy” string (abbreviations, special characters, etc.). It could be modeled as a dict (street, number, etc.), but for synthetic HR data and 1.5M records it usually adds noise and increases size. str is simple and realistic.

- **city**: str --> A city name is a descriptive label rather than a numerical value, so representing it as text preserves readability and avoids unnecessary complexity. Using an int would only make sense if the system relied on an external normalized city catalog with numeric IDs, which adds architectural overhead without clear benefits for a synthetic HR dataset. Storing the value as str allows easy grouping, filtering, and aggregation in reporting while keeping the dataset human-readable and flexible.

- **province**: str --> Same justification than city.

- **postal_code**: str --> Postal codes are identifiers, not mathematical values. They may include leading zeros or country-specific formats, which would be lost if stored as int. Using str ensures formatting consistency and avoids data integrity issues during imports or transformations.

- **phone**: str --> Phone numbers are not numerical quantities; they may contain symbols such as “+”, spaces, or extensions. Storing them as int would remove formatting and could introduce errors. Representing them as str preserves flexibility and aligns with common data-modeling practices.

- **email**: str --> An email address is a structured textual identifier containing special characters (“@”, “.”). Using str ensures compatibility with validation rules and avoids unnecessary transformations. There is no practical advantage to using any other data type.

- **marital_status**: str --> MaritalStatus is conceptually an enumerated field because it only accepts a limited set of values (e.g., “Single”, “Married”, “Divorced”, “Widowed”). However, instead of implementing a strict enum or numeric code, it is stored as a controlled str. MongoDB does not enforce enum types natively, and using numeric identifiers would reduce readability and require additional mapping logic. By using controlled string values generated from a predefined list, the dataset remains human-readable, consistent, and easier to analyze in reports and visualizations while preserving the semantic behavior of an enum at the application level.

- **dependents**: int

- **job_title**: str

- **department**: str

- **work_center**: str

- **job_group**: str

- **hire_date**: date

- **contract_type**: str (e.g. Permanent/Temporary/Intern)

- **workday**: str (Full-time/Part-time)

- **schedule**: str (e.g. "9-18", "Shifts", etc.)

- **probation_period**: str (or int months; recommended: int months)

- **applicable_collective_agreement**: str

<br>

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


## Compensation
base_salary_monthly: float
allowances: float
extra_payments: int
extra_payments_prorated: bool
deductions: float
withholding_rate: float
bank_account_iban: str
estimated_company_cost: float
compensation_notes: str

## Documentation
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

## History
history: JSON //Delivery date, event_type, delivered/received, description

We changed the event structure to a JSON inside history

## OSH (PRL)
role_risk_factors: str
osh_training_received: bool
osh_training_date: str | datetime
ppe_issued: bool
ppe_details: str
medical_fitness: str
medical_exam_date: str | datetime
osh_notes: str

## SocialSecurity
- **ss_affiliation_number**: str --> It is not a mathematical value, it is a legal identifier assigned by the Social Security system. Although it contains numbers, it may include leading zeros or follow a specific structured format. Representing it as text preserves its integrity, avoids formatting issues, and prevents accidental mathematical operations.

- **ss_enrollment_date**: datetetime --> It represents the date when the employee was registered in the Social Security system. Python does not have a standalone date type outside the datetime module, so the date class from datetime is used. This allows temporal comparisons, seniority calculations, and efficient date-based queries without adding unnecessary time precision.

- **contribution_group**: str --> It represents an administrative classification that determines contribution bases and regulatory conditions. Although it may appear numeric in regulations, it is conceptually a category rather than a value used for calculations. Storing it as text avoids semantic confusion and preserves flexibility.

- **withholding_rate_ss**: float --> It represents a percentage applied to salary calculations and may include decimal values. Since it is used in financial computations, a numeric type is required. float is appropriate because contribution rates are expressed with decimal precision.

- **applicable_bonuses**: list[str] --> An employee may qualify for multiple Social Security bonuses simultaneously. A list structure allows storing multiple values dynamically. Each bonus is represented as text because it is identified by name or legal reference.


## Resources
- **laptop_assigned**: bool --> This field can only be true or false. It shows if the employee has a
company laptop. Since the employee either has it or not, a boolean value is enough. It avoids confusion
and keeps the data clear and easy to read.

- **mobile_phone_assigned**: bool --> This also uses true or false. It indicates if the employee has
acompany mobile phone. Because it is just a yes/no situation, a boolean type is the simplest and most
correct option.

- **access_card_assigned**: bool --> This field shows if the employee has received an access card for the
building. It is a simple yes/no condition, so bool is the best type to use.

- **other_assets**: list[str] --> This is a list because the employee may have more extra items, such as a
monitor, headset, or tablet. Each item is stored as text. A list allows storing multiple values in one
field.

- **asset_delivery_date**: date (datetime.date) --> This field stores the date when the equipment was
given to the employee. Using a date type allows sorting by time and checking how long the assets have
been assigned.

- **asset_return_date**: date | None --> This field stores the date when the assets were returned. It can
also be empty (None) if the employee is still using them. This makes it clear whether the return has
happened or not.

- **system_accesses**: list[str] --> This is a list of systems the employee can use, such as ERP, CRM, o
email platforms. Since an employee can have access to several systems, a list is the correct structure.

- **assigned_licenses**: list[str] --> This field stores the software licenses assigned to the employee,
like Microsoft 365 or Adobe. It is a list because the employee may have more than one license at the
same time.

## Exit
- **termination_date**:datetime | None --> The termination may not have occurred yet, so it requires a date-time value but must allow null when the employee is still active.

- **termination_reason**: str | None -->Is descriptive text and may be unknown or not provided at the moment of record creation.

- **exit_interview_done**: bool --> This is a yes/no process indicating whether the exit interview has been completed.

- **severance_delivered**: bool -->Severance is either delivered or not, making a boolean the most appropriate status flag.

- **employer_certificate_delivered**: bool -->  Is either delivered or not.

- **assets_recovered**: bool --> Is either  fully recovered or not.

- **exit_comments**: str --> Free-form text is required to store notes, feedback, or additional context about the exit process.