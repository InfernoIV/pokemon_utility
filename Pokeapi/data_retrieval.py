#imports
import requests
from termcolor import cprint #https://pypi.org/project/termcolor/
from pokemon_obj import Pokemon as pokemon_obj
from constants import ___BASE_URL___, ___ALLOWED_TYPES___



#function that gets pokemon information from https://pokeapi.co/
def get_pokemon(criteria):
    #get pokemon json data
    json_pokemon, error = get_JSON("pokemon", criteria)
    #if error
    if error != None:
        #stop
        return None, error
    #get the name
    name = json_pokemon["name"]

    #get species info
    species_url = json_pokemon["species"]["url"].split('/')
    species_name = species_url[len(species_url)-2]
    json_species, error = get_JSON("pokemon-species", species_name)
    #if error
    if error != None:
        #stop
        return None, error
    
    #check for evolution URL
    evolution_url = json_species["evolution_chain"]["url"]
    url_elements = evolution_url.split('/')
    evolution_chain_number = url_elements[len(url_elements)-2]
    #get evolution info
    json_evolutions, error = get_JSON("evolution-chain", evolution_chain_number)
    #if error
    if error != None:
        #stop
        return None, error
    
    #merge json
    json_pokemon = json_pokemon | json_species | json_evolutions
    #overwrite back the name
    json_pokemon["name"] = name
    #convert to object
    pokemon_api_obj = Pokemon(json_pokemon)
    #return the value
    return [pokemon_api_obj], None



#function that performs and http request and returns JSON
def get_JSON(type, criteria):
    #create URL
    url = ___BASE_URL___ + type + "/"
    #check if it is number
    if isinstance(criteria, int):
        url += f"{criteria}"
    else:
        url += criteria.lower()

    #perform a get message
    response = requests.get(url)
    #check if everything went well
    if response.ok == False:
        #print message
        print(f"Error with request, url: {url}, response: {response.status_code}")
        #return status code
        return None, response.status_code
    #convert JSON to object
    pokemon_json = response.json()#json.parse(result.text);
    #return the online data
    return pokemon_json, None



#function that gets the data of an ability
def get_ability_description(ability_name):
    #convert spaces to dash
    ability_name_converted = ability_name.replace(' ','-')
    #get the data
    json_ability, error = get_JSON("ability",ability_name_converted)
    #if error
    if error != None:
        #stop
        return None, error
    #for each data entry
    for effect_entry in json_ability["effect_entries"]:
        #only use the entry which is english
        if effect_entry["language"]["name"] == "en":
            #remove the extra lines
            effect_formatted = effect_entry["effect"].replace('\n', ' ').replace('\r', '')
            #copy this description
            effect = effect_formatted
            #return the effect
            return effect, None
    #ability not found, should not happen
    return None, LookupError(f"Ability '{ability_name}' not found!")
    



#pokemon object, containing information of the pokemon
class Pokemon(pokemon_obj):
    #get the ability description
    def get_ability(self, ability_name):
        #get and return the values
        return get_ability_description(ability_name)
        

    
    # The class "constructor" - It's actually an initializer 
    def __init__(self, json_obj):
        #get the components of the name
        full_name = json_obj["name"].capitalize().split('-')
        #the first component is the name
        self.name = full_name[0]
        #set default value for form
        self.form = ""
        #if we have a form component
        if len(full_name) > 1:
            #set the form name
            self.form = full_name[1]
        
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

        #classification
        self.classification = ""
        if json_obj["is_legendary"] == True:
            self.classification = "Legendary"
        elif json_obj["is_mythical"] == True:
            self.classification = "Mythical"

        #calculate other parameters
        self.get_ability_type_modifiers()
        self.get_type_matchup()
        

