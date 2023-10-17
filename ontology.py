from owlready2 import *
import rdflib 

# Load the knowledge graph for UWA handbook
handbook = rdflib.Graph()
handbook.parse('project.rdf', format='xml')

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

    # RULE 1: A prerequisite of a prerequisite is a prerequisite.
    rule1 = Imp()
    rule1.set_as_rule("""Unit(?a), Unit(?b), Prerequisite(?p), prerequisitesCNF(?a, ?p), orReq(?p, ?b), prerequisitesCNF(?b, ?q) -> prerequisitesCNF(?a, q?)""" )


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

    # Load ontology with data from knowledge graph
    





onto.save(file = "ontology.owl", format = "rdfxml")
