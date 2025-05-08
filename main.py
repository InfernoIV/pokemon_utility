#usage
#python3 main.py pokemon haunter
#python3 main.py pokemon pikachu
#python3 main.py pokemon all
#python3 main.py form alolan
#python3 main.py class legendary
#python3 main.py class mythical



#imports
import sys
from data_processing import describe_pokemon
from data_conversion import get_pokemon



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
            
            #if they want to have all pokemon
            if criteria == "all":
                #get all pokemon
                pokemon_list = get_pokemon(name="")
            #if it is number based
            elif criteria[0].isdigit():
                #get all pokemon with this number
                pokemon_list = get_pokemon(number=criteria)
            #otherwise searching by name 
            else:
                #get all pokemon with this number
                pokemon_list = get_pokemon(name=criteria)
                #for each pokemon found
            for entry in pokemon_list:
                #describe the pokemon
                describe_pokemon(entry)
                
    #looking for specific forms
    elif command == "form":
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
            #if they want to have all pokemon
            #TODO: how to get all alt formes?
            #if criteria == "all":
                #get all pokemon
                #pokemon_list = get_pokemon_data(form="")
            #otherwise searching by name 
            #else:
                #get all pokemon with this number
            pokemon_list = get_pokemon(form=criteria)
            #for each pokemon found
            for entry in pokemon_list:
                #describe the pokemon
                describe_pokemon(entry)

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
    print("\tform <text> -> gets information of all pokemon with this text in their form description (alolan, galarian, hisuian, paldean)")
    print("\tclass <classification> -> gets information of either legendary or mythical pokemon")
    #print("\tfamilies -> gets information of the pokemon families")
    
    #stop
    sys.exit(1)
    #needed?
    return



#exectue main function
main()