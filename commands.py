from constants import ___OPERATING_MODE_LOCAL___, ___OPERATING_MODE_ONLINE___
from Local.data_lookup import get_pokemon as get_pokemon_local
from Pokeapi.data_retrieval import get_pokemon as get_pokemon_online



#function that looks up a pokemon
def lookup_pokemon(arguments, operating_mode):
    #guard clauses
    #check if there is an argument
    if len(arguments) == 0:
        #return error
        return SyntaxError(f"Not enough arguments: {len(arguments)} / 1")
    #check if not too many errors
    elif len(arguments) > 1:
        #return error
        return SyntaxError(f"Too many arguments: {len(arguments)} / 1")
    #check config
    elif operating_mode != ___OPERATING_MODE_LOCAL___ and  operating_mode != ___OPERATING_MODE_ONLINE___:
        #return error
        return ValueError(f"Incorrect operating_mode config: {operating_mode} ")

    #get the key
    criteria = arguments[0]
    #placeholders
    number = ""
    name = ""
    #if it is a number
    if criteria[0].isdigit():
        #set the number
        number = criteria
    #if it is text
    else:
        #set the name
        name = criteria
    
    #if looking locally
    if operating_mode == ___OPERATING_MODE_LOCAL___:
        #get the pokemon(s)
        pokemon_list, error = get_pokemon_local(number=number, name=name)
    #if looking online
    elif operating_mode == ___OPERATING_MODE_ONLINE___:
        #get the pokemon(s)
        pokemon_list, error = get_pokemon_online(criteria)

    #if error
    if error != None:
        return error
    #if no pokemon found
    elif len(pokemon_list) == 0:
        #return error
        return "No pokemon found!"
    else:
        #for each pokemon found
        for pokemon in pokemon_list:
            #describe the pokemon
            pokemon.describe()
    
    #return
    return None
        

