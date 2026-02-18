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

- **dependents**: int --> It represents a discrete countable quantity, making int the most semantically correct and efficient representation. Using float would be inappropriate because dependents can not be fractional, and storing the value as str would complicate filtering, aggregation, and statistical analysis.

- **job_title**: str --> A job title is a descriptive business label rather than a numeric value, so representing it as str preserves readability and makes the dataset easier to understand in reports and visualizations. While it could be modeled using numeric IDs linked to a normalized job catalog, this would introduce additional complexity without clear benefits for a synthetic HR dataset

- **department**: str --> A department is a categorical business label whose main purpose is grouping and reporting rather than numerical calculation. Storing it as a str keeps the dataset human-readable and allows direct aggregation in analytics (e.g., headcount by department) without requiring additional lookup tables.

- **work_center**: str --> Same as previous ones.

- **job_group**: str --> Using a string preserves the original business format and avoids unnecessary transformations when generating or displaying data. While an int could be slightly more efficient if job groups were strictly numeric and standardized across the organization, this assumption often does not hold in real HR systems. A controlled str value ensures readability, consistency, and compatibility with reporting tools, while still allowing filtering and aggregation without added complexity.

- **hire_date**: date (datetime.date) --> Using a proper date type (datetime.date) ensures accurate comparisons, chronological sorting, and efficient querying in MongoDB. Storing this field as a string (e.g., "2023-01-15") would introduce risks of inconsistent formatting and would require additional parsing before performing time-based operations. A date object keeps the data semantically correct while enabling scalable analytics across a large HR dataset.

- **contract_type**: str (e.g. Permanent/Temporary/Intern) --> contract_type is a categorical business attribute whose main purpose is classification and reporting rather than numerical computation. Representing it as a controlled str keeps the dataset readable and self-explanatory in analytics and dashboards (e.g., distribution of permanent vs temporary employees). Although it could be encoded as an integer enum, this would reduce clarity and require additional mapping logic. MongoDB does not enforce enum constraints natively, so using predefined string values at the application level achieves consistency while maintaining flexibility and interpretability.

- **workday**: str (Full-time/Part-time) --> Using a controlled str keeps the dataset intuitive and aligned with common HR terminology, making reports and visualizations easier to interpret. Since MongoDB does not enforce enums, predefined string values act as a logical enum while maintaining readability. Although representing workday as a numeric FTE ratio (float) could enable more precise analytical calculations, it reduces semantic clarity and may complicate interpretation for non-technical users.

- **schedule**: str (e.g. "9-18", "Shifts", etc.) --> Using a str provides a lightweight and human-readable way to represent schedules, which is especially beneficial when generating large-scale synthetic datasets such as a 1.5-million-record HR database. A simple string keeps storage overhead low and simplifies data generation while still allowing grouping and reporting.

- **probation_period**: int (number of months) --> Although probation periods are sometimes expressed as text (e.g., “2 months”), storing the value as an int provides a consistent and analytically useful representation. Using an integer allows direct comparisons, filtering, and statistical analysis (e.g., identifying employees still within probation or analyzing average probation durations). Representing this field as a str introduces formatting inconsistencies and requires additional parsing for numerical operations. By defining a fixed unit (months) at the model level, the dataset remains simple, scalable, and semantically clear while avoiding unnecessary complexity.

- **applicable_collective_agreement**: str --> A collective agreement is a legal or organizational classification rather than a numerical value, making str the most appropriate representation. Using readable text preserves clarity in reports and ensures that the dataset remains self-explanatory without requiring additional mapping tables.

<br>

## Compensation
- **base_salary_monthly**: float --> This field represents the employee’s gross monthly base salary, which is a quantitative monetary value. Using float allows the model to handle decimal values accurately and supports financial calculations, aggregations, and comparisons. Storing it as int could be restrictive if cents or prorated values appear, while str would prevent numerical analysis and require unnecessary parsing.

- **allowances**: float --> Allowances represent additional monetary compensation (e.g., transport or meal benefits). Representing this field as a float keeps the model simple and efficient for large-scale synthetic datasets. Although a dict could provide a detailed breakdown, it would increase complexity and storage size without clear analytical benefits for the current scope.

- **extra_payments**: int --> This attribute represents the number of additional salary payments per year (e.g., 12, 14). Since it is a discrete countable quantity, int is the most semantically correct and efficient representation. Using float or str would introduce ambiguity and reduce clarity.

