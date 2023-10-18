from owlready2 import *
import rdflib 

# Load the knowledge graph for UWA handbook
handbook = rdflib.Graph()

onto_path.append(".")
onto = get_ontology("http://uwabookofknowledge.org/ontology.owl#")

with onto:
    # Define classes
    class Unit(Thing): pass
    class Major(Thing): pass
    class Prerequisite(Thing): pass
    class Contact(Thing): pass

    # Define object properties for Unit entity
    class unitCode(DataProperty, FunctionalProperty): 
        domain = [Unit]
        range = [str]
    
    class unitTitle(DataProperty, FunctionalProperty): 
        domain = [Unit]
        range = [str]

    class unitSchool(DataProperty): 
        domain = [Unit]
        range = [str]

    class unitBoard(DataProperty): 
        domain = [Unit]
        range = [str]

    class unitDelivery(DataProperty): 
        domain = [Unit]
        range = [str]
            
    class level(DataProperty): 
        domain = [Unit]
        range = [int]

    class unitDescription(DataProperty): 
        domain = [Unit]
        range = [str]
    
    class credit(DataProperty): 
        domain = [Unit]
        range = [int]

    class assessment(DataProperty): 
        domain = [Unit]
        range = [str]

    class prerequisitesCNF(DataProperty):
        domain = [Unit]
        range = [Prerequisite]
        
    class orReq(DataProperty):
        domain = [Prerequisite]
        range = [Unit]
   
    # Define data properties for Major entity
    class isPartOfMajor(DataProperty): 
        domain = [Unit]
        range = [str]

    class unitOutcome(DataProperty):
        domain = [Unit]
        range = [str]

    class unitText(DataProperty):
        domain = [Unit]
        range = [str]
        
    class contact(ObjectProperty):
        domain = [Unit]
        range = [Contact]
    
    class activity(DataProperty):
        domain = [Contact]
        range = [str]

    class hours(DataProperty):
        domain = [Contact]
        range = [int]   

    class note(DataProperty):
        domain = [Unit]
        range = [str]

    class advisablePriorStudy(ObjectProperty):
        domain = [Unit]
        range = [Unit]

    # Define object properties for Major entity
    class majorCode(DataProperty, FunctionalProperty): 
        domain = [Major]
        range = [str]

    class majorTitle(DataProperty, FunctionalProperty): 
        domain = [Major]
        range = [str]

    class majorSchool(DataProperty): 
        domain = [Major]
        range = [str]

    class majorBoard(DataProperty): 
        domain = [Major]
        range = [str]

    class majorDelivery(DataProperty): 
        domain = [Major]
        range = [str]

    class majorDescription(DataProperty): 
        domain = [Major]
        range = [str]

    class majorOutcome(DataProperty): 
        domain = [Major]
        range = [str]
    
    class majorText(DataProperty): 
        domain = [Major]
        range = [str]

    class course(DataProperty): 
        domain = [Major]
        range = [str]

    class bridging(ObjectProperty): 
        domain = [Major]
        range = [Unit]

    class containsUnit(ObjectProperty): 
        domain = [Major]
        range = [Unit]
        
    # SWRL rule 1: A prerequisite of a prerequisite is a prerequisite
    rule1 = Imp()
    rule1.set_as_rule("""Unit(?a) ^ Unit(?b) ^ Prerequisite(?p) ^ prerequisitesCNF(?a, ?p) ^ orReq(?p, ?b) ^ prerequisitesCNF(?b, ?q) -> prerequisitesCNF(?a, ?q)""")
    
    # SWRL rule 2: An outcome of a core unit is an outcome of a major
    rule2 = Imp()
    rule2.set_as_rule("""containsUnit(?u) ^ Major(?m) ^ unitOutcome(?u, ?o) -> majorOutcome(?m, ?o)""")
    
    # SWRL rule 3: A required text of a core unit is a required text for a major
    rule3 = Imp()
    rule3.set_as_rule("""containsUnit(?u) ^ Major(?m) ^ unitText(?u, ?t) -> majorText(?m, ?t)""")
  
    # Add Unit
    # new_unit = Unit("CITS1111")
    # new_unit.unitCode = "CITS1111"
    # new_unit.unitTitle = "Programming Fundamentals"
    # new_unit.unitSchool.append("Computer Science and Software Engineering")
    # new_unit.unitBoard.append("School of Computer Science and Software Engineering")
    # new_unit.unitDelivery.append("Crawley")
    # new_unit.level.append(1)
    # new_unit.unitDescription.append("This unit introduces the fundamental concepts.")
    # new_unit.credit.append(6)
    # new_unit.assessment.append("Examination (60%), Labs (40%)")
    # new_unit.isPartOfMajor.append("Computer Science")



from rdflib import Graph, Literal, Namespace, RDF, XSD

UNIT = Namespace("http://uwabookofknowledge.org/unit/")
MAJOR = Namespace("http://uwabookofknowledge.org/major/")
TERMS = Namespace("http://uwabookofknowledge.org/terms/")
PREREQ = Namespace("http://uwabookofknowledge.org/prereq/")
CONTACT = Namespace("http://uwabookofknowledge.org/contact/")

handbook = Graph()
handbook.parse('project.rdf', format='xml')


for subj in handbook.subjects(RDF.type, TERMS.Unit, unique=True):
    new_unit = Unit()
    for pred, obj in handbook.predicate_objects(subj):
        if pred == TERMS.unitCode:
            new_unit.unitCode.append()

# for subj, pred, obj in handbook: 
    # if (subj, pred, obj) not in handbook:
    #     raise Exception("RDF graph 'http://uwabookofknowledge.org' is empty. ")



onto.save(file = "ontology.owl", format = "rdfxml")


# # Load ontology with data from knowledge graph
# handbook.parse("ontology.owl", format="xml")
# handbook.parse("project.rdf", format="xml")

# query = """
# SELECT ?code ?title
# WHERE {
#     ?unit rdf:type terms:Unit .
#     ?unit terms:level ?level .
#     ?unit terms:unitCode ?code .
#     ?unit terms:unitTitle ?title .
#     FILTER (?level = 9)
# }
# """

# for row in handbook.query(query):
#     print(f"- {row.code}, {row.title}")
# print("-------------------------------------------------------")
