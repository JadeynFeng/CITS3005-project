from rdflib import Graph, Literal, Namespace, RDF, XSD
import json

# Create a new RDF graph
g = Graph()

# Define namespaces for your RDF data
UNIT = Namespace("http://uwabookofknowledge.org/unit/")
MAJOR = Namespace("http://uwabookofknowledge.org/major/")
TERMS = Namespace("http://uwabookofknowledge.org/terms/")
PREREQ = Namespace("http://uwabookofknowledge.org/prereq/")
CONTACT = Namespace("http://uwabookofknowledge.org/contact/")

# Load JSON data from the file
with open("units.json", "r") as json_file:
    units_data = json.load(json_file)
    
with open("majors.json", "r") as json_file:
    majors_data = json.load(json_file)

# Iterate through the units JSON data and create RDF triples
for unit_code, unit_data in units_data.items():
    unit_uri = UNIT[unit_code]

    # Add RDF triples for each unit attribute
    g.add((unit_uri, RDF.type, TERMS.Unit))
    g.add((unit_uri, TERMS.unitCode, Literal(unit_data["code"])))
    g.add((unit_uri, TERMS.unitTitle, Literal(unit_data["title"])))
    g.add((unit_uri, TERMS.unitSchool, Literal(unit_data["school"])))
    g.add((unit_uri, TERMS.unitBoard, Literal(unit_data["board_of_examiners"])))
    g.add((unit_uri, TERMS.unitDelivery, Literal(unit_data["delivery_mode"])))
    g.add((unit_uri, TERMS.level, Literal(unit_data["level"], datatype=XSD.integer)))
    g.add((unit_uri, TERMS.unitDescription, Literal(unit_data["description"])))
    g.add((unit_uri, TERMS.credit, Literal(unit_data["credit"], datatype=XSD.integer)))
    
    for assessment in unit_data["assessment"]:
        g.add((unit_uri, TERMS.assessment, Literal(assessment)))

    # if "offering" in unit_data:
    #     g.add((unit_uri, TERMS.offering, Literal(unit_data["offering"])))

    if "majors" in unit_data:
        for major in unit_data["majors"]:
            g.add((unit_uri, TERMS.isPartOfMajor, Literal(major)))
    
    if "outcomes" in unit_data:
        for outcome in unit_data["outcomes"]:
            g.add((unit_uri, TERMS.unitOutcome, Literal(outcome)))

    if "prerequisites_text" in unit_data:
        g.add((unit_uri, TERMS.unitText, Literal(unit_data["prerequisites_text"])))

    totalHours = 0
    if "contact" in unit_data:
        for contact, hours in unit_data["contact"].items():
            contact_uri = CONTACT[unit_code+"_"+contact.lower().replace(" ", "_")]
            g.add((contact_uri, RDF.type, TERMS.Contact))
            g.add((contact_uri, TERMS.activity, Literal(contact)))
            g.add((contact_uri, TERMS.hours, Literal(hours, datatype=XSD.integer)))
            g.add((unit_uri, TERMS.contact, contact_uri))
            totalHours += int(hours)
    g.add((unit_uri, TERMS.totalHours, Literal(totalHours, datatype=XSD.integer)))
            
    if "note" in unit_data:
        g.add((unit_uri, TERMS.note, Literal(unit_data["note"])))

# Iterate through the units JSON data to store prerequisites in RDF
for unit_code, unit_data in units_data.items():
    unit_uri = UNIT[unit_code]
    if "prerequisites_cnf" in unit_data:
        counter = 0 
        for prereq_list in unit_data["prerequisites_cnf"]:
            name = unit_code+"andReqs"+str(counter)
            prereq_uri = PREREQ[name]
            g.add((prereq_uri, RDF.type, TERMS.AndReq))
            for p in prereq_list:
                g.add((prereq_uri, TERMS.orReq, UNIT[p]))
            g.add((unit_uri, TERMS.prerequisitesCNF, prereq_uri))
            counter += 1
            
    if "advisable_prior_study" in unit_data:
        for prior_study in unit_data["advisable_prior_study"]:
            prior_uri = UNIT[prior_study]
            g.add((unit_uri, TERMS.advisablePriorStudy, prior_uri))
    
# Iterate through the majors JSON data and create RDF triples
for major_code, major_data in majors_data.items():
    major_uri = MAJOR[major_code]

    # Add RDF triples for each major attribute
    g.add((major_uri, RDF.type, TERMS.Major))
    g.add((major_uri, TERMS.majorCode, Literal(major_code)))
    g.add((major_uri, TERMS.majorTitle, Literal(major_data["title"])))
    g.add((major_uri, TERMS.majorSchool, Literal(major_data["school"])))
    g.add((major_uri, TERMS.majorBoard, Literal(major_data["board_of_examiners"])))
    g.add((major_uri, TERMS.majorDelivery, Literal(major_data["delivery_mode"])))
    g.add((major_uri, TERMS.najorDescription, Literal(major_data["description"])))
    
    for outcome in major_data["outcomes"]:
        g.add((major_uri, TERMS.majorOutcome, Literal(outcome)))
    
    if "prerequisites" in major_data:
        g.add((major_uri, TERMS.majorText, Literal(major_data["prerequisites"])))
    
    for course in major_data["courses"]:
        g.add((major_uri, TERMS.course, Literal(course)))
        
    for bridge in major_data["bridging"]:
        g.add((major_uri, TERMS.bridging, UNIT[bridge]))
        
    for unit in major_data["units"]:
        g.add((major_uri, TERMS.containsUnit, UNIT[unit]))

