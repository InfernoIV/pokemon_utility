#script functions that handles the data from the CSV file into usable functionalities
#to be used:
# get_pokemon (returns pokemon object)



#imports
import csv, sys, operator
from termcolor import colored, cprint #https://pypi.org/project/termcolor/



#constants
___CSV_POKEMON____ = "Data/pokemon.csv"
___CSV_TYPES___ = "Data/types.csv"
___CSV_TYPE_ABILITIES___ = "Data/type_ability.csv"
___ALLOWED_TYPES___ = ["Normal","Fire","Water","Grass","Electric","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy"]

#function that creates a filter and then retrieves the matching pokemon
def get_pokemon(**kwargs): 
    #create the filter
    filter = create_filter(kwargs)
    #get the pokemon(s)
    pokemon_list = lookup_pokemon(filter)
    #return the pokemon
    return pokemon_list



#function that creates the filter
def create_filter(kwargs):
    #create local object to keep track of the filters
    filter = { 
        "number": "", #number of the pokemon (can be specfic but also be "generic" in case of regional forms) (number)
        "name": "", #name of the pokemon (name)
        "form": "", #searching for a specific form (form)
        "classification": "", #classification for legendary or mythical (classification)
        "type": "", #specific type (type-1 or type-2)
        "types": "", #specific type combination (type-1,type-2 or type-2,type-1)
        "ability": "", #specific ability (ability-1,ability-2,ability-hidden)
    }

    #for each key that we accept
    for key in filter:
        #if it is described
        if key in kwargs:
            #copy it
            filter[key] = kwargs[key]
    #remove empty keys
    empty_keys = []
    for key in filter:
        #if it is empty
        if filter[key] == "":
            #add it to the list
            empty_keys.append(key)
    #for each empty filter
    for key in empty_keys:
        #delete it
        del filter[key]
    #return the filter
    return filter



#function that gets pokemon according to the filter
def lookup_pokemon(filter):
    #list to hold the matching pokemon
    matching_pokemon = []
    #used multiple times
    filename = ___CSV_POKEMON____
    #use the csv as data source
    with open(filename) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                #set a flag
                flag_matching = True
                #for each check
                for check in filter:
                    #if not matching the value in the row
                    if filter[check].lower() not in row[check].lower():
                        #set flag to false
                        flag_matching = False
                        #stop
                        break
                #check if matching
                if flag_matching == True:
                    #convert the data to an object
                    pokemon_object = Pokemon(row)
                    #add object to the list
                    matching_pokemon.append(pokemon_object)                                        
        #if exception
        except csv.Error as e:
            cprint("CSV error", "red")
            #print and exit
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    #return the list of matching pokemon
    return matching_pokemon 



#pokemon object, containing information of the pokemon
class Pokemon(object):
    # The class "constructor" - It's actually an initializer 
    def __init__(self, dict):
        
        #guard clauses
        #check the number
        if dict["number"] == "":
            #missing number
            cprint("Missing number of the following pokemon:", "red")
            #stop
            sys.exit(f"dict: {dict}")   
        #check the name
        if dict["name"] == "":
            #missing name
            cprint("Missing name of the following pokemon:", "red")
            #stop
            sys.exit(f"dict: {dict}")   
        #check the typing
        if dict["type-1"] == "":
            #missing data
            cprint("Missing type of the following pokemon:", "red")
            #stop
            sys.exit(f"dict: {dict}")    
        #check the typing
        if dict["type-1"] not in ___ALLOWED_TYPES___:
            #missing data
            cprint("Incorrect type of the following pokemon:", "red")
            #stop
            sys.exit(f"dict: {dict}")        
            
        
        #description
        #add number
        self.number = dict["number"]
        #add name
        self.name = dict["name"]
        #add form name (for description)
        self.form_name = dict["form"]
        #add classification
        self.classification = dict["classification"]

        #typing
        #always add type 1
        self.type = [dict["type-1"]]
        #if it has a secondary type
        if dict["type-2"] != "":
            #add it
            self.type.append(dict["type-2"])

        #get the type matchup
        self.get_type_matchup()

        #ability-1,ability-2,ability-hidden
        #abilities
        #always add ability 1
        self.abilities = [dict["ability-1"]]
        #if it has a secondary ability
        if dict["ability-2"] != "":
            #add it
            self.abilities.append(dict["ability-2"])
        #copy the current list to all abilities
        self.all_abilities = self.abilities.copy()
        
        #save the hidden ability
        self.hidden_ability = dict["ability-hidden"]
        #if it has a hidden ability
        if dict["ability-hidden"] != "":
            #add to the ability list
            self.all_abilities.append(self.hidden_ability)
        
        #get the typing of specific abilities
        self.get_ability_type_modifiers()

        #predecessors,successors
        #Evolutions
        self.predecessors = []
        self.successors = []
        #if it has previous evolutions
        if dict["predecessors"] != "": 
            #save them
            self.predecessors = dict["predecessors"].split(",")
        #if it has next evolutions
        if dict["successors"] != "": 
            #save them
            self.successors = dict["successors"].split(",")

    

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
