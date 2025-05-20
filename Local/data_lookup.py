#script functions that handles the data from the CSV file into usable functionalities
#to be used:
# get_pokemon (returns pokemon object)



#imports
import csv, sys
from pokemon_obj import Pokemon as pokemon_obj
from constants import ___CSV_POKEMON____, ___CSV_ABILITIES____, ___ALLOWED_TYPES___, ___CSV_TYPES___, ___CSV_TYPE_ABILITIES___
from termcolor import cprint #https://pypi.org/project/termcolor/ 



#function that creates a filter and then retrieves the matching pokemon
def get_pokemon(**kwargs): 
    #create the filter
    filter = create_filter(kwargs)
    #get the pokemon(s)
    pokemon_list, error = lookup_pokemon(filter)
    #return the pokemon
    return pokemon_list, error



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
#returns pokemon_list, error
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
                    #create pokemon object
                    pokemon_object = Pokemon(row)
                    #add object to the list
                    matching_pokemon.append(pokemon_object)                                        
        #if exception
        except csv.Error as e:
            #return the error
            return None, 'file {}, line {}: {}'.format(filename, reader.line_num, e)
    #return the list of matching pokemon
    return matching_pokemon, None 



#Function that will retrieve the description of the ability
def lookup_ability(ability_name):
    #used multiple times
    filename = ___CSV_ABILITIES____
    #dummy value
    description = ""
    #use the csv as data source
    with open(filename) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                #only exact matches
                if row["ability"] == ability_name:
                    #get the description
                    description = row["description"]                                       
                    #return the description
                    return description, None 
        #if exception
        except csv.Error as e:
            #return the error
            return None, 'file {}, line {}: {}'.format(filename, reader.line_num, e)
    #return the list of matching pokemon
    return None, LookupError(f"Ability '{ability_name}' not found!")



#pokemon object, containing information of the pokemon
class Pokemon(pokemon_obj):
    #get the ability description
    def get_ability(self, ability_name):
        #get and return the values
        return lookup_ability(ability_name)

        
    
    # The class "constructor" - It's actually an initializer 
    def __init__(self, dict):
        #guard clauses
        flag_guarded = False
        #check the number
        if dict["number"] == "":
            #set flag
            flag_guarded = True 
            #missing number
            cprint("Missing number of the following pokemon:", "red")
        #check the name
        if dict["name"] == "":
            #set flag
            flag_guarded = True
            #missing name
            cprint("Missing name of the following pokemon:", "red")  
        #check the typing
        if dict["type-1"] == "":
            #set flag
            flag_guarded = True
            #missing data
            cprint("Missing type of the following pokemon:", "red")
        #check the typing
        elif dict["type-1"] not in ___ALLOWED_TYPES___:
            #set flag
            flag_guarded = True
            #missing data
            cprint("Incorrect type of the following pokemon:", "red")
        #check the typing
        if dict["ability-1"] == "":
            #set flag
            flag_guarded = True
            #missing data
            cprint("Missing ability of the following pokemon:", "red")
                  
        #if there is a guard
        if flag_guarded == True:
            #stop the script
            sys.exit(f"dict: {dict}")  

        #data is correct, start conversion to object 
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
        if dict["predecessors"] != "" and dict["predecessors"] != None: 
            #save them
            self.predecessors = dict["predecessors"].split(",")
        #if it has next evolutions
        if dict["successors"] != "" and dict["successors"] != None: 
            #save them
            self.successors = dict["successors"].split(",")

        #calculate other parameters
        self.get_ability_type_modifiers()
        self.get_type_matchup()