from owlready2 import *
onto_path.append(".")
onto = get_ontology("http://uwabookofknowledge.org/onto.owl#")

with onto:
    class Unit(Thing): pass
    class UnitCode(Unit): pass # a subclass of Unit
    class UnitTitle(Unit): pass

    class Major(Thing): pass
    class MajorCode(Major): pass
    class MajorTitle(Major): pass

    class Prereq(Thing): pass
    class OrReq(Prereq): pass

    class Contact(Thing): pass

# properties ======================================
    class has_unitcode(ObjectProperty, FunctionalProperty): 
        domain = [Unit]
        range = [UnitCode]
    
    class has_unittitle(ObjectProperty, FunctionalProperty): 
        domain = [Unit]
        range = [UnitTitle]

    class has_unitlevel(DataProperty): 
        domain = [Unit]
        range = [int]
    
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

onto.save()
onto.save(file = "ontology.owl", format = "rdfxml")