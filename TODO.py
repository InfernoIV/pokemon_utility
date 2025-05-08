#file with functions to be refactored



#function that gets the amount of lines in the csv file
def get_amount_of_pokemon():
    #get the amount of lines in the pokemon csv file
    return get_amount_of_rows(___CSV_POKEMON____)



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







#assuming object pokemon_obj
def determine_type_matchups(pokemon_obj):
    #keep track of scores
    score = {}

    #get the type modifiers from the abilities
    ability_type_modifiers = get_ability_type_modifiers(pokemon_obj)
    
    #get the list of all abilities, except the abilities that affect the typing matchup
    ability_list = []
    print(f"ability_type_modifiers: {ability_type_modifiers}, ability_list: {ability_list}")
    #for each ability (should be either 1 ability or 2)
    for ability in pokemon_obj.abilities:
        #if not in the modifier list
        if ability not in ability_type_modifiers:
            #add to ability list
            ability_list.append(ability)
    print(f"ability_type_modifiers: {ability_type_modifiers}, ability_list: {ability_list}")
    #check for hidden ability
    if pokemon_obj.hidden_ability != "" and pokemon_obj.hidden_ability not in ability_type_modifiers:
        #add if there is a hidden ability and it is not in the ability type modifier list 
        ability_list.append(pokemon_obj.hidden_ability)
    print(f"ability_type_modifiers: {ability_type_modifiers}, ability_list: {ability_list}")

    #used multiple times
    filename = ___CSV_TYPES___
    #use the csv as data source
    with open(filename) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                #get the information of the type
                attack_type = row["Type"]
                                
                #first defense type
                multiplier_1 = row[pokemon_obj.type[0]]
                if multiplier_1 == "":
                    multiplier_1 = float(1)
                else:
                    multiplier_1 = float(multiplier_1)
                
                #set second multiplier to 1 (if there is not second type)
                multiplier_2 = float(1)
                if len(pokemon_obj.type) > 1 and pokemon_obj.type[1] != "":
                    multiplier_2 = row[pokemon_obj.type[1]]
                    if multiplier_2 == "":
                        multiplier_2 = float(1)
                    else:
                        multiplier_2 = float(multiplier_2)
                
                #calculate the damage multiplier
                damage_multiplier = multiplier_1 * multiplier_2
                #check if we neet to create an entry
                if damage_multiplier not in score:
                    #add empty list
                    score[damage_multiplier] = []

                #print(f"ability_type_modifiers: {ability_type_modifiers}, ability_list: {ability_list}")

                #if there are type_modifiers
                if len(ability_type_modifiers) > 0:
                    
                    #if our ability affects this specific type
                    if attack_type in ability_type_modifiers:
                        #get the data 
                        data = ability_type_modifiers[attack_type]
                        #set the multiplier
                        multiplier_3 = float(data["modifier"])
                        #calculate the damage multiplier for with the ability
                        damage_multiplier_ability = damage_multiplier * multiplier_3
                        #if it should absorb
                        if multiplier_3 == -1:
                            #set to absorb
                            damage_multiplier_ability = -1
                        #check if we need to create an entry
                        if damage_multiplier_ability not in score:
                            #add empty list
                            score[damage_multiplier_ability] = []


                        #print(f"ability_list: {ability_list} & {damage_multiplier}")
                        #print(f"type ability: {data["ability"]} & {damage_multiplier_ability}")

                        #first: if there are other abilities which DO NOT modify typing
                        if len(ability_list) > 0:
                            #add the non-affected typing to score list (with the extra text)
                            score[damage_multiplier].append(attack_type + f" ({", ".join(ability_list)})")
                            #add the affected typing to score list (with the extra text)
                            score[damage_multiplier_ability].append(attack_type + f" ({data["ability"]})")
                        #if there is only 1 ability
                        else:
                            #only add the calculation, not the extra text at the attack type
                            score[damage_multiplier_ability].append(attack_type)                    

                #no ability typing, just add the value
                else:
                    #add to score list
                    score[damage_multiplier].append(attack_type)

        #if exception
        except csv.Error as e:
            #print and exit
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    
    #sort dict
    score_sorted = sorted(score.items(), key=operator.itemgetter(0), reverse=True)
    #default return value
    return score_sorted          