from owlready2 import *
from rdflib import Graph, Namespace, RDF

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

    class unitSchool(DataProperty, FunctionalProperty): 
        domain = [Unit]
        range = [str]

    class unitBoard(DataProperty, FunctionalProperty): 
        domain = [Unit]
        range = [str]

    class unitDelivery(DataProperty, FunctionalProperty): 
        domain = [Unit]
        range = [str]
            
    class level(DataProperty, FunctionalProperty): 
        domain = [Unit]
        range = [int]

    class unitDescription(DataProperty, FunctionalProperty): 
        domain = [Unit]
        range = [str]
    
    class credit(DataProperty, FunctionalProperty): 
        domain = [Unit]
        range = [int]

    class assessment(DataProperty): 
        domain = [Unit]
        range = [str]

    class prerequisitesCNF(ObjectProperty):
        domain = [Unit]
        range = [Prerequisite]
        
    class orReq(ObjectProperty):
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

    class note(DataProperty):
        domain = [Unit]
        range = [str]

    class advisablePriorStudy(ObjectProperty):
        domain = [Unit]
        range = [Unit]
        
    # Define data properties for Contact entity
    class activity(DataProperty, FunctionalProperty):
        domain = [Contact]
        range = [str]

    class hours(DataProperty, FunctionalProperty):
        domain = [Contact]
        range = [int] 

    # Define object properties for Major entity
    class majorCode(DataProperty, FunctionalProperty): 
        domain = [Major]
        range = [str]

    class majorTitle(DataProperty, FunctionalProperty): 
        domain = [Major]
        range = [str]

    class majorSchool(DataProperty, FunctionalProperty): 
        domain = [Major]
        range = [str]

    class majorBoard(DataProperty, FunctionalProperty): 
        domain = [Major]
        range = [str]

    class majorDelivery(DataProperty, FunctionalProperty): 
        domain = [Major]
        range = [str]

    class majorDescription(DataProperty, FunctionalProperty): 
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
    
    # Load Handbook Knowledge Graph onto Ontology
    # Load Contact Entities
    for subj in handbook.subjects(RDF.type, TERMS.Contact, unique=True):
        current_code = str(subj).split('/')[-1]
        new_contact = Contact(current_code)
        for pred, obj in handbook.predicate_objects(subj):
            if pred == TERMS.activity:
                new_contact.activity = obj.value
            elif pred == TERMS.hours:
                new_contact.hours = obj.value

    # Load Unit Entities
    for subj in handbook.subjects(RDF.type, TERMS.Unit, unique=True):
        current_code = str(subj).split('/')[-1]
        new_unit = Unit(current_code)
        for pred, obj in handbook.predicate_objects(subj):
            if pred == TERMS.unitCode:
                new_unit.unitCode = obj.value
            elif pred == TERMS.unitTitle:
                new_unit.unitTitle = obj.value
            elif pred == TERMS.unitSchool:
                new_unit.unitSchool = obj.value
            elif pred == TERMS.unitBoard:
                new_unit.unitBoard = obj.value
            elif pred == TERMS.unitDelivery:
                new_unit.unitDelivery = obj.value
            elif pred == TERMS.level:
                new_unit.level = obj.value
            elif pred == TERMS.unitDescription:
                new_unit.unitDescription = obj.value
            elif pred == TERMS.credit:
                new_unit.credit = obj.value
            elif pred == TERMS.assessment:
                new_unit.assessment.append(obj.value)
            elif pred == TERMS.prerequisitesCNF:
                current_CNF = str(obj).split('/')[-1]
                new_prereq = Prerequisite(current_CNF)
                new_unit.prerequisitesCNF.append(new_prereq)
            elif pred == TERMS.isPartOfMajor:
                new_unit.isPartOfMajor.append(obj.value)
            elif pred == TERMS.unitOutcome:
                new_unit.unitOutcome.append(obj.value)
            elif pred == TERMS.unitText:
                new_unit.unitText.append(obj.value)
            elif pred == TERMS.contact:
                current_contact = str(obj).split('/')[-1]
                new_unit.contact.append(onto[current_contact])
            elif pred == TERMS.note:
                new_unit.note.append(obj.value)

    allunits = Unit.instances()

    for subj, obj in handbook.subject_objects(TERMS.orReq):
        current_prereqCNF = str(subj).split('/')[-1]
        current_orReq = str(obj).split('/')[-1]
        if (onto[current_orReq] in allunits):
            onto[current_prereqCNF].orReq.append(onto[current_orReq])
        else:
            new_unit = Unit(current_orReq)
            onto[current_prereqCNF].orReq.append(onto[current_orReq])

    for subj, obj in handbook.subject_objects(TERMS.advisablePriorStudy):
        current_code = str(subj).split('/')[-1]
        current_advisablePriorStudy = str(obj).split('/')[-1]
        if (onto[current_advisablePriorStudy] in allunits):
            onto[current_code].advisablePriorStudy.append(onto[current_advisablePriorStudy])
        else:
            if len(current_advisablePriorStudy) == 8: # if it is a unit code
                new_unit = Unit(current_advisablePriorStudy)
                onto[current_code].advisablePriorStudy.append(onto[current_advisablePriorStudy])

    # Load Major Entities
    for subj in handbook.subjects(RDF.type, TERMS.Major, unique=True):
        current_code = str(subj).split('/')[-1]
        new_major = Major(current_code)
        for pred, obj in handbook.predicate_objects(subj):
            if pred == TERMS.majorCode:
                new_major.majorCode = obj.value
            elif pred == TERMS.majorTitle:
                new_major.majorTitle = obj.value
            elif pred == TERMS.majorSchool:
                new_major.majorSchool = obj.value
            elif pred == TERMS.majorBoard:
                new_major.majorBoard = obj.value
            elif pred == TERMS.majorDelivery:
                new_major.majorDelivery = obj.value
            elif pred == TERMS.majorDescription:
                new_major.majorDescription = obj.value
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
                
    # SWRL rule 1: A prerequisite of a prerequisite is a prerequisite
    rule1 = Imp()
    rule1.set_as_rule("Unit(?a) ^ prerequisitesCNF(?a, ?p) ^ orReq(?p, ?b) ^ prerequisitesCNF(?b, ?q) -> prerequisitesCNF(?a, ?q)")
    
    # SWRL rule 2: An outcome of a core unit is an outcome of a major
    rule2 = Imp()
    rule2.set_as_rule("Major(?m) ^ containsUnit(?m, ?u) ^ unitOutcome(?u, ?o) -> majorOutcome(?m, ?o)")
    
    # SWRL rule 3: A required text of a core unit is a required text for a major
    rule3 = Imp()
    rule3.set_as_rule("Major(?m) ^ containsUnit(?m, ?u) ^ unitText(?u, ?t) -> majorText(?m, ?t)")

sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
onto.save(file = "ontology.owl", format = "rdfxml")

print("1. Add a new unit")
action = input("Select an action number: ")
if (action == "1"):
    value = input("Unit Code: ")
    new_unit = Unit(value)
    new_unit.unitCode = value
    value = input("Unit Title: ")
    new_unit.unitTitle = value
    value = input("Unit School: ")
    new_unit.unitSchool = value
    value = input("Unit Board of Examiners: ")
    new_unit.unitBoard = value
    value = input("Unit Delivery Mode (Face to face/Online/Both/None): ")
    if value != "None": 
        new_unit.unitDelivery = value
    else: 
        new_unit.unitDelivery = ""
    value = input("Unit Level: ")
    new_unit.level = value
    value = input("Unit Description: ")
    new_unit.unitDescription = value
    value = input("Unit Credit: ")
    new_unit.credit = value
    value = input("Unit Assessment (split by commas): ")
    v = value.split(",")
    for i in v:
        new_unit.assessment.append(i)
    value = input('Prerequisite CNF (eg. ["ACCT5432"],["ECON5541","ECON3300"] ): ')
    v = value.split(",")
    for i in v:
        new_unit.assessment.append(i)


        current_CNF = str(obj).split('/')[-1]
        new_prereq = Prerequisite(current_CNF)
        new_unit.prerequisitesCNF.append(new_prereq)
    elif pred == TERMS.isPartOfMajor:
        new_unit.isPartOfMajor.append(obj.value)
    elif pred == TERMS.unitOutcome:
        new_unit.unitOutcome.append(obj.value)
    elif pred == TERMS.unitText:
        new_unit.unitText.append(obj.value)
    elif pred == TERMS.contact:
        current_contact = str(obj).split('/')[-1]
        new_unit.contact.append(onto[current_contact])
    elif pred == TERMS.note:
        new_unit.note.append(obj.value)

    
# with onto:
#     for unit in onto.Unit.instances():
#         if unit.unitCode == "GEOG3310":
#                 for p in unit.prerequisitesCNF:
#                     print(p)
#                     for o in p.orReq:
#                         print("\t-", o.unitCode)
#     print("total:", len(onto.Unit.instances()))
    
#     count = 0
#     for major in onto.Major.instances():
#         if len(major.majorOutcome) < 30:
#             print(f"{major.majorCode} has {len(major.majorOutcome)} outcomes")
#             count += 1
#     print("count:", count, "\ntotal:", len(onto.Major.instances()))
    