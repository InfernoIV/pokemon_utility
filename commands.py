from constants import ___OPERATING_MODE_LOCAL___, ___OPERATING_MODE_ONLINE___, ___TOTAL_NUMBER_OF_POKEMON___
from Local.data_lookup import get_pokemon as get_pokemon_local
from Pokeapi.data_retrieval import get_pokemon as get_pokemon_online
from config import get_retrieval_limit


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
    
    #check if we need to get all
    if criteria == "all":
         #if looking locally
        if operating_mode == ___OPERATING_MODE_LOCAL___:
            #get the pokemon(s)
            pokemon_list, error = get_pokemon_local() #does this work without filter?
        #if looking online
        elif operating_mode == ___OPERATING_MODE_ONLINE___:
            #create a list to fill
            pokemon_list = []
            #get the lowest value
            lookup_range = min(___TOTAL_NUMBER_OF_POKEMON___, get_retrieval_limit())
            print(f"lookup_range: {lookup_range}")
            
            #for a range
            for index in range(lookup_range):
                #correct the index
                corrected_index = index+1
                #get the pokemon(s) (index + 1 to start at 1 and end at the range we provided)
                pokemon, error = get_pokemon_online(corrected_index)
                #debug
                #print(f"corrected_index: {corrected_index}, found: {len(pokemon)}")
                #if error
                if error != None:
                    #break out of the loop
                    break
                #add to the list
                pokemon_list.extend(pokemon)

    #otherwise use specific filters
    else: 
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

    #process results
    #if error
    if error != None:
        return error
    #if no pokemon found
    elif len(pokemon_list) == 0:
        #return error
        return "No pokemon found!"
    else:
        #debug
        print(f"Found {len(pokemon_list)} pokemon")
        #for each pokemon found
        for pokemon_entry in pokemon_list:
            #describe the pokemon
            #pokemon_entry.describe()
            pass
        
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