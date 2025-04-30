#imports
import csv, sys



#Return data, according to input
#either number or name
def get_pokemon_data(input_raw):
    #sanatize
    input_sanatized = str(input_raw).lower()

    #set to number
    dict_keys = "name"
    #check if name input
    if input_sanatized.isdigit():
        dict_keys = "number"
    #debug
    #print(f"get_pokemon_data '{dict_keys}' '{input_sanatized}'")
    #used multiple times
    filename = 'pokemon.csv'
    #use the csv as data source
    with open(filename) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                #if it matches what we are looking for
                if row[dict_keys].lower() == input_sanatized:
                    #convert the data to an object
                    pokemon_object = pokemon(row)
                    #return the object
                    return pokemon_object, None 
        #if exception
        except csv.Error as e:
            #print and exit
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    #default return value
    return None, f"Pokemon '{input_sanatized}' not found! ({input_raw})"



#function the print information to the console
def describe_pokemon(input):
    #get data of the pokemon
    pokemon, error = get_pokemon_data(input)
    #check if success
    if error is not None:
        #print error
        print(error)
        #stop
        return
    
    #print report
    print(f"Pokemon #{pokemon.number}: {pokemon.name}")
    print(f"Type: {", ".join(pokemon.type)}")
    ability_string = "Abilities: "
    if pokemon.abilities[1] == "":
        ability_string += f"{"".join(pokemon.abilities)}"
    else: 
        ability_string += f"{", ".join(pokemon.abilities)}"
    
    if pokemon.hidden_ability != "": 
        ability_string += f" ({pokemon.hidden_ability})"
    print(ability_string)

    #if there are predecessors
    if len(pokemon.predecessors) > 0:
        predecessor_list = []
        #for each number in the predecssor lsit
        for predecessor in pokemon.predecessors:
            #get the data
            predecessor_data, error = get_pokemon_data(predecessor)
            if error is None:
                predecessor_list.append(predecessor_data.name)
        #print information
        print(f"Evolves from {", ".join(predecessor_list)}")
    
    #if there are successors
    if len(pokemon.successors) > 0:
        #create a list
        successor_list = []
        #for each number in the predecssor lsit
        for successor in pokemon.successors:
            #get the data
            successors_data, error = get_pokemon_data(successor)
            if error is None:
                successor_list.append(successors_data.name)
        #print information
        print(f"Evolves to {", ".join(successor_list)}")



#pokemon object, containing information of the pokemon
class pokemon(object):
    number = -1
    name = ""
    form = ""
    type = []
    abilities = []
    hidden_ability = ""
    predecessors = []
    successors = []

    # The class "constructor" - It's actually an initializer 
    def __init__(self, dict):
        self.number = dict["number"]
        self.name = dict["name"]
        self.form = dict["form"]
        self.type = dict["type"].split(",")

        abilities = dict["abilities"].split(",")
        self.abilities = [abilities[0], abilities[1]]
        self.hidden_ability = abilities[2]

        predecessors_list = dict["predecessors"].split(",")
        if predecessors_list[0] != '': 
            self.predecessors = predecessors_list

        successors_list = dict["successors"].split(",")
        if successors_list[0] != '': 
            self.successors = successors_list

