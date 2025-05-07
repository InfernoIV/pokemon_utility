#script functions that handles the data from the CSV file into usable functionalities



#imports
import csv, sys



#constants
___CSV_POKEMON____ = "Data/pokemon.csv"



#function that counts the row of a csv file
def get_amount_of_rows(csv_file):
     #use the csv as data source
    with open(csv_file) as csvfile: 
        #use a dict
        reader = csv.Reader(csvfile)
        #count the rows
        row_count = sum(1 for row in reader)  # fileObject is your csv.reader
    #return the row count
    return row_count




#function that gets the amount of lines in the csv file
def get_amount_of_pokemon():
    #get the amount of lines in the pokemon csv file
    return get_amount_of_rows(___CSV_POKEMON____)




#function that gets pokemon according to the filter
def get_pokemon(filter):
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
                    #convert the data to an object
                    pokemon_object = Pokemon(row)
                    #add object to the list
                    matching_pokemon.append(pokemon_object)                                        
        #if exception
        except csv.Error as e:
            #print and exit
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    #return the list of matching pokemon
    return matching_pokemon 



#pokemon object, containing information of the pokemon
class Pokemon(object):
    #properties
    number = -1
    name = ""
    form_name = ""
    form_type = ""
    type = []
    abilities = []
    hidden_ability = ""
    predecessors = []
    successors = []

    # The class "constructor" - It's actually an initializer 
    def __init__(self, dict):
        #print(f"dict: {dict}")
        self.number = -1
        self.name = ""
        self.form_name = ""
        self.classification = ""
        self.type = []
        self.abilities = []
        self.hidden_ability = ""
        self.predecessors = []
        self.successors = []

        #description
        #add number
        self.number = dict["number"]
        #add name
        self.name = dict["name"]
        #add form name (for description)
        self.form_name = dict["form"]
        #add classification
        self.classification = dict["classification"]

        #typing
        #always add type 1
        self.type.append(dict["type-1"])        
        #if it has a secondary type
        if dict["type-2"] != "":
            #add it
            self.type.append(dict["type-2"])

        #ability-1,ability-2,ability-hidden
        #abilities
        #always add ability 1
        self.abilities.append(dict["ability-1"])
        #if it has a secondary ability
        if dict["ability-2"] != "":
            #add it
            self.abilities.append(dict["ability-2"])
        #if it has a hidden ability
        if dict["ability-hidden"] != "":
            self.hidden_ability = dict["ability-hidden"]

        #predecessors,successors
        #Evolutions
        #if it has previous evolutions
        if dict["predecessors"] != "": 
            #save them
            self.predecessors = dict["predecessors"].split(",")
        #if it has next evolutions
        if dict["successors"] != "": 
            #save them
            self.successors = dict["successors"].split(",")
    
    def __repr__(self):
        return f"number: '{self.number}', name: '{self.name}', form_name: '{self.form_name}', form_type: '{self.form_type}', type: '{self.type}', abilities: '{self.abilities}', hidden_ability: '{self.hidden_ability}', predecessors: '{self.predecessors}', successors: '{self.successors}'"