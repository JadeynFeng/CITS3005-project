# Knowledge Graph Overview
## Schema
### Namespaces
- `UNIT` namespace for representing educational units (http://uwabookofknowledge.org/unit/)
- `MAJOR` namespace for representing majors (http://uwabookofknowledge.org/major/)
- `TERMS` namespace for various terms and properties (http://uwabookofknowledge.org/terms/)

### Units Schema
| RDF Property                   | Description                                         | Example Value                                    |
|--------------------------------|-----------------------------------------------------|--------------------------------------------------|
| `UNIT:<unit_code>`             | URI representing the unit                           | UNIT:AGRI5403                                    |
| `RDF.type`                     | Type of the resource (always `TERMS.Unit`)          | TERMS.Unit                                       |
| `TERMS.code`                   | Unit code                                           | "AGRI5403"                                       |
| `TERMS.title`                  | Unit title                                          | "Advanced Commodity Marketing"                   |
| `TERMS.school`                 | School offering the unit                            | "Agriculture and Environment"                    |
| `TERMS.board_of_examiners`     | Board of examiners for the unit                     | "05 - Agriculture, Environmental and Related S"  |
| `TERMS.delivery_mode`          | Delivery mode of the unit                           | "Face to face"                                   |
| `TERMS.level`                  | Level of the unit                                   | "3"                                              |
| `TERMS.description`            | Description of the unit                             | "This is a course on..."                         |
| `TERMS.credit`                 | Credit hours for the unit                           | "6"                                              |
| `TERMS.assessment`             | Assessment methods for the unit                     | "Quizzes, Assignments"                           |
| `TERMS.offering`               | Offering information for the unit (optional)        | "..."                                            |
| `TERMS.majors`                 | Majors associated with the unit (optional)          | "Agribusiness"                                   |
| `TERMS.outcomes`               | Learning outcomes of the unit (optional)            | "Demonstrate an understanding..."                |
| `TERMS.prerequisites_text`     | Prerequisites in text format (optional)             | "Successful completion of..."                    |
| `TERMS.prerequisites_cnf`      | Prerequisites in Conjunctive Normal Form (optional) | "ACCT5432 AND ECON5541"                          |
| `TERMS.advisable_prior_study`  | Advisable prior study (optional)                    | "AGRI5402"                                       |
| `TERMS.contact`                | Contact hours information (optional)                | "Lectures: 6 hours..."                           |
| `TERMS.note`                   | Additional notes about the unit (optional)          | "..."                                            |

### Majors Schema

| RDF Property                   | Description                                         | Example Value                                    |
|--------------------------------|-----------------------------------------------------|--------------------------------------------------|
| `MAJOR:<major_code>`           | URI representing the major                          | MAJOR:MJD-AGBUS                                  |
| `RDF.type`                     | Type of the resource (always `TERMS.Major`)         | TERMS.Major                                      |
| `TERMS.code`                   | Major code                                          | "MJD-AGBUS"                                      |
| `TERMS.title`                  | Major title                                         | "Agribusiness"                                   |
| `TERMS.school`                 | School offering the major                           | "Agriculture and Environment"                    |
| `TERMS.board_of_examiners`     | Board of examiners for the major                    | "05 - Agriculture, Environmental and Related S"  |
| `TERMS.delivery_mode`          | Delivery mode of the major                          | "Face to face"                                   |
| `TERMS.description`            | Description of the major                            | "Agribusiness refers to..."                      |
| `TERMS.outcomes`               | Learning outcomes of the major                      | "Demonstrate capacity to..."                     |
| `TERMS.prerequisites`          | Prerequisites for the major (optional)              | "Mathematics Methods ATAR or..."                 |
| `TERMS.courses`                | List of courses required for the major              | "BP004, BH005"                                   |
| `TERMS.bridging`               | Bridging courses for the major (optional)           | "MATH1720, SCIE1500"                             |
| `TERMS.units`                  | List of units associated with the major             | "ACCT1100, AGRI1001, ..."                        |

## Constraints

1. Prerequisite Level Constraint
- Every prerequisite for a level X unit should have a level less than X
- The prerequisites for a unit are at a lower level than the unit itself
- For example, if a unit is at Level 3, its prerequisites should be at Level 1 or Level 2.

2. No Self-Prerequisite Constraint
- No unit should be its own prerequisite
- A unit cannot require itself as a prerequisite for completion

3. Contact Hours Constraint
- No major should require more than 40 contact hours per week
- Limits the total contact hours (e.g., lecture hours, lab hours) per week for any major to be no more than 40 hours

## Ontology Rules


# Executing Queries



# Instructions
## How to add data

## How to update data

## How to remove data

## How to add rules

## How to update rules

## How to remove rules

## How to check consistency

## How to identify errors