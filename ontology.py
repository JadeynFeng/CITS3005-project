from owlready2 import *
onto = get_ontology("http://uwabookofknowledge.org/onto.owl#")

with onto:
    class Unit(Thing): pass
    class Major(Thing): pass
    