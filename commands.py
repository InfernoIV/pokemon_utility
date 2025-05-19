from constants import ___OPERATING_MODE_LOCAL___, ___OPERATING_MODE_ONLINE___
from Local.data_lookup import get_pokemon as get_pokemon_local
from Pokeapi.data_retrieval import get_pokemon as get_pokemon_online



#function that looks up a pokemon
def lookup_pokemon(arguments, operating_mode):
    #guard clauses
    #check if there is an argument
    if len(arguments) == 0:
        #return error
        return SyntaxError(f"Not enough arguments: {len(arguments)}, min 1")
    #check if not too many errors
    elif len(arguments) > 2:
        #return error
        return SyntaxError(f"Too many arguments: {len(arguments)}, max 2")

    #get the key
    criteria = arguments[0].lower()
    #placeholders
    number = ""
    name = ""
    form = ""
    
    #if there is a form argument
    if len(arguments) > 1:
        #get the form
        form = arguments[1].lower()

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
        pokemon_list, error = get_pokemon_local(number=number, name=name, form=form)
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
        


#function that looks up pokemon form
def lookup_pokemon_form(arguments, operating_mode):
 #guard clauses
    #check if there is an argument
    if len(arguments) == 0:
        #return error
        return SyntaxError(f"Not enough arguments: {len(arguments)}, min 1")
    #check if not too many errors
    elif len(arguments) > 2:
        #return error
        return SyntaxError(f"Too many arguments: {len(arguments)}, max 1")
    
    #get the key
    criteria = arguments[0].lower()
     #if looking locally
    if operating_mode == ___OPERATING_MODE_LOCAL___:
        #get the pokemon(s)
        pokemon_list, error = get_pokemon_local(form=criteria)
    #if looking online
    elif operating_mode == ___OPERATING_MODE_ONLINE___:
        #get the pokemon(s)
        #pokemon_list, error = get_pokemon_online(criteria)
        pass

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




#function that looks up a pokemon
def lookup_pokemon_classification(arguments, operating_mode):
    #guard clauses
    #check if there is an argument
    if len(arguments) == 0:
        #return error
        return SyntaxError(f"Not enough arguments: {len(arguments)}, min 1")
    #check if not too many errors
    elif len(arguments) > 2:
        #return error
        return SyntaxError(f"Too many arguments: {len(arguments)}, max 1")
    
    #get the key
    criteria = arguments[0].lower()
     #if looking locally
    if operating_mode == ___OPERATING_MODE_LOCAL___:
        #get the pokemon(s)
        pokemon_list, error = get_pokemon_local(classification=criteria)
    #if looking online
    elif operating_mode == ___OPERATING_MODE_ONLINE___:
        #get the pokemon(s)
        #pokemon_list, error = get_pokemon_online(criteria)
        pass

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