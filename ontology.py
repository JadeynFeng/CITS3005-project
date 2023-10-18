from owlready2 import *
from rdflib import Graph, Literal, Namespace, RDF, XSD

UNIT = Namespace("http://uwabookofknowledge.org/unit/")
MAJOR = Namespace("http://uwabookofknowledge.org/major/")
TERMS = Namespace("http://uwabookofknowledge.org/terms/")
PREREQ = Namespace("http://uwabookofknowledge.org/prereq/")
CONTACT = Namespace("http://uwabookofknowledge.org/contact/")

# Load the knowledge graph for UWA handbook
handbook = Graph()
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
    
    for subj in handbook.subjects(RDF.type, TERMS.Contact, unique=True):
        current_code = str(subj).split('/')[-1]
        new_contact = Contact(current_code)
        for pred, obj in handbook.predicate_objects(subj):
            if pred == TERMS.activity:
                new_contact.activity.append(obj.value)
            elif pred == TERMS.hours:
                new_contact.hours.append(obj.value)

    for subj in handbook.subjects(RDF.type, TERMS.Unit, unique=True):
        current_code = str(subj).split('/')[-1]
        new_unit = Unit(current_code)
        for pred, obj in handbook.predicate_objects(subj):
            if pred == TERMS.unitCode:
                new_unit.unitCode = obj.value
            elif pred == TERMS.unitTitle:
                new_unit.unitTitle = obj.value
            elif pred == TERMS.unitSchool:
                new_unit.unitSchool.append(obj.value)
            elif pred == TERMS.unitBoard:
                new_unit.unitBoard.append(obj.value)
            elif pred == TERMS.unitDelivery:
                new_unit.unitDelivery.append(obj.value)
            elif pred == TERMS.level:
                new_unit.level.append(obj.value)
            elif pred == TERMS.unitDescription:
                new_unit.unitDescription.append(obj.value)
            elif pred == TERMS.credit:
                new_unit.credit.append(obj.value)
            elif pred == TERMS.assessment:
                new_unit.assessment.append(obj.value)
            # elif pred == TERMS.prerequisitesCNF:
            #     new_unit.prerequisitesCNF.append(obj.value)
            # elif pred == TERMS.orReq:
            #     new_unit.orReq.append(obj.value)
            elif pred == TERMS.isPartOfMajor:
                new_unit.isPartOfMajor.append(obj.value)
            elif pred == TERMS.unitOutcome:
                new_unit.unitOutcome.append(obj.value)
            elif pred == TERMS.unitText:
                new_unit.unitText.append(obj.value)
            elif pred == TERMS.contact:
                current_contact = str(obj).split('/')[-1]
                new_unit.contact.append(onto[current_contact])
            elif pred == TERMS.activity:
                new_unit.activity.append(obj.value)
            elif pred == TERMS.hours:
                new_unit.hours.append(obj.value)
            elif pred == TERMS.note:
                new_unit.note.append(obj.value)
            # elif pred == TERMS.advisablePriorStudy:
            #     new_unit.advisablePriorStudy.append(obj.value)

    for subj in handbook.subjects(RDF.type, TERMS.Major, unique=True):
        current_code = str(subj).split('/')[-1]
        new_major = Major(current_code)
        for pred, obj in handbook.predicate_objects(subj):
            if pred == TERMS.majorCode:
                new_major.majorCode = obj.value
            elif pred == TERMS.majorTitle:
                new_major.majorTitle = obj.value
            elif pred == TERMS.majorSchool:
                new_major.majorSchool.append(obj.value)
            elif pred == TERMS.majorBoard:
                new_major.majorBoard.append(obj.value)
            elif pred == TERMS.majorDelivery:
                new_major.majorDelivery.append(obj.value)
            elif pred == TERMS.majorDescription:
                new_major.majorDescription.append(obj.value)
            elif pred == TERMS.majorOutcome:
                new_major.majorOutcome.append(obj.value)
            elif pred == TERMS.majorText:
                new_major.majorText.append(obj.value)
            elif pred == TERMS.course:
                new_major.course.append(obj.value)
            elif pred == TERMS.bridging:
                unit = str(obj).split('/')[-1]
                new_major.bridging.append(onto[unit])
            elif pred == TERMS.containsUnit:
                unit = str(obj).split('/')[-1]
                new_major.containsUnit.append(onto[unit])

# sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)

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
