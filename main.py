#imports
import sys
from data_csv_functions import get_pokemon
from data_processing import describe_pokemon, describe_pokemon_from_api



#main function
def main():
    #if not correct arguments
    if len(sys.argv) < 2:
        #print usage
        print_usage()    

    #placeholder
    pokemon_list = []
        
    #get information
    command = sys.argv[1].lower()
    #check what to do
    if command == "pokemon":
        #arg 3 = specific pokemon
        if len(sys.argv) < 3:
            #not enough arguments
            print_usage()
        #enough arguments
        else:
            #get the criteria
            criteria = sys.argv[2].lower()
            #dummy for form
            form = ""
            #if we have a form argument
            if len(sys.argv) == 4:
                    #update it
                form = sys.argv[3].lower()

            #if they want to have all pokemon
            if criteria == "all":
                #get all pokemon
                pokemon_list = get_pokemon(name="", form=form)
            #if it is number based
            elif criteria[0].isdigit():
                #get all pokemon with this number
                pokemon_list = get_pokemon(number=criteria, form=form)
            #otherwise searching by name 
            else:
                #get all pokemon with this number
                pokemon_list = get_pokemon(name=criteria, form=form)
                #for each pokemon found
            for entry in pokemon_list:
                #describe the pokemon
                describe_pokemon_from_api(entry)
                #describe_pokemon(entry)

            

    #looking for legendary or mythical pokemon
    elif command == "class":
        #arg 3 = specific form
        if len(sys.argv) < 3:
            #not enough arguments
            print_usage()
        #enough arguments
        else:
            #get the criteria
            criteria = sys.argv[2].lower()
            #placeholder
            pokemon_list = []
            #get all pokemon with this classification
            pokemon_list = get_pokemon(classification=criteria)
            #for each pokemon found
            for entry in pokemon_list:
                #describe the pokemon
                describe_pokemon(entry)
    
        

    #not a valid command
    else:
        #print usage
        print_usage()
    #stop function
    return



#prints the usage of the program
def print_usage():
    #print help message
    print("Usage: python3 main.py <command>")
    print("\tpokemon <name/number> -> gets information of the pokemon, inputting 'all' gets information of all pokemon!!!")
    print("\tpokemon <name/number> <forme> -> gets information of the pokemon of this specific form (if exists)")
    print("\tclass <classification> -> gets information of either legendary or mythical pokemon")
    #print("\tfamilies -> gets information of the pokemon families")
    #print("\ttype <type> -> gets information of pokemon that has this specific type. 1 types")
    #print("\ttype <type><type> -> gets information of pokemon with specific typing combination. 2 types")
    #print("\tability <ability> -> gets information of pokemon which can have this specific ability")
    #stop
    sys.exit(1)
    #needed?
    return



#exectue main function
main()