#usage
#python3 main.py

#imports
import sys
#import own functions
from pokemon_functions import describe_pokemon, describe_pokemon_all, get_families



#main function
def main():
    #if not correct arguments
    if len(sys.argv) < 2:
        #print usage
        print_usage()

    #get information
    command = sys.argv[1].lower()
    #check what to do
    if command == "pokemon":
        #arg 3 = specific pokemon
        if len(sys.argv) < 3:
            print_usage()
        else:
            pokemon = sys.argv[2].lower()
            #if they want to have all pokemon
            if pokemon == "all":
                describe_pokemon_all()
            #searching for a specific pokemon
            else:
                describe_pokemon(pokemon)
    #get the pokemon families
    elif command == "families":
        get_families()
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
    print("pokemon <name/number> -> gets information of the pokemon, inputting 'all' gets information of all pokemon in the pokedex !!!")
    print("families -> gets information of the pokemon families")
    #stop
    sys.exit(1)
    #needed?
    return



#exectue main function
main()