g.bind("terms",TERMS)
g.bind("unit", UNIT)
g.bind("major", MAJOR)
g.bind("prereq", PREREQ)
g.bind("contact", CONTACT)

# Serialize the RDF graph to a file (e.g., in Turtle format)
g.serialize("project.rdf", format="xml")

# QUERIES ===============================================================
print("======================= QUERIES =======================")
# Query 1 : Find all units with more than 6 outcomes  
print("Query 1 : Find all units with more than 6 outcomes")
q1 = """
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    PREFIX unit: <http://uwabookofknowledge.org/unit/>

    SELECT DISTINCT ?code ?title (COUNT(?outcomes) AS ?c)
    WHERE {
        ?unit rdf:type terms:Unit . 
        ?unit terms:unitCode ?code .
        ?unit terms:unitTitle ?title . 
        ?unit terms:unitOutcome ?outcomes .
    }
    GROUP BY ?code
    HAVING (COUNT(?outcomes) > 6)
"""
# for row in g.query(q1):
#     print(f"- {row.code}, {row.title}, {row.c}")
# print("-------------------------------------------------------")
    
# Query 2 : Find all level 3 units that do not have an exam, and where none of their prerequisites have an exam
print("Query 2 : Find all level 3 units that do not have an exam, and where none of their prerequisites have an exam")
q2 = """
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    
    SELECT ?code ?title
    WHERE {
        ?unit rdf:type terms:Unit .
        ?unit terms:unitCode ?code .
        ?unit terms:unitTitle ?title .
        ?unit terms:level "3" .
        
        FILTER NOT EXISTS {
            ?unit terms:assessment ?assessment .
            FILTER(REGEX(?assessment, "exam", "i"))
        }

        FILTER NOT EXISTS {
            ?unit terms:prerequisitesCNF ?andReq . 
            ?andReq rdf:type terms:AndReq . 
            ?andReq terms:orReq ?orReq . 
            ?orReq terms:unitCode ?pre .
            ?orReq terms:assessment ?test .
            FILTER(REGEX(?test, "exam", "i"))
        }
    } 
"""
# for row in g.query(q2):
#     print(f"- {row.code}, {row.title}")
# print("-------------------------------------------------------")

# Query 3 : Find all units that appear in more than 3 majors
print("Query 3 : Find all units that appear in more than 3 majors")
q3 = """
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    PREFIX major: <http://uwabookofknowledge.org/major/>
    
    SELECT ?code ?title (COUNT(?major) AS ?m)
    WHERE {
        ?maj rdf:type terms:Major .
        ?maj terms:majorTitle ?major . 
        ?maj terms:containsUnit ?unit . 
        ?unit rdf:type terms:Unit .
        ?unit terms:unitCode ?code. 
        ?unit terms:unitTitle ?title. 
    }
    GROUP BY ?code
    HAVING (COUNT(?major) > 3)     
"""
# for row in g.query(q3):
#     print(f"- {row.code}, {row.title}, {row.m}")
# print("-------------------------------------------------------")

# Query 4 : Basic search functionality in unit's description or outcomes
print("Query 4 : Basic search functionality in unit's description or outcomes")
user_input = input("Enter a search query: ")
q4 = f"""
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    PREFIX terms: <http://uwabookofknowledge.org/terms/>

    SELECT DISTINCT ?code ?title
    WHERE {{
        ?unit rdf:type terms:Unit .
        ?unit terms:unitCode ?code .
        ?unit terms:unitTitle ?title .
        
        {{ ?unit terms:unitDescription ?description . FILTER(CONTAINS(UCASE(?description), UCASE("{user_input}"))) }}
        UNION
        {{ ?unit terms:unitOutcome ?outcome . FILTER(CONTAINS(UCASE(?outcome), UCASE("{user_input}"))) }}
    }}
"""
# for row in g.query(q4):
#     print(f"- {row.code}, {row.title}")
# print("-------------------------------------------------------")

# Query 5 : Find all units with a specific major
print("Query 5 : Find all units with a specific major")
user_input = input("Enter a major code: ")
q5 = f"""
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    PREFIX major: <http://uwabookofknowledge.org/major/>
    
    SELECT ?code ?title
    WHERE {{
        ?major terms:majorCode "{user_input}" .
        ?major terms:containsUnit ?unit .
        ?unit terms:unitCode ?code .
        ?unit terms:unitTitle ?title .
    }}
"""
# for row in g.query(q5):
#     print(f"- {row.code}, {row.title}")
# print("-------------------------------------------------------")

