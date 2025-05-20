#imports
import sys
from commands import lookup_pokemon, lookup_pokemon_form, lookup_pokemon_classification
from config import get_operating_mode, set_operating_mode, repair_config



#main function
def main():
    #check for config
    repair_config()

    #handle the program
    error = handle_program(sys.argv)
    #if there is an error
    if error != None:
        #print the error
        print(f"Error: {error}")
        #print usage
        print_usage()
    #stop function
    return



#function that handles the program, returns if there is an error
def handle_program(arguments): 
    #check and convert the input
    command, arguments, error = process_input(arguments)
    if error != None:
        return error

    #check the config
    #get operating mode    
    operating_mode, error = get_operating_mode()
    #if there an error
    if error != None:
        return error
    #print the mode the program is working in
    print(f"Operating mode: {operating_mode}")

    #if mode change
    if command == "mode":
        #change the operating mode
        return set_operating_mode(arguments)
    
    #if looking for specific pokemon
    elif command == "pokemon":
        #lookup the pokemon(s)
        return lookup_pokemon(arguments, operating_mode)
        
    #if looking for a specific form
    elif command == "form":
        return lookup_pokemon_form(arguments, operating_mode)
    
    #if looking for a specific class
    elif command == "class":
        return lookup_pokemon_classification(arguments, operating_mode)
        

    #not a valid command
    return SyntaxError("Not a vaild command")



#function that checks the input arguments
def process_input(arguments):
    #check if there are arguments
    if len(arguments) < 2:
        #set error
        return None, None, SyntaxError("No arguments")
    else:
        #get the command
        command = sys.argv[1].lower()
        #get the arguments
        arguments = sys.argv[2:len(sys.argv)]
        #return all
        return command, arguments, None



#prints the usage of the program
def print_usage():
    #print help message
    print("Usage: python3 main.py <command> <arguments>")
    print("\tpokemon <name/number> -> gets information of the pokemon, inputting 'all' gets information of all pokemon!!!")
    print("\tpokemon <name/number> <form> -> gets information of the pokemon with specific form, inputting 'all' gets information of all pokemon!!!")
    print("\tmode 'local' or 'online' -> sets the information to local database or pokeapi respectively")
    print("\tform <forme name> -> gets information of the pokemon of this specific form (if exists)")
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