#imports
from termcolor import cprint #https://pypi.org/project/termcolor/
import sys
from pokemon_obj import Pokemon
from constants import ___ALLOWED_TYPES___, ___CSV_TYPES___, ___CSV_TYPE_ABILITIES___



#pokemon object, containing information of the pokemon
class Pokemon_CSV(Pokemon):
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