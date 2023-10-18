from owlready2 import *
from rdflib import Graph, Namespace, RDF

TERMS = Namespace("http://uwabookofknowledge.org/terms/")

# Load the knowledge graph for UWA handbook
handbook = Graph()
handbook.parse('handbook.rdf', format='xml')

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

    
    
    while True:
        print("1. Add a new unit")
        print("2. Add a new major")
        print("3. Remove a unit or major")
        print("0. Exit")

        action = input("Select an action number: ")
        
        if action == "0":
            break
        
        # Add a new unit entity
        elif action == "1":
            code_value = input("Unit Code: ")
            new_unit = Unit(code_value)
            new_unit.unitCode = code_value
            new_unit.unitTitle = input("Unit Title: ")
            new_unit.unitSchool = input("Unit School: ")
            new_unit.unitBoard = input("Unit Board of Examiners: ")
            user_input = input("Unit Delivery Mode (Face to face/Online/Both/None): ")
            if user_input != "None": 
                new_unit.unitDelivery = user_input
            else: 
                new_unit.unitDelivery = ""
            new_unit.level = int(input("Unit Level: "))
            new_unit.unitDescription = input("Unit Description: ")
            new_unit.credit = int(input("Unit Credit: "))

            while True:
                user_input = input("Unit Assessment (leave blank to finish): ")
                if user_input:
                    new_unit.assessment.append(user_input)
                else:
                    break

            user_input = input('Prerequisite CNF (eg. [ACCT5432]^[ECON5541,ECON3300] ): ')
            group = user_input.split("^")
            counter = 0 
            for g in group:
                new_prereq = Prerequisite(code_value+"andReqs"+str(counter))
                counter += 1
                new_unit.prerequisitesCNF.append(new_prereq)
                for unit in g[1:-1].split(","): 
                    if onto[unit] in allunits:
                        new_prereq.orReq.append(onto[unit])
                    else:
                        req = Unit(unit)
                        new_prereq.orReq.append(req)

            while True:
                value = input('List all majors this unit is part of (leave blank to finish): ')
                if value:
                    new_unit.isPartOfMajor.append(value)
                else:
                    break  

            while True:
                user_input = input("Unit Outcome (leave blank to finish): ")
                if user_input:
                    new_unit.unitOutcome.append(user_input)
                else:
                    break        
            
            new_unit.unitText.append(input("Required Text: "))
            new_unit.note.append(input("Note (optional): "))
            
            counter = 0 
            while True: 
                user_input = input("Contact type and hour (eg lecture-6) (leave blank to finish): ")
                if user_input: 
                    new_contact = Contact(code_value+"contact"+str(counter))
                    counter  += 1
                    new_unit.contact.append(new_contact)
                    contact_info = user_input.split("-")
                    new_contact.activity = contact_info[0] 
                    new_contact.hours = int(contact_info[1])
                else:
                    break
        
        # Add a new major entity
        elif action == "2":
            code_value = input("Major Code: ")
            new_major = Major(code_value)
            new_major.majorCode = code_value
            new_major.majorTitle = input("Major Title: ")
            new_major.majorSchool = input("Major School: ")
            new_major.majorBoard = input("Major Board: ")
            user_input = input("Major Delivery Mode (Face to face/Online/Both/None): ")
            if user_input != "None": 
                new_major.majorDelivery = user_input
            else: 
                new_major.majorDelivery = ""
            new_major.majorDescription = input("Major Description: ")
            new_major.majorText.append(input("Required Text: "))

            while True:
                user_input = input("Major Outcome (leave blank to finish): ")
                if user_input:
                    new_major.majorOutcome.append(user_input)
                else:
                    break
                
            while True:
                user_input = input("Course (leave blank to finish): ")
                if user_input:
                    new_major.course.append(user_input)
                else:
                    break
                
            while True:
                user_input = input("Bridging Unit (leave blank to finish): ")
                if user_input:
                    if onto[user_input] in allunits:
                        new_major.bridging.append(onto[user_input])
                    else:
                        print(f"Unit with ID {user_input} not found in the ontology.")
                else:
                    break

            while True:
                user_input = input("Core Unit (leave blank to finish): ")
                if user_input:
                    if onto[user_input] in allunits:
                        new_major.containsUnit.append(onto[user_input])
                    else:
                        print(f"Unit with ID {user_input} not found in the ontology.")
                else:
                    break
                
        # Remove a unit or major entity
        elif action == "3":
            user_input = input("Enter unit or major code: ")
            if onto[user_input] in allunits:
                for i in onto[user_input].contact:
                    destroy_entity(i)
                for i in onto[user_input].prerequisitesCNF:
                    destroy_entity(i)
                destroy_entity(onto[user_input])
                print(f"Successfully removed unit {user_input}.")
            elif onto[user_input] in Major.instances():
                destroy_entity(onto[user_input])
                print(f"Successfully removed major {user_input}.")
            else:
                print(f"Unit or major code {user_input} not found in the ontology.")
        else:
            print("Invalid action number.")

# sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
onto.save(file = "ontology.owl", format = "rdfxml")


# # Demonstration of SWRL rules applied onto Ontology
# with onto:
#     print("\nDemonstration of SWRL rules applied onto Ontology")
#     print("\n==========================================================================")
#     print("SWRL rule 1: A prerequisite of a prerequisite is a prerequisite")
#     for unit in onto.Unit.instances():
#         if unit.unitCode == "GEOG3310":
#             for group in unit.prerequisitesCNF:
#                 for prereq in group.orReq:
#                     print(f"{group} Group has {prereq.unitCode}")
#     print("GEOG3310 has 1 prerequisite (GEOG2202) which has 4 prerequisites (GEOG1107, GEOG1106, GEOG1104, GEOG1103)")
    
#     print("\n==========================================================================")
#     print("SWRL rule 2: An outcome of a core unit is an outcome of a major")
#     for major in onto.Major.instances():
#         if len(major.majorOutcome) < 30:
#             print(f"- {major.majorCode} has {len(major.majorOutcome)} outcomes")
#     print("MJD-GRMNA major has 4 outcomes, but its core units have 23 distinct outcomes, which gives a total of 27 outcomes")
#     print("MJD-GRMNI major has 4 outcomes, but its core units have 25 distinct outcomes, which gives a total of 29 outcomes")
            
#     print("\n==========================================================================")
#     print("SWRL rule 3: A required text of a core unit is a required text for a major")
#     for major in onto.Major.instances():
#         if len(major.majorText) == 3:
#             print(f"- {major.majorCode} has {len(major.majorText)} required texts")
#     print("MJD-PSYCH, MJD-ANTHR, and MJD-PSYDM majors has 1 required text, but its core units have 2 distinct required texts, which gives a total of 3 required texts")
    
    