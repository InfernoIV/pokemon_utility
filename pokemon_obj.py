#imports
from termcolor import cprint #https://pypi.org/project/termcolor/
import csv, sys, operator
from constants import ___ALLOWED_TYPES___, ___CSV_TYPES___, ___CSV_TYPE_ABILITIES___
 


#base pokemon object, containing information of the pokemon
class Pokemon(object):

    #initial values
    number = ""
    name = ""
    form = ""
    classification = ""
    predecessors = []
    successors = []
    
    all_abilities = []
    abilities = []
    hidden_ability = ""
    ability_type_modifiers = []
    type = []

    

    # The class "constructor" - It's actually an initializer 
    def __init__(self):
        #to be filled in by implementors   
        pass



    def get_ability(self, ability_name):
            #to be filled in by implementors   
        pass



    #function that will print when converted to str
    def __repr__(self):
        #string to return
        string = ""
        #for each attribute
        for attr, value in self.__dict__.items():
            #add to return string
            string += f"'{attr}': '{value}', "
        #remove string while removing the last ', ' 
        return string[:-2]



    #fuction that collects the information of it's own type matchup
    #used in calculations later, can be influenced by abilities
    def get_type_matchup(self):
        #value to fill
        self.matchup = {}
        #used multiple times
        filename = ___CSV_TYPES___
        #use the csv as data source
        with open(filename) as csvfile: 
            #use a dict
            reader = csv.DictReader(csvfile)
            try:
                #check every ability
                for row in reader:
                    #get the attack type
                    attack_type = row["Type"]
                    #create list
                    self.matchup[attack_type] = []
                    #for each type
                    for type in self.type:
                        #get the modifier
                        modifier = row[type]
                        #if not set
                        if modifier == "":
                            #set to 1
                            modifier = 1
                        #Add the modifier to the list
                        self.matchup[attack_type].append(float(modifier))
            #if exception
            except csv.Error as e:
                cprint("CSV error", "red")
                #print and exit
                sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))        



    #function to return the type modifier options of a pokemon
    def get_ability_type_modifiers(self):
        #return value
        self.ability_type_modifiers = {}
        #create a list to keep track of abilities not affecting type modifiers
        abilities_not_foud = self.all_abilities.copy()
        #used multiple times
        filename = ___CSV_TYPE_ABILITIES___
        #use the csv as data source
        with open(filename) as csvfile: 
            #use a dict
            reader = csv.DictReader(csvfile)
            try:
                #check every ability
                for row in reader:
                    #get the ability
                    ability = row["Ability"]
                    #if we have this ability
                    if ability in self.all_abilities:
                        #remove from the not-found list
                        while(ability in abilities_not_foud):
                            abilities_not_foud.remove(ability)

                        #get the types
                        types = row["Type"].split(",")
                        #get the number of modifiers
                        number_of_modifiers = len(types)
                        #get the modifiers
                        modifiers = row["Modifier"].split(",")
                        #create entry for the ability
                        self.ability_type_modifiers[ability] = {}
                        #for each modifier
                        for index in range(number_of_modifiers):
                            #get the type
                            type = types[index]
                            #get the modifier
                            modifier = modifiers[index]                    
                            #write to object
                            self.ability_type_modifiers[ability][type] = float(modifier)
            #if exception
            except csv.Error as e:
                cprint("CSV error", "red")
                #print and exit
                sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))        
        #check for adding the non-affected modifiers
        if len(abilities_not_foud) > 0:
            #create a collection name
            ability_group_name = ", ".join(abilities_not_foud)
            #set to empty modifiers
            self.ability_type_modifiers[ability_group_name] = {}



    #function that will run calculations for each applicable configuration (ability setup) if needed
    def calculate_type_matchups(self):
        #value to return
        type_matchups = {}
        #for each matchup
        for matchup in self.ability_type_modifiers:
            #create entry
            type_matchups[matchup] = {}
            #get the modifiers of the ability
            ability_modifiers = self.ability_type_modifiers[matchup]
            #for each type
            for type in self.matchup:
                #dummy value unless needed
                ability_modifier = 1
                #check if we have a modifier
                if type in ability_modifiers:
                    #set the ability modifier
                    ability_modifier = self.ability_type_modifiers[matchup][type]

                #calculate own modifiers
                total_modifier = self.matchup[type][0]
                
                #if multiple types
                if len(self.matchup[type]) > 1:
                    #also add the secondary typing
                    total_modifier *= self.matchup[type][1]
                
                #check for special calculations
                if matchup == "Wonder Guard":
                    #if not super effective
                    if total_modifier <= 1:
                        #set to 0
                        total_modifier = 0
                else:
                    #check for absorbtion
                    if ability_modifier == -1:
                        #set to absorb
                        total_modifier = -1
                    else:
                        #add the ability modifier (if changed)
                        total_modifier *= ability_modifier
                #save modifier
                type_matchups[matchup][type] = total_modifier
        
        #check duplicate entries
        combined_type_matchups = {}
        #for each raw matchup
        for type_matchup in type_matchups:
            #flag to check if we have found duplicate
            flag_found = False
            #get the value
            values = type_matchups[type_matchup]
            #for every saved entry
            for combined_type_matchup in combined_type_matchups:
                #if the values are the same
                if combined_type_matchups[combined_type_matchup] == values:
                    #indicate duplicate
                    flag_found = True
                    #create a new name
                    new_name = combined_type_matchup + ", " + type_matchup
                    #create a new entry
                    combined_type_matchups[new_name] = values
                    #remove the existing entry
                    del combined_type_matchups[combined_type_matchup]
                    #stop looking
                    break
            #if not found
            if flag_found == False:
                #just add it
                combined_type_matchups[type_matchup] = values
        
        #return the values
        return combined_type_matchups
    

    
    #function to determine the generation of the pokemon
    def determine_generation(self):
        #check form first, since this can give away the generation
        #forms for region
        regional_forms = {
            "Alolan":7,
            "Galarian":8,
            "Hisuian":8,
            "Paldean":9,
        }
        #get the form to check for alternate forms
        form = self.form
        if form in regional_forms:
            #return the generation of this form
            return regional_forms[form]
        
        #otherwise normal processing
        #get the number of the pokemon
        number = self.number
        #if it is an alternate form
        while not number[len(number)-1].isdigit():
            #remove the last character
            number = number[:-1]
        #convert to number
        number = int(number)

        generation = [
            1,#-151
            152,#-251
            252,#-386
            387,#-493
            494,#-649
            650,#-721
            722,#-809
            810,#-905
            906,#-1010
        ]
        #for each generation
        for gen in range(len(generation)):
            start_value_of_generation = generation[gen]
            #if lower than the current generation
            if number < start_value_of_generation:
                #return the index (which is 1 lower than the current generation)
                return gen
        #return the highest generation
        return len(generation)   



    #function that describes the pokemon
    def describe(self):

        #describe the name
        name = self.name
        #if it is a specific form
        if self.form != "":
            #add to name
            name += f" ({self.form})"
        #get the generation
        generation = self.determine_generation()
        
        #if we have a classification
        if self.classification != "":
            #print the number and name
            cprint(f"Pokemon #{self.number} (gen {generation}): {name} ({self.classification})", None, attrs=["bold", "underline"])
        else:
            #print the number and name
            cprint(f"Pokemon #{self.number} (gen {generation}): {name}", None, attrs=["bold", "underline"])

        #check evolutions
        #predecessors, successors, _ = get_evolutions(pokemon_obj)
        #check if we have ANY evolutions
        #if len(predecessors) > 0:
            #cprint(f"Evolves from: {", ".join(successors)}")
        #if len(successors) > 0:
            #cprint(f"Evolves to: {", ".join(successors)}")

        #print abilities
        cprint(f"Abilities:", None ,attrs=["underline"])#{", ".join(pokemon_obj.all_abilities)}")

        for ability in self.all_abilities:
            #get the ability description
            ability_description, error = self.get_ability(ability)
            #if error
            if error != None:
                #show the error instead of the description
                ability_description = error
            #if it is an hidden ability
            if ability in self.hidden_ability:
                #add the hidden ability description
                cprint(f"{ability} (Hidden-Ability): {ability_description}")
            else:
                #otherwise print normally
                cprint(f"{ability}: {ability_description}")
        
        #print the type
        cprint(f"Type: {", ".join(self.type)}", None, attrs=["underline"])

        #get the type match-up
        type_matchups = self.calculate_type_matchups()
        #convert for better reporting
        modifier_list = convert_type_matchups(type_matchups)
        #check if we need to create spacing
        if len(modifier_list) > 1:
            #empty line
            print("")

        #for each weakness
        for matchup in modifier_list:
            #if there are multiple configs
            if len(modifier_list) > 1:
                #print the ability for this config
                print(f"Modifiers with: {matchup}")
            #get the modifiers of this matchup
            modifiers = modifier_list[matchup]
            #for every modifier
            for entry in modifiers:
                #get the modifier
                modifier = entry[0]
                #get the types
                types = entry[1]
                
                if modifier > float(1): 
                    cprint(f"Super Effective ({modifier}): {", ".join(types)}", "green")
                elif modifier == float(0):
                    cprint(f"No effect ({modifier}): {", ".join(types)}", "red", attrs=["bold"])
                elif modifier < float(0):
                    cprint(f"Absorb ({modifier}): {", ".join(types)}", "red", attrs=["bold","underline"])
                elif modifier != float(1):
                    cprint(f"Not very effective ({modifier}): {", ".join(types)}", "red") 
                else:
                    print(f"Effective: ({modifier}): {", ".join(types)}")
            #empty line
            print("")

        #spacer
        print("------------------------------------------------------------")



