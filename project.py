from rdflib import Graph, Literal, Namespace, RDF, URIRef
import json

# Create a new RDF graph
g = Graph()

# Define namespaces for your RDF data
UNIT = Namespace("http://uwabookofknowledge.org/unit/")
MAJOR = Namespace("http://uwabookofknowledge.org/major/")
TERMS = Namespace("http://uwabookofknowledge.org/terms/")
PREREQ = Namespace("http://uwabookofknowledge.org/prereq/")

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
    g.add((unit_uri, TERMS.code, Literal(unit_data["code"])))
    g.add((unit_uri, TERMS.title, Literal(unit_data["title"])))
    g.add((unit_uri, TERMS.school, Literal(unit_data["school"])))
    g.add((unit_uri, TERMS.board_of_examiners, Literal(unit_data["board_of_examiners"])))
    g.add((unit_uri, TERMS.delivery_mode, Literal(unit_data["delivery_mode"])))
    g.add((unit_uri, TERMS.level, Literal(unit_data["level"])))
    g.add((unit_uri, TERMS.description, Literal(unit_data["description"])))
    g.add((unit_uri, TERMS.credit, Literal(unit_data["credit"])))
    
    for assessment in unit_data["assessment"]:
        g.add((unit_uri, TERMS.assessment, Literal(assessment)))

    if "offering" in unit_data:
        g.add((unit_uri, TERMS.offering, Literal(unit_data["offering"])))

    if "majors" in unit_data:
        for major in unit_data["majors"]:
            g.add((unit_uri, TERMS.majors, Literal(major)))
    
    if "outcomes" in unit_data:
        for outcome in unit_data["outcomes"]:
            g.add((unit_uri, TERMS.outcomes, Literal(outcome)))

    if "prerequisites_text" in unit_data:
        g.add((unit_uri, TERMS.prerequisites_text, Literal(unit_data["prerequisites_text"])))
    

    if "advisable_prior_study" in unit_data:
        for prior_study in unit_data["advisable_prior_study"]:
            g.add((unit_uri, TERMS.advisable_prior_study, Literal(prior_study)))

    if "contact" in unit_data:
        for key, value in unit_data["contact"].items():
            g.add((unit_uri, TERMS.contact, Literal(f"{key}: {value}")))

    if "note" in unit_data:
        g.add((unit_uri, TERMS.note, Literal(unit_data["note"])))

for unit_code, unit_data in units_data.items():
    if "prerequisites_cnf" in unit_data:
        unit_uri = UNIT[unit_code]
        counter = 0 
        for prereq_list in unit_data["prerequisites_cnf"]:
            name = unit_code+"andReqs"+str(counter)
            prereq = PREREQ[name]
            g.add((prereq, RDF.type, TERMS.AndReq))
            for p in prereq_list:
                g.add((prereq, TERMS.orReqs, UNIT[p]))
            g.add((unit_uri, TERMS.prerequisites_cnf, prereq))
            counter += 1

        
# Iterate through the majors JSON data and create RDF triples
for major_code, major_data in majors_data.items():
    major_uri = MAJOR[major_code]

    # Add RDF triples for each major attribute
    g.add((major_uri, RDF.type, TERMS.Major))
    g.add((major_uri, TERMS.code, Literal(major_code)))
    g.add((major_uri, TERMS.title, Literal(major_data["title"])))
    g.add((major_uri, TERMS.school, Literal(major_data["school"])))
    g.add((major_uri, TERMS.board_of_examiners, Literal(major_data["board_of_examiners"])))
    g.add((major_uri, TERMS.delivery_mode, Literal(major_data["delivery_mode"])))
    g.add((major_uri, TERMS.description, Literal(major_data["description"])))
    
    for outcome in major_data["outcomes"]:
        g.add((major_uri, TERMS.outcomes, Literal(outcome)))
    
    if "prerequisites" in major_data:
        g.add((major_uri, TERMS.prerequisites, Literal(major_data["prerequisites"])))
    
    for course in major_data["courses"]:
        g.add((major_uri, TERMS.courses, Literal(course)))
        
    for bridge in major_data["bridging"]:
        g.add((major_uri, TERMS.bridging, Literal(bridge)))
        
    for unit in major_data["units"]:
        g.add((major_uri, TERMS.units, UNIT[unit]))

