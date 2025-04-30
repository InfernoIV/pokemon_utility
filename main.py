#python3 main.py

#imports
import sys
from pokemon_functions import describe_pokemon, get_families

#main function
def main():
    #if not correct arguments
    if len(sys.argv) < 2:
        print_usage()

    #get information
    command = sys.argv[1].lower()
    #check what to do
    if command == "pokemon":
        if len(sys.argv) < 3:
            print_usage()
        else:
            pokemon = sys.argv[2].lower()
            describe_pokemon(pokemon)

    elif command == "families":
        get_families()

    else:
        print_usage()
    return



#prints the usage of the program
def print_usage():
    #print help message
    print("Usage: python3 main.py <command>")
    print("pokemon <name or number> -> gets information of the pokemon")
    print("families -> gets information of the pokemon families")
    #stop
    sys.exit(1)
    #needed?
    return

#exectue main function
main()