#function that returns the evolutions
#predecessor(s), successor(s), error
#def get_evolutions(pokemon_obj):
    #get predecessors
    #predecessors_id = pokemon_obj.predecessors
    #predecessors_name = []
    #for id in predecessors_id:
        #get the pokemon
        #pokemon = get_pokemon(number=id)
        #save the name
        #predecessors_name.append(pokemon.name)
    #get successors
    #successors_id = pokemon_obj.successors
    #successors_name = []
    #for id in successors_id:
        #get the pokemon
        #pokemon = get_pokemon(number=id)
        #save the name
        #successors_name.append(pokemon.name)
    
    #return predecessors_name, successors_name, None



#function that converst type match to an list with scores which contains the typings instead of typings which contain their score 
def convert_type_matchups(type_matchups):
    #create list to print later
    type_matchups_modifiers = {}
    #group them, largest modifier first
    #for every possible ability which affects type
    for type_matchup in type_matchups:
        #create list
        modifiers = {}
        #get the types
        types = type_matchups[type_matchup]
        #for every type
        for type in types:
            #get the modifier
            modifier = types[type]
            #set to int if possible
            if modifier % 1 == 0:
                #convert to whole number (if a whole number)
                modifier = int(modifier)
            #check if entry exists
            if modifier not in modifiers:
                #create empty list
                modifiers[modifier] = []
            #add to list
            modifiers[modifier].append(type)
        #reverse sort (highest first)
        modifiers_sorted = sorted(modifiers.items(), key=operator.itemgetter(0), reverse=True)
        #add to total list
        type_matchups_modifiers[type_matchup] = modifiers_sorted    
    #return the modifiers
    return type_matchups_modifiers


