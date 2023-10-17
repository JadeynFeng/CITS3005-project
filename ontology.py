from owlready2 import *
onto_path.append(".")
onto = get_ontology("/project.rdf").load()

with onto:
    # Define classes
    class Unit(Thing): pass

    class Major(Thing): pass

    class Prerequisite(Thing): pass

    class Contact(Thing): pass

    # Define object properties
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
        # inverse_property = is_part_of_major
        
    # # Define rules
    # class PrerequisiteOfPrerequisite(Prerequisite >> Prerequisite, FunctionalProperty):
    #     pass
    # class OutcomeOfCoreUnit(Outcome >> Major, FunctionalProperty):
    #     pass
    # # class PrerequisiteTextOfCoreUnit(Prerequisite >> str, FunctionalProperty):
    # #     pass

    # # Add data to Knowledge Graph
    # # Add Unit
    # new_unit = Unit("CITS1111")
    # new_unit.has_unitcode = UnitCode("CITS1111")
    # new_unit.has_unittitle = UnitTitle("Artificial Intelligence")
    # new_unit.has_unitlevel.append(1)
    # new_unit.has_outcome.append(Outcome("Learn about AI"))
    # new_unit.has_assessment.append(Assessment("Exams"))
    
    # # Add Major
    # major = Major("CS")
    # major.has_majorcode = MajorCode("CS")
    # major.has_majortitle = MajorTitle("Computer Science")
    # major.contains_unit.append(new_unit)
    # new_unit.is_part_of_major.append(major)
    
    # # Update data in Knowledge Graph
    # update_unit = onto.search_one(iri = "*CITS1111")
    # update_unit.has_unitlevel.append(3)
    # update_unit.has_outcome.append(Outcome("Learn about AI and ML"))
    # update_unit.has_assessment.append(Assessment("Exams and assignments"))
    
    # # Delete data from Knowledge Graph
    # delete_unit = onto.search_one(iri = "*CITS1111")
    # destroy_entity(delete_unit)

onto.load()
sync_reasoner()

onto.save(file = "ontology.owl", format = "rdfxml")