# Query 6 : Find all prerequisites for a given unit
print("Query 6 : Find all prerequisites for a given unit")
user_input = input("Enter a unit code: ")
q6 = f"""
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    PREFIX major: <http://uwabookofknowledge.org/major/>
    PREFIX prereq: <http://uwabookofknowledge.org/prereq/>
    
    SELECT ?code ?title
    WHERE {{
        unit:{user_input} terms:prerequisitesCNF ?prereq_group .
        ?prereq_group rdf:type terms:AndReq .
        ?prereq_group terms:orReq ?prereq_unit .
        ?prereq_unit terms:unitCode ?code .
        ?prereq_unit terms:unitTitle ?title .
    }}
"""
# for row in g.query(q6):
#     print(f"- {row.code}, {row.title}")
# print("-------------------------------------------------------")

# Query 7 : Find all units with a specific level
print("Query 7 : Find all units with a specific level")
user_input = input("Enter a level: ")
q7 = f"""
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    PREFIX major: <http://uwabookofknowledge.org/major/>
    
    SELECT ?code ?title
    WHERE {{
        ?unit rdf:type terms:Unit .
        ?unit terms:level ?level .
        ?unit terms:unitCode ?code .
        ?unit terms:unitTitle ?title .
        FILTER (?level = "{user_input}")
    }}
"""
# for row in g.query(q7):
#     print(f"- {row.code}, {row.title}")
# print("-------------------------------------------------------")

# Query 8 : Find units with 12 credit points
print("Query 8 : Find units with 12 credit points")
q8 = """
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    
    SELECT ?code ?title
    WHERE {
        ?unit rdf:type terms:Unit .
        ?unit terms:credit ?credit .
        ?unit terms:unitCode ?code .
        ?unit terms:unitTitle ?title .
        FILTER (?credit = "12")
    }
"""
# for row in g.query(q8):
#     print(f"- {row.code}, {row.title}")
# print("-------------------------------------------------------")

# Query 9 : Find all majors that require a specific unit
print("Query 9 : Find all majors that require a specific unit")
user_input = input("Enter a unit code: ")
q9 = f"""
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    PREFIX major: <http://uwabookofknowledge.org/major/>
    
    SELECT ?code ?title
    WHERE {{
        ?major rdf:type terms:Major .
        ?major terms:containsUnit unit:{user_input} .
        ?major terms:majorCode ?code .
        ?major terms:majorTitle ?title .
    }}
"""
# for row in g.query(q9):
#     print(f"- {row.code}, {row.title}")
# print("-------------------------------------------------------")

# Query 10 : Find units with a specific delivery mode
print("Query 10 : Find units with a specific delivery mode (Face to face, Online, Both)")
user_input = input("Enter a delivery mode ('Face to face', 'Online', 'Both'): ").capitalize()
q10 = f"""
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    
    SELECT ?code ?title
    WHERE {{
        ?unit rdf:type terms:Unit .
        ?unit terms:unitDelivery ?mode .
        ?unit terms:unitCode ?code .
        ?unit terms:unitTitle ?title .
        FILTER (?mode = "{user_input}")
    }}
"""
# for row in g.query(q10):
#     print(f"- {row.code}, {row.title}")
# print("-------------------------------------------------------")


# Query 11: Find units with school in Molecular Sciences and is 6 credit points. 
print("Query 11 : Find units with school in Molecular Sciences and is 6 credit points")
q11 = """
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    
    SELECT ?code ?title
    WHERE {
        ?unit rdf:type terms:Unit .
        ?unit terms:unitCode ?code .
        ?unit terms:unitTitle ?title .
        ?unit terms:unitSchool "Molecular Sciences" . 
        ?unit terms:credit "6" . 
    }
"""
# for row in g.query(q11):
#     print(f"- {row.code}, {row.title}")
# print("-------------------------------------------------------")

# Query 12 : Find all Molecular Sciences units that do not have BIOC2002 as a prerequisite
print("Query 12 : Find all Molecular Sciences units that do not have BIOC2002 as a prerequisite")
q12 = """
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    
    SELECT ?code ?title
    WHERE {
        ?unit rdf:type terms:Unit .
        ?unit terms:unitCode ?code .
        ?unit terms:unitTitle ?title .
        ?unit terms:unitSchool "Molecular Sciences" . 

        FILTER NOT EXISTS {
            ?unit terms:prerequisitesCNF ?andReq . 
            ?andReq rdf:type terms:AndReq . 
            ?andReq terms:orReq ?orReq . 
            ?orReq terms:unitCode ?pre .
            FILTER(REGEX(?pre, "BIOC2002", "i"))
        }
    } 
"""
for row in g.query(q12):
    print(f"- {row.code}, {row.title}")
print("-------------------------------------------------------")
