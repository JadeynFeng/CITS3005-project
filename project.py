from rdflib import Graph, Literal, Namespace, RDF, URIRef

# Create a new RDF graph
g = Graph()

# Define namespaces for your RDF data
my_ns = Namespace("http://example.org/myontology#")
schema_ns = Namespace("http://schema.org/")

# Load JSON data from the file
import json

with open("units.json", "r") as json_file:
    data = json.load(json_file)

# Iterate through the JSON data and create RDF triples
for unit_code, unit_data in data.items():
    unit_uri = URIRef(f"http://example.org/units/{unit_code}")

    # Add RDF triples for each unit attribute
    g.add((unit_uri, RDF.type, schema_ns.Course))
    g.add((unit_uri, schema_ns.code, Literal(unit_code)))
    g.add((unit_uri, schema_ns.title, Literal(unit_data["title"])))
    g.add((unit_uri, schema_ns.school, Literal(unit_data["school"])))
    g.add((unit_uri, schema_ns.board_of_examiners, Literal(unit_data["board_of_examiners"])))
    g.add((unit_uri, schema_ns.delivery_mode, Literal(unit_data["delivery_mode"])))
    g.add((unit_uri, schema_ns.level, Literal(unit_data["level"])))
    g.add((unit_uri, schema_ns.description, Literal(unit_data["description"])))
    g.add((unit_uri, schema_ns.credit, Literal(unit_data["credit"])))
    
    for assessment in unit_data["assessment"]:
        g.add((unit_uri, schema_ns.assessment, Literal(assessment)))

    if "offering" in unit_data:
        g.add((unit_uri, schema_ns.offering, Literal(unit_data["offering"])))

    if "majors" in unit_data:
        for major in unit_data["majors"]:
            g.add((unit_uri, schema_ns.majors, Literal(major)))
    
    if "outcomes" in unit_data:
        for outcome in unit_data["outcomes"]:
            g.add((unit_uri, schema_ns.outcomes, Literal(outcome)))

    if "prerequisites_text" in unit_data:
        g.add((unit_uri, schema_ns.prerequisites_text, Literal(unit_data["prerequisites_text"])))
    
    if "prerequisites_cnf" in unit_data:
        for prereq_list in unit_data["prerequisites_cnf"]:
            for prereq in prereq_list:
                g.add((unit_uri, schema_ns.prerequisites_cnf, Literal(prereq)))

    if "advisable_prior_study" in unit_data:
        for prior_study in unit_data["advisable_prior_study"]:
            g.add((unit_uri, schema_ns.advisable_prior_study, Literal(prior_study)))

    if "contact" in unit_data:
        for key, value in unit_data["contact"].items():
            g.add((unit_uri, schema_ns.contact, Literal(f"{key}: {value}")))

    if "note" in unit_data:
        g.add((unit_uri, schema_ns.note, Literal(unit_data["note"])))

# Serialize the RDF graph to a file (e.g., in Turtle format)
g.serialize("units.rdf", format="turtle")
