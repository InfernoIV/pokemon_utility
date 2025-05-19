#imports
import requests
from Pokeapi.pokemon_json import Pokemon_JSON as Pokemon
from constants import __BASE_URL___

#global constants




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
    #number = json_pokemon["id"]

    #get species info
    json_species, error = get_JSON("pokemon-species", name)
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
    #convert to object
    pokemon_api_obj = Pokemon(json_pokemon)
    #return the value
    return [pokemon_api_obj], None



#function that performs and http request and returns JSON
def get_JSON(type, name):
    #create URL
    url = __BASE_URL___ + type + "/" + name.lower()
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
def get_ability_data(ability_name):
    #convert spaces to dash
    ability_name_converted = ability_name.replace(' ','-')
    #get the data
    json_ability, err = get_JSON("ability",ability_name_converted)
    #if error
    if err != None:
        #stop
        return
    #create ability
    ability = Ability(ability_name, json_ability)
    return ability



#pokemon object, containing information of the pokemon
class Ability(object):
    # The class "constructor" - It's actually an initializer 
    def __init__(self, ability_name, data):#, data_type="json"):
        #if data is dict
        #if data_type == "csv":
            #use csv init
            #self.init_csv(ability_name, data)
        #elif data_type == "json":
            #use json init
        self.init_json(ability_name, data)
    
    def init_json(self, ability_name, data):
        #set name
        self.name = ability_name
        #for each entry
        for effect_entry in data["effect_entries"]:
            #only use the entry which is english
            if effect_entry["language"]["name"] == "en":
                #remove the extra lines
                effect_formatted = effect_entry["effect"].replace('\n', ' ').replace('\r', '')
                #copy this description
                self.effect = effect_formatted

        #copy the pokemon list
        self.pokemon = []
        #
        for pokemon in data["pokemon"]:
            self.pokemon.append(pokemon["pokemon"]["name"])
            

        #debug
        #print(f"ability: {str(self)}")

    
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
