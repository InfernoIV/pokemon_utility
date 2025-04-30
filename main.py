#python3 main.py

#imports
import sys
from pokemon_functions import describe_pokemon

#main function
def main():
    #if not correct arguments
    if len(sys.argv) != 2:
        #print help message
        print("Usage: python3 main.py <name or number>")
        #stop
        sys.exit(1)
        #needed?
        return
    
    #get information
    pokemon = sys.argv[1]
    describe_pokemon(pokemon)
    return

#exectue main function
main()