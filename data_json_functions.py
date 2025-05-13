#imports
import requests
from pokemon_obj import Pokemon



#global constants
__BASE_URL___ = "https://pokeapi.co/api/v2/"



#function that gets pokemon information from https://pokeapi.co/
def get_pokemon_from_api(pokemon_obj):
    #get pokemon json data
    pokemon_json, err = get_pokemon_JSON(pokemon_obj)
    #if error
    if err != None:
        #stop
        return
    #convert to object
    pokemon_api_obj = Pokemon(pokemon_json, "json")
    #return the value
    return pokemon_api_obj



#function that performs and http request and returns JSON
def get_pokemon_JSON(pokemon_obj):
    #create URL
    url = __BASE_URL___ + "pokemon/" + pokemon_obj.name.lower()
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
   