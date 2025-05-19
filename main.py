#imports
import sys
from commands import lookup_pokemon
from config import get_operating_mode, set_operating_mode



#main function
def main():
    #get operating mode    
    operating_mode = get_operating_mode()

    #if not correct arguments
    if len(sys.argv) < 2:
        #print usage
        print_usage()   

    else:
        #get information
        command = sys.argv[1].lower()
        arguments = sys.argv[2:len(sys.argv)]
        #if mode change
        if command == "mode":
            #change the operating mode
            error = set_operating_mode(arguments)

        #if looking for specific pokemon
        elif command == "pokemon":
            #lookup the pokemon(s)
            error = lookup_pokemon(arguments, operating_mode)
            
        elif command == "form":
            #error = lookup_pokemon_form(arguments)
            pass
        elif command == "class":
            #error = lookup_pokemon_class(arguments)
            pass
        #not a valid command
        else:
            #print usage
            print_usage()

        #check for errors
        if error != None:
            #print the error
            print(f"Error: {error}")
            #print usage
            print_usage()

    #stop function
    return



#prints the usage of the program
def print_usage():
    #print help message
    print("Usage: python3 main.py <command>")
    print("\tpokemon <name/number> -> gets information of the pokemon, inputting 'all' gets information of all pokemon!!!")
    print("\tmode local/online -> sets the information to local database or pokeapi respectively")
    #print("\tpokemon <name/number> <forme> -> gets information of the pokemon of this specific form (if exists)")
    #print("\tclass <classification> -> gets information of either legendary or mythical pokemon")
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