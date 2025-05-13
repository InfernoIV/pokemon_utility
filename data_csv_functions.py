#script functions that handles the data from the CSV file into usable functionalities
#to be used:
# get_pokemon (returns pokemon object)



#imports
import csv, sys
from termcolor import colored, cprint #https://pypi.org/project/termcolor/
from pokemon_obj import Pokemon



#constants
___CSV_POKEMON____ = "Data/pokemon.csv"



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
                    #create pokemon object
                    pokemon_object = Pokemon(row, "csv")
                    #add object to the list
                    matching_pokemon.append(pokemon_object)                                        
        #if exception
        except csv.Error as e:
            cprint("CSV error", "red")
            #print and exit
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    #return the list of matching pokemon
    return matching_pokemon 
