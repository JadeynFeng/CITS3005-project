from owlready2 import *

onto_path.append(".")
onto = get_ontology("ontology.owl").load()

def get_string_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input:
            return user_input
        else:
            print("[!] Input cannot be empty.")
            
def get_digit_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            return int(user_input)
        else:
            print("[!] Input must be a number.")
            
def get_recursive_input(prompt, property):
    while True:
        user_input = input(prompt)
        if user_input:
            property.append(user_input)
        else:
            break
        
def get_recursive_unit(prompt, property, onto, allunits):
    while True:
        user_input = input(prompt)
        if user_input:
            if onto[user_input] in allunits:
                property.append(onto[user_input])
            else:
                print(f"[!] Unit with ID {user_input} not found in the ontology.")
        else:
            break

def add_unit(onto, unit_code):
    new_unit = onto.Unit(unit_code)
    new_unit.unitCode = unit_code
    new_unit.unitTitle = get_string_input("Unit Title: ")
    new_unit.unitSchool = get_string_input("Unit School: ")
    new_unit.unitBoard = get_string_input("Unit Board of Examiners: ")
    user_input = get_string_input("Unit Delivery Mode (Face to face/Online/Both/None): ")
    if user_input in ["Face to face", "Online", "Both"]:
        new_unit.unitDelivery = user_input
    elif user_input == "None":
        new_unit.unitDelivery = ""
    new_unit.level = get_digit_input("Unit Level: ")
    new_unit.unitDescription = get_string_input("Unit Description: ")
    new_unit.credit = get_digit_input("Unit Credit: ")
    get_recursive_input("Unit Assessment (leave blank to finish): ", new_unit.assessment)
    get_recursive_input("Part of Majors (leave blank to finish): ", new_unit.isPartOfMajor)
    get_recursive_input("Unit Outcome (leave blank to finish): ", new_unit.unitOutcome)
    new_unit.unitText.append(get_string_input("Required Text: "))
    new_unit.note.append(get_string_input("Additional Note: "))
    
    user_input = input('Prerequisite CNF (eg. [ACCT5432]^[ECON5541,ECON3300] ): ')
    group = user_input.split("^")
    counter = 0 
    for g in group:
        new_prereq = onto.Prerequisite(unit_code+"andReqs"+str(counter))
        counter += 1
        new_unit.prerequisitesCNF.append(new_prereq)
        for unit in g[1:-1].split(","): 
            if onto[unit] in allunits:
                new_prereq.orReq.append(onto[unit])
            else:
                req = onto.Unit(unit)
                new_prereq.orReq.append(req)

    counter = 0 
    while True: 
        user_input = input("Contact type and hour (eg lecture-6) (leave blank to finish): ")
        if user_input: 
            new_contact = onto.Contact(unit_code+"contact"+str(counter))
            counter  += 1
            new_unit.contact.append(new_contact)
            contact_info = user_input.split("-")
            new_contact.activity = contact_info[0] 
            new_contact.hours = int(contact_info[1])
        else:
            break
    
def add_major(onto, major_code):
    new_major = onto.Major(major_code)
    new_major.majorCode = major_code
    new_major.majorTitle = get_string_input("Major Title: ")
    new_major.majorSchool = get_string_input("Major School: ")
    new_major.majorBoard = get_string_input("Major Board: ")
    user_input = get_string_input("Major Delivery Mode (Face to face/Online/Both/None): ")
    if user_input in ["Face to face", "Online", "Both"]:
        new_major.majorDelivery = user_input
    elif user_input == "None":
        new_major.majorDelivery = ""
    new_major.majorDescription = get_string_input("Major Description: ")
    new_major.majorText.append(get_string_input("Required Text: "))
    get_recursive_input("Major Outcome (leave blank to finish): ", new_major.majorOutcome)
    get_recursive_input("Course (leave blank to finish): ", new_major.course)
    get_recursive_unit("Bridging Unit (leave blank to finish): ", new_major.bridging, onto, allunits)
    get_recursive_unit("Core Unit (leave blank to finish): ", new_major.containsUnit, onto, allunits)

def delete_action(entity_code):
    if onto[entity_code] in allunits:
        for i in onto[entity_code].contact:
            destroy_entity(i)
        for i in onto[entity_code].prerequisitesCNF:
            destroy_entity(i)
        destroy_entity(onto[entity_code])
        print(f"Successfully removed unit {entity_code}.")
    elif onto[entity_code] in onto.Major.instances():
        destroy_entity(onto[entity_code])
        print(f"Successfully removed major {entity_code}.")
    else:
        print(f"Unit or major code {entity_code} not found in the ontology.")

with onto:
    allunits = onto.Unit.instances()
    
    while True:
        print("\n========================== ACTIONS ==========================")
        print("1. Add a new unit")
        print("2. Add a new major")
        print("3. Remove a unit or major")
        print("0. Exit")

        action = input("Select an action number: ")
        
        # Exit the program
        if action == "0":
            break
        
        # Add a new unit entity
        elif action == "1":
            print("\nAdding a new unit...")
            unit_code = input("Unit Code: ")
            add_unit(onto, unit_code)

        # Add a new major entity
        elif action == "2":
            print("\nAdding a new major...")
            major_code = input("Major Code: ")
            add_major(onto, major_code)
                
        # Remove a unit or major entity
        elif action == "3":
            print("\nRemoving a unit or major...")
            entity_code = input("Enter unit or major code: ")
            delete_action(entity_code)
            
        else:
            print("Invalid action number.")

print("Exiting...")

# Save the updated ontology to file
onto.save(file = "updated.owl", format = "rdfxml")