g.bind("terms",TERMS)
g.bind("unit", UNIT)
g.bind("major", MAJOR)
g.bind("prereq", PREREQ)

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
        ?unit terms:code ?code .
        ?unit terms:title ?title . 
        ?unit terms:outcomes ?outcomes .
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
        ?unit terms:code ?code .
        ?unit terms:title ?title .
        ?unit terms:level "3" .
        
        FILTER NOT EXISTS {
            ?unit terms:assessment ?assessment .
            FILTER(REGEX(?assessment, "exam", "i"))
        }

        FILTER NOT EXISTS {
            ?unit terms:prerequisites_cnf ?andReq . 
            ?andReq rdf:type terms:AndReq . 
            ?andReq terms:orReqs ?orReq . 
            ?orReq terms:code ?pre .
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
        ?maj terms:title ?major . 
        ?maj terms:units ?unit . 
        ?unit rdf:type terms:Unit .
        ?unit terms:code ?code. 
        ?unit terms:title ?title. 
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
        ?unit terms:code ?code .
        ?unit terms:title ?title .
        
        {{ ?unit terms:description ?description . FILTER(CONTAINS(UCASE(?description), UCASE("{user_input}"))) }}
        UNION
        {{ ?unit terms:outcomes ?outcome . FILTER(CONTAINS(UCASE(?outcome), UCASE("{user_input}"))) }}
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
        ?major terms:code "{user_input}" .
        ?major terms:units ?unit .
        ?unit terms:code ?code .
        ?unit terms:title ?title .
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
        unit:{user_input} terms:prerequisites_cnf ?prereq_group .
        ?prereq_group rdf:type terms:AndReq .
        ?prereq_group terms:orReqs ?prereq_unit .
        ?prereq_unit terms:code ?code .
        ?prereq_unit terms:title ?title .
    }}
"""
# for row in g.query(q6):
#     print(f"- {row.code}, {row.title}")
# print("-------------------------------------------------------")

# Query 7 : Find all units with a specific level
print("Query 7 : Find all units with a specific level")
user_input = input("Enter a level (1-5): ")
q7 = f"""
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    PREFIX major: <http://uwabookofknowledge.org/major/>
    
    SELECT ?code ?title
    WHERE {{
        ?unit rdf:type terms:Unit .
        ?unit terms:level ?level .
        ?unit terms:code ?code .
        ?unit terms:title ?title .
        FILTER (?level = "{user_input}")
    }}
"""
# for row in g.query(q7):
#     print(f"- {row.code}, {row.title}")
# print("-------------------------------------------------------")

# Query 8 : Find units with credit level 12
print("Query 8 : Find units with credit level 12")
q8 = """
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    
    SELECT ?code ?title
    WHERE {
        ?unit rdf:type terms:Unit .
        ?unit terms:credit ?credit .
        ?unit terms:code ?code .
        ?unit terms:title ?title .
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
        ?major terms:units unit:{user_input} .
        ?major terms:code ?code .
        ?major terms:title ?title .
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
        ?unit terms:delivery_mode ?mode .
        ?unit terms:code ?code .
        ?unit terms:title ?title .
        FILTER (?mode = "{user_input}")
    }}
"""
# for row in g.query(q10):
#     print(f"- {row.code}, {row.title}")
# print("-------------------------------------------------------")


# Query 11: Find units with school in Molecular Sciences and is 6 points. 
print("Query 11 : Find units with the prerequisite BIOC1001")
q11 = """
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    
    SELECT ?code ?title
    WHERE {
        ?unit rdf:type terms:Unit .
        ?unit terms:code ?code .
        ?unit terms:title ?title .
        ?unit terms:school "Molecular Sciences" . 
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
        ?unit terms:code ?code .
        ?unit terms:title ?title .
        ?unit terms:school "Molecular Sciences" . 

        FILTER NOT EXISTS {
            ?unit terms:prerequisites_cnf ?andReq . 
            ?andReq rdf:type terms:AndReq . 
            ?andReq terms:orReqs ?orReq . 
            ?orReq terms:code ?pre .
            FILTER(REGEX(?pre, "BIOC2002", "i"))
        }
    } 
"""
for row in g.query(q12):
    print(f"- {row.code}, {row.title}")
print("-------------------------------------------------------")
