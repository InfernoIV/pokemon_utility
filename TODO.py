#file with functions to be refactored

#function to get all pokemon families
def get_families():
    numbers_processed = []
    families = []
    print("Pokemon families:")
    for index in range(1, ___NUMBER_OF_POKEMON___):
        #convert to string for lookup
        index = str(index)
        #if not already processed
        if index not in numbers_processed:
            #get the evolution line
            evolution_tree, evolution_numbers = get_evolution_line(index)
            #print the evolution line
            print(f"{", ".join(evolution_tree)}")
            #families.append(evolution_tree)
            numbers_processed = numbers_processed + evolution_numbers

#describe all pokemon
def describe_pokemon_all():
    #used multiple times
    filename = ___CSV_POKEMON____
    #use the csv as data source
    with open(filename) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                    #convert the data to an object
                    pokemon_object = Pokemon(row)
                    #describe the pokemon
                    describe_pokemon(pokemon_object)               
        #if exception
        except csv.Error as e:
            #print and exit
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))



#function to get the whole evolution line
def get_evolution_line(input):
    #print(f"get_evolutions: {input}")
    #variable to fill and return
    evolution_tree = []
    evolution_numbers = []
    #get the base pokemon
    base_pokemon, error = get_base_pokemon(input)
    #check for errors
    if error is not None:
        print(f"get_evolution_line: {error}")
    else:
        #print(f"Start get_evolutions: get_base_pokemon('{input}')")
        #get the evolution tree
        get_evolutions(base_pokemon, evolution_tree, evolution_numbers)
    #return data
    return evolution_tree, evolution_numbers



#[names, numbers], error
def get_evolutions(pokemon_object, evolution_tree, evolution_numbers):
    #guard clause, check object
    if not hasattr(pokemon_object, 'name'):
        print(f"Pokemon object")

    #determine the name of the pokemon
    name = pokemon_object.name
    #if it is a specific form:
    if pokemon_object.form_name != "":
        name += " (" + pokemon_object.form_name + ")"
    #add information of the current pokemon
    evolution_tree.append(name)
    evolution_numbers.append(pokemon_object.number)
    #for each successor
    for evolution in pokemon_object.successors:
        #get object
        successor, error = get_pokemon_data(evolution)
        #if error occurred
        if error is not None:
            #print error
            print(f"get_evolutions: {error}")
        else:
            #go deeper
            get_evolutions(successor, evolution_tree, evolution_numbers)
    return



#get the lowest level pokemon
def get_base_pokemon(pokemon_id):
    #get data of the pokemon
    pokemon, error = get_pokemon_data(pokemon_id)
    #check for errors
    if error is not None:
        #return the error
        return None, f"get_base_pokemon: Pokemon not found! {error}"
    else:
        #get to the lowest evolution
        #if there is a predecessor
        while len(pokemon.predecessors) > 0:
            #get the (first) predecessor
            pokemon, error = get_pokemon_data(pokemon.predecessors[0])
            #if error
            if error is not None:
                #return the error
                return None, f"get_base_pokemon(inner): Pokemon not found! {error}" 
        #return this pokemon
        return pokemon, None
    
    



    


def describe_pokemon_form(form):
    #get the numbers of the forms
    pokemon_form_list, error = get_pokemon_form_data(form)
    #check if success
    if error is not None:
        #print error
        print(error)
        #stop
        return
    
    #print(f"pokemon_form_list: {pokemon_form_list}")
    #for every pokemon
    for number in pokemon_form_list:
        #print(f"describe_pokemon_form: number: {number}")
        #get pokemon number
        pokemon_number = str(number)
        #describe the pokemon
        describe_pokemon(pokemon_number)



def get_pokemon_form_data(input_raw):
    #create a list of pokemon to return (list of pokemon numbers)
    form_list = []
    #sanatize
    input_sanatized = str(input_raw).lower()
    #set to number
    dict_keys = "form"
    #used multiple times
    filename = ___CSV_POKEMON____
    #use the csv as data source
    with open(filename) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                if (input_sanatized == "all" and row[dict_keys] != "") or (input_sanatized in row[dict_keys].lower()):
                    #convert the data to an object
                    pokemon_object = Pokemon(row)
                    #only add the number
                    form_list.append(pokemon_object.number)                    
        #if exception
        except csv.Error as e:
            #print and exit
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    #return the object
    return form_list, None 







