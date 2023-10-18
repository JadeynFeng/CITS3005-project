from rdflib import Graph
from pyshacl import validate

# Load the knowledge graph for UWA handbook
handbook = Graph()
handbook.parse('handbook.rdf', format='xml')

# Load the SHACL constraint shapes
shapes = Graph()
shapes.parse('constraints.shacl', format='turtle')

# Validate the knowledge graph against the SHACL shapes
conforms, results_graph, results_text = validate(handbook, shacl_graph=shapes, inference='rdfs', abort_on_first=False, allow_infos=False, 
                                                 allow_warnings=False, meta_shacl=False, advanced=False, js=False, debug=False)

# Print the results
print(results_text)
if conforms:
    print("The knowledge graph conforms to the constraints.")
else:
    print("The knowledge graph does not conform to the constraints.")