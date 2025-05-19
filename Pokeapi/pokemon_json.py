#imports
from termcolor import cprint #https://pypi.org/project/termcolor/
from pokemon_obj import Pokemon

#constants
___ALLOWED_TYPES___ = ["Normal","Fire","Water","Grass","Electric","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy"]



#pokemon object, containing information of the pokemon
class Pokemon_JSON(Pokemon):
    # The class "constructor" - It's actually an initializer 
    def __init__(self, json_obj):
        self.name = json_obj["name"].capitalize()
        self.number = str(json_obj["order"])
        #set properties
        self.all_abilities = []
        self.abilities = []
        self.hidden_ability = ""
        #for each ability
        for ability in json_obj["abilities"]:
            #get the desired properties
            ability_name = ability["ability"]["name"].capitalize()
            ability_is_hidden = ability["is_hidden"]
            #add to ability list
            self.all_abilities.append(ability_name)
            #check if hidden
            if ability_is_hidden == True:
                #set as hidden ability
                self.hidden_ability = ability_name
            else:
                #add as normal abilities
                self.abilities.append(ability_name)
        
        #types
        self.type = []
        #get types
        for type in json_obj["types"]:
            #get the typing
            typing = type["type"]["name"].capitalize()
            #add type to list
            self.type.append(typing)
        
        #evolutions
        self.predecessors = []
        self.successors = []
        

        #todo
        self.form_name = ""

        #calculate other parameters
        self.get_ability_type_modifiers()
        self.get_type_matchup()
        


