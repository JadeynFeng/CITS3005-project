# Knowledge Graph Overview
## Schema
### Namespaces
- `UNIT` namespace for representing units (http://uwabookofknowledge.org/unit/)
- `MAJOR` namespace for representing majors (http://uwabookofknowledge.org/major/)
- `TERMS` namespace for various terms and properties (http://uwabookofknowledge.org/terms/)
- `PREREQ` namespace for representing prerequisites CNF (http://uwabookofknowledge.org/prereq/)
- `CONTACT` namespace for representing contact activities (http://uwabookofknowledge.org/contact/)

### Units Schema
| RDF Property                | Description                                    | Example Value                                    |
|-----------------------------|------------------------------------------------|--------------------------------------------------|
| `UNIT:<unit_code>`          | URI representing the unit                      | UNIT:AGRI5403                                    |
| `RDF.type`                  | Type of the resource (always `TERMS.Unit`)     | TERMS.Unit                                       |
| `TERMS.unitCode`            | Unit code                                      | "AGRI5403"                                       |
| `TERMS.unitTitle`           | Unit title                                     | "Advanced Commodity Marketing"                   |
| `TERMS.unitSchool`          | School offering the unit                       | "Agriculture and Environment"                    |
| `TERMS.unitBoard`           | Board of examiners for the unit                | "05 - Agriculture, Environmental and Related S"  |
| `TERMS.unitDelivery`        | Delivery mode of the unit                      | "Face to face"                                   |
| `TERMS.level`               | Level of the unit                              | 3                                                |
| `TERMS.credit`              | Credit points for completing the unit          | 6                                                |
| `TERMS.unitDescription`     | Description of the unit                        | "This is a course on agricultural commodity..."  |
| `TERMS.assessment`          | Assessment methods for the unit                | "Quizzes, Assignments"                           |
| `TERMS.isPartOfMajor`       | Majors associated with the unit (optional)     | "Agribusiness"                                   |
| `TERMS.unitOutcome`         | Learning outcomes of the unit (optional)       | "Demonstrate an understanding..."                |
| `TERMS.unitText`            | Prerequisites in text format (optional)        | "Successful completion of..."                    |
| `TERMS.prerequisitesCNF`    | Prerequisites in CNF `TERMS.AndReq` (optional) | "ACCT5432 AND ECON5541"                          |
| `TERMS.advisablePriorStudy` | Advisable prior study `TERMS.Unit` (optional)  | "AGRI5402"                                       |
| `TERMS.contact`             | Contact activity `TERMS.Contact` (optional)    | "Lectures: 6 hours..."                           |
| `TERMS.totalHours`          | The total contact hours per week for the unit  | 10                                               |
| `TERMS.note`                | Additional notes about the unit (optional)     | "..."                                            |

### Majors Schema

| RDF Property             | Description                                          | Example Value                                    |
|--------------------------|------------------------------------------------------|--------------------------------------------------|
| `MAJOR:<major_code>`     | URI representing the major                           | MAJOR:MJD-AGBUS                                  |
| `RDF.type`               | Type of the resource (always `TERMS.Major`)          | TERMS.Major                                      |
| `TERMS.majorCode`        | Major code                                           | "MJD-AGBUS"                                      |
| `TERMS.majorTitle`       | Major title                                          | "Agribusiness"                                   |
| `TERMS.majorSchool`      | School offering the major                            | "Agriculture and Environment"                    |
| `TERMS.majorBoard`       | Board of examiners for the major                     | "05 - Agriculture, Environmental and Related S"  |
| `TERMS.majorDelivery`    | Delivery mode of the major                           | "Face to face"                                   |
| `TERMS.majorDescription` | Description of the major                             | "Agribusiness refers to..."                      |
| `TERMS.majorOutcome`     | Learning outcomes of the major                       | "Demonstrate capacity to..."                     |
| `TERMS.majorText`        | Prerequisites text for the major (optional)          | "Mathematics Methods ATAR or..."                 |
| `TERMS.course`           | Course codes which requires the major                | "BP004, BH005"                                   |
| `TERMS.bridging`         | Bridging units for the major `TERMS.Unit` (optional) | "MATH1720, SCIE1500"                             |
| `TERMS.containsUnit`     | Core units for the major `TERMS.Unit`                | "ACCT1100, AGRI1001, ..."                        |

### Contact Schema

| RDF Property             | Description                                   | Example Value              |
|--------------------------|-----------------------------------------------|----------------------------|
| `CONTACT:<contact_code>` | URI representing the contact activity         | CONTACT:AGRI5403contact0   |
| `RDF.type`               | Type of the resource (always `TERMS.Contact`) | TERMS.Contact              |
| `TERMS.activity`         | Contact activity type                         | "Lecture"                  |
| `TERMS.hours`            | Contact hours for the activity                | 6                          |

### Prerequisite Schema

| RDF Property             | Description                                   | Example Value              |
|--------------------------|-----------------------------------------------|----------------------------|
| `PREREQ:<prereq_code>`   | URI representing the prerequisite CNF         | PREREQ:AGRI5403andReqs0    |
| `RDF.type`               | Type of the resource (always `TERMS.AndReq`)  | TERMS.AndReq               |
| `TERMS.orReq`            | Prerequisite unit `TERMS.Unit`                | "ACCT5432"                 |

## Queries List

Note: All SPARQL queries can be found on `line 122-402` in `handbook.py`.

1. Find all units with more than 6 outcomes
2. Find all level 3 units that do not have an exam, and where none of their prerequisites have an exam
3. Find all units that appear in more than 3 majors
4. Basic search functionality in unit's description or outcomes by inputting a search string
5. Find all units with a specific major
6. Find all prerequisites for a given unit
7. Find all units with a specific level
8. Find units with 12 credit points
9. Find all majors that require a specific unit
10. Find units with a specific delivery mode
11. Find units with school in Molecular Sciences and is 6 credit points
12. Find all Molecular Sciences units that do not have BIOC2002 as a prerequisite

## Constraints

Note: All constraints shape graph can be found on `constraints.shacl`.

### 1. Prerequisite Level Constraint
- Every prerequisite for a level X unit should have a level less than X
- For example, if a unit is at Level 3, its prerequisites should be at Level 1 or Level 2

### 2. No Self-Prerequisite Constraint
- No unit should be its own prerequisite
- For example, AGRI5403 should not be a prerequisite for AGRI5403

### 3. Contact Hours Constraint
- No major should require more than 40 contact hours per week
- This is based on the assumption that all units of a certain level in a major would be completed in the same year. Thus, this constraint was calculated by grouping units of the same level and ensuring that the sum of their contact hours are within the threshold of 80 hours per week for 2 semesters.

### 4. Unit Properties Constraint
- This constraint specifies the required properties for a unit
- A unit can only have ONE of each:
    - unit code - (must be a string of 4 letters followed by 4 numbers)
    - title - (must be a string)
    - school - (must be a string)
    - board of examiners - (must be a string)
    - delivery mode - (must have a value of either 'Face to face', 'Online', 'Both', or '')
    - level - (must be an integer)
    - description - (must be a string)
    - credit - (must be an integer)
    - total contact hours - (must be an integer)
    - prerequisites text - (must be a string)
- A unit can have MULTIPLE of:
    - assessment methods - (must be a string)
    - majors - (must be a string)
    - learning outcomes - (must be a string)
    - contact activities - (must be an entity of type `TERMS.Contact`)
    - prerequisites CNF - (must be an entity of type `TERMS.AndReq`)
    - advisable prior study - (must be an entity of type `TERMS.Unit`)
    - notes - (must be a string)

### 5. Major Properties Constraint
- This constraint specifies the required properties for a major
- A major can only have ONE of each:
    - major code - (must be a string of 3 letters, followed by a hyphen, followed by 5 letters)
    - title - (must be a string)
    - school - (must be a string)
    - board of examiners - (must be a string)
    - delivery mode - (must have a value of either 'Face to face', 'Online', 'Both', or '')
    - description - (must be a string)
    - prerequisites text - (must be a string)
- A major can have MULTIPLE of:
    - learning outcomes - (must be a string)
    - courses - (must be a string)
    - bridging units - (must be an entity of type `TERMS.Unit`)
    - core units - (must be an entity of type `TERMS.Unit`)

### 6. Contact Properties Constraint
- This constraint specifies the required properties for a contact activity
- A contact activity can only have ONE of each: 
    - activity type - (must be a string)
    - its contact hours - (must be an integer)

### 7. Prerequisite Properties Constraint
- This constraint specifies the required properties for a prerequisite CNF
- A prerequisite CNF can only have MULTIPLE of:
    - prerequisite units - (must be an entity of type `TERMS.Unit`)

## Ontology

### Classes
1. `Unit`: Represents a unit.
2. `Major`: Represents a major.
3. `Contact`: Represents a contact activity for a unit.
4. `Prerequisite`: Represents a prerequisite CNF for a unit.

### Object Properties
1. `prerequisitesCNF`: Relates a unit to its prerequisite CNF.
2. `orReq`: Relates a prerequisite CNF to its prerequisite unit.
3. `contact`: Relates a unit to its contact activity.
4. `advisablePriorStudy`: Relates a unit to its advisable prior study.
5. `containsUnit`: Relates a major to its core units.
6. `bridging`: Relates a major to its bridging units.

### Data Properties for `Contact`
- These properties define attributes related to contact activity information.
- Examples include `activity` and `hours`.

### Data Properties for `Unit`
- These properties define attributes related to unit information.
- Examples include `unitCode`, `unitTitle`, `unitSchool`, `unitBoard`, `unitDelivery`, `level`, `unitDescription`, `credit`, `assessment`, `isPartOfMajor`, `unitOutcome`, `unitText`, and `note`.

### Data Properties for `Major`
- These properties define attributes related to major information.
- Examples include `majorCode`, `majorTitle`, `majorSchool`, `majorBoard`, `majorDelivery`, `majorDescription`, `majorOutcome`, `majorText`, and `course`.

### SWRL Rules
1. A prerequisite of a prerequisite is a prerequisite.
2. An outcome of a core unit is an outcome of a major.
3. A required text of a core unit is a required text for a major (based on the assumption that this is relating to the unitText and majorText property). 

# Instructions
## Executing SPARQL Queries

1. Run `python3 handbook.py` to start the script to load the data into RDFLib and execute some SPARQL queries
2. The script will present you with a list of queries to choose from.
3. Enter the corresponding number to execute a query.
4. The script will execute the selected query and display the results.
5. Press `Enter` to continue to selecting the next query.
6. To exit the script, enter 0 when prompted.

Note: The script maintains a log of queries and their results in a text file called 'query_results.txt'.

## Executing SHACL Constraints Validation

1. Run `python3 constraints.py` to start the script to load the shapes graph for running validation.
2. It displays the validation results, including any violation information.

## Executing OWL Ontology Rules

1. Run `python3 ontology.py` to start the script to create an OWL ontology, apply SWRL rules to the handbook knowledge graph and saves it to 'ontology.owl'.
2. You can input additional SWRL rules, given that they are valid.
3. Press `Enter` to continue running the script to apply SWRL rules and save the ontology.
4. It displays information which demonstrates that the rules have been applied.

## How to Add, Update, or Remove Data

1. Run `python3 crud.py` to start the script to load the ontology.
2. The script will present you with a list of actions to choose from to update the ontology.
3. You can add, update or remove unit entities or major entities.
4. To exit the script, enter 0 when prompted.
5. The script will save the updated ontology to 'updated.owl'.
