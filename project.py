from rdflib import Graph, Literal, Namespace, RDF, URIRef
import json

# Create a new RDF graph
g = Graph()

# Define namespaces for your RDF data
UNIT = Namespace("http://uwabookofknowledge.org/unit/")
MAJOR = Namespace("http://uwabookofknowledge.org/major/")
TERMS = Namespace("http://uwabookofknowledge.org/terms/")

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
    
    if "prerequisites_cnf" in unit_data:
        for prereq_list in unit_data["prerequisites_cnf"]:
            for prereq in prereq_list:
                g.add((unit_uri, TERMS.prerequisites_cnf, Literal(prereq)))

    if "advisable_prior_study" in unit_data:
        for prior_study in unit_data["advisable_prior_study"]:
            g.add((unit_uri, TERMS.advisable_prior_study, Literal(prior_study)))

    if "contact" in unit_data:
        for key, value in unit_data["contact"].items():
            g.add((unit_uri, TERMS.contact, Literal(f"{key}: {value}")))

    if "note" in unit_data:
        g.add((unit_uri, TERMS.note, Literal(unit_data["note"])))


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
        g.add((major_uri, TERMS.units, Literal(unit)))

g.bind("terms",TERMS)
g.bind("unit", UNIT)
g.bind("major", MAJOR)

# Serialize the RDF graph to a file (e.g., in Turtle format)
g.serialize("project.rdf", format="turtle")

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
for row in g.query(q1):
    print(f"- {row.code}, {row.title}, {row.c}")
print("-------------------------------------------------------")
    
# Query 2 : Find all level 3 units that do not have an exam, and where none of their prerequisites have an exam
# print("Query 2 : Find all level 3 units that do not have an exam, and where none of their prerequisites have an exam")
# q2 = """
#     PREFIX terms: <http://uwabookofknowledge.org/terms/>
#     PREFIX unit: <http://uwabookofknowledge.org/unit/>
    
#     SELECT ?code ?title ?p
#     WHERE {
#         ?unit rdf:type terms:Unit .
#         ?unit terms:code ?code .
#         ?unit terms:title ?title .
#         ?unit terms:level "3" .
#         ?unit terms:prerequisites_cnf ?p . 
        
#         FILTER NOT EXISTS {
#             ?unit terms:assessment ?assessment .
#             FILTER(REGEX(?assessment, "exam", "i"))
#         }
        
#         FILTER NOT EXISTS {
#             ?unit terms:prerequisites_cnf ?prereq .
#             ?a terms:code ?prereq .
#             ?a rdf:type terms:Unit .
#             ?a terms:assessment ?prereqAssessment .
#             FILTER(REGEX(?prereqAssessment, "exam", "i"))
#         }
        
#     }
# """
# for row in g.query(q3):
#     print(f"- {row.code}, {row.title}, {row.p}")
# print("-------------------------------------------------------")

# Query 3 : Find all units that appear in more than 3 majors
print("Query 3 : Find all units that appear in more than 3 majors")
q3 = """
    PREFIX terms: <http://uwabookofknowledge.org/terms/>
    PREFIX unit: <http://uwabookofknowledge.org/unit/>
    PREFIX major: <http://uwabookofknowledge.org/major/>
    
    SELECT ?code ?title (COUNT(?major) AS ?c)
    WHERE {
        ?unit rdf:type terms:Unit .
        ?unit terms:code ?code .
        ?unit terms:title ?title .
        ?unit terms:majors ?major .
    }
    GROUP BY ?code
    HAVING (COUNT(?major) > 3)
        
"""
for row in g.query(q3):
    print(f"- {row.code}, {row.title}, {row.c}")
print("-------------------------------------------------------")

# Query 4 : Find all units that appear in more than 3 majors
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
for row in g.query(q4):
    print(f"- {row.code}, {row.title}")
print("-------------------------------------------------------")