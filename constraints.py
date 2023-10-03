from rdflib import Graph
from pyshacl import validate

handbook = Graph()
handbook.parse('project.rdf', format='turtle')
shapes = Graph()
shapes.parse('constraints.shacl', format='turtle')

conforms, results_graph, results_text = validate(handbook, shacl_graph=shapes, inference='rdfs', abort_on_first=False, allow_infos=False, 
                                                 allow_warnings=False, meta_shacl=False, advanced=False, js=False, debug=False)

if conforms:
    print("The knowledge graph conforms to the constraints.")
else:
    print("The knowledge graph does not conform to the constraints.")
    
print(results_text)