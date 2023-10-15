from owlready2 import *
onto_path.append(".")
onto = get_ontology("http://uwabookofknowledge.org/ontology.owl#")

with onto:
    # Define classes
    class Unit(Thing): pass
    class UnitCode(Unit): pass
    class UnitTitle(Unit): pass

    class Major(Thing): pass
    class MajorCode(Major): pass
    class MajorTitle(Major): pass

    class Prerequisite(Thing): pass
    class OrReq(Prerequisite): pass

    class Outcome(Thing): pass
    class Assessment(Thing): pass
    class Contact(Thing): pass

    # Define object properties
    class has_unitcode(ObjectProperty, FunctionalProperty): 
        domain = [Unit]
        range = [UnitCode]
    
    class has_unittitle(ObjectProperty, FunctionalProperty): 
        domain = [Unit]
        range = [UnitTitle]

    class has_unitlevel(DataProperty): 
        domain = [Unit]
        range = [int]
        
    class has_prerequisite(DataProperty):
        domain = [Unit]
        range = [Prerequisite]
        
    class has_prerequisite_text(ObjectProperty):
        domain = [Unit]
        range = [str]
        
    class has_outcome(ObjectProperty):
        domain = [Unit]
        range = [Outcome]

    class has_assessment(ObjectProperty):
        domain = [Unit]
        range = [Assessment]
    
    class is_part_of_major(ObjectProperty): 
        domain = [Unit]
        range = [Major]
            
    class has_majorcode(ObjectProperty, FunctionalProperty): 
        domain = [Major]
        range = [MajorCode]

    class has_majortitle(ObjectProperty, FunctionalProperty): 
        domain = [Major]
        range = [MajorTitle]

    class contains_unit(ObjectProperty): 
        domain = [Major]
        range = [Unit]
        inverse_property = is_part_of_major
        
    # Define rules
    class PrerequisiteOfPrerequisite(Prerequisite >> Prerequisite, FunctionalProperty):
        pass
    class OutcomeOfCoreUnit(Outcome >> Major, FunctionalProperty):
        pass
    # class PrerequisiteTextOfCoreUnit(Prerequisite >> str, FunctionalProperty):
    #     pass

    # Add data to Knowledge Graph
    # Add Unit
    new_unit = Unit("CITS1111")
    new_unit.has_unitcode = UnitCode("CITS1111")
    new_unit.has_unittitle = UnitTitle("Artificial Intelligence")
    new_unit.has_unitlevel.append(1)
    new_unit.has_outcome.append(Outcome("Learn about AI"))
    new_unit.has_assessment.append(Assessment("Exams"))
    
    # Add Major
    major = Major("CS")
    major.has_majorcode = MajorCode("CS")
    major.has_majortitle = MajorTitle("Computer Science")
    major.contains_unit.append(new_unit)
    new_unit.is_part_of_major.append(major)
    
    # Update data in Knowledge Graph
    update_unit = onto.search_one(iri = "*CITS1111")
    update_unit.has_unitlevel.append(3)
    update_unit.has_outcome.append(Outcome("Learn about AI and ML"))
    update_unit.has_assessment.append(Assessment("Exams and assignments"))
    
    # Delete data from Knowledge Graph
    delete_unit = onto.search_one(iri = "*CITS1111")
    destroy_entity(delete_unit)

onto.load()
sync_reasoner()

onto.save(file = "ontology.owl", format = "rdfxml")