- **extra_payments_prorated**: bool --> This field indicates whether extra payments are distributed across monthly salaries or paid separately. As it expresses a binary condition (true/false), bool is the most appropriate and clear data type.

- **deductions**: float --> Deductions represent monetary reductions applied to the salary. Using float allows consistent financial calculations and aggregation. While a structured dict could model detailed deduction categories, it would significantly increase complexity and data volume without being strictly necessary for the current dataset design.

- **withholding_rate**: float --> This value represents a percentage (e.g., tax withholding) that may include decimals. A float ensures precise numerical representation and enables analytical operations such as averages or comparisons. Using int could limit precision, and str would complicate computations.

- **bank_account_iban**: str --> IBAN is an alphanumeric identifier that includes letters and numbers and must preserve its exact format. Storing it as str avoids data corruption, formatting loss, or incorrect mathematical interpretation.

- **estimated_company_cost**: float --> This field represents the total estimated cost of the employee for the company, combining salary and employer contributions. As a monetary metric requiring calculations and aggregations, float is the most appropriate representation.

- **compensation_notes**: str --> This optional field stores additional free-text information related to compensation. Since it may contain descriptive comments or explanations, str is the most flexible and suitable data type.

<br>

## Documentation
- **contract_signed**: bool --> Indicates whether the main employment contract has been signed. Since this represents a binary state (signed or not signed), bool is the most semantically correct and efficient data type, avoiding ambiguity and simplifying filtering or validation logic.

- **contract_addenda**: list[str] --> Represents a list of contract addenda identifiers or filenames associated with the employee. A list[str] keeps the structure lightweight and easy to manage for large datasets. Although list[dict] could store richer metadata (e.g., date, type, or version), it would increase storage size and complexity without clear necessity for a synthetic HR model.

- **id_copy**: bool --> Indicates whether a copy of the employee’s identification document has been provided. As a simple yes/no condition, bool is the most appropriate representation and allows straightforward validation checks.

- **degrees_certificates**: list[str] --> Stores references to academic degrees or professional certifications provided by the employee. Using a list[str] allows multiple documents to be associated with a single employee while keeping the model simple and scalable.

- **resume_cv**: bool --> Indicates whether the employee has submitted a CV or résumé. This is a binary status field, making bool the most accurate and efficient choice.

- **gdpr_policies_signed**: bool --> Indicates whether the employee has signed GDPR-related policies or consent forms. A boolean value clearly represents compliance status without requiring additional interpretation.

- **code_of_ethics_signed**: bool --> Indicates whether the employee has accepted and signed the organization’s code of ethics. Since this is a compliance flag, bool ensures clarity and easy auditing.

- **osh_informed**: bool --> Indicates whether the employee has been informed about Occupational Safety and Health (OSH) requirements. Using bool reflects the binary nature of the information while enabling simple reporting on compliance coverage.

- **medical_clearance**: bool --> Indicates whether valid medical clearance documentation exists for the employee. A boolean value is appropriate because the field reflects a presence/absence condition rather than descriptive data.

- **image_use_authorization**: bool --> Indicates whether the employee has granted authorization for image or media usage. As with other consent-related attributes, bool provides a clear and consistent representation.

- **last_documentation_update_date**: datetime (or str | datetime during ingestion) --> Represents the most recent date when employee documentation was updated or reviewed. Using a proper datetime object enables chronological sorting, auditing, and temporal analysis. While str may be accepted during ingestion or data import, standardizing to datetime is recommended to maintain consistency and enable efficient querying in MongoDB.

<br>

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

<br>

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

<br>

## Exit
- **termination_date**:datetime | None --> The termination may not have occurred yet, so it requires a date-time value but must allow null when the employee is still active.

- **termination_reason**: str | None -->Is descriptive text and may be unknown or not provided at the moment of record creation.

- **exit_interview_done**: bool --> This is a yes/no process indicating whether the exit interview has been completed.

- **severance_delivered**: bool -->Severance is either delivered or not, making a boolean the most appropriate status flag.

- **employer_certificate_delivered**: bool -->  Is either delivered or not.

- **assets_recovered**: bool --> Is either  fully recovered or not.

- **exit_comments**: str --> Free-form text is required to store notes, feedback, or additional context about the exit process.