#script functions that handles all type specific comparisons and calculations



#imports
import csv, sys, operator



#constants
___CSV_TYPES___ = "Data/types.csv"
___CSV_TYPE_ABILITIES___ = "Data/type_ability.csv"


#assuming object pokemon_obj
def get_weakness(pokemon_obj):
    #keep track of scores
    score = {}

    #get the type modifiers from the abilities
    ability_type_modifiers = get_ability_type_modifiers(pokemon_obj)

    #used multiple times
    filename = ___CSV_TYPES___
    #use the csv as data source
    with open(filename) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                attack_type = row["Type"]
                
                multiplier_1 = row[pokemon_obj.type[0]]
                if multiplier_1 == "":
                    multiplier_1 = float(1)
                else:
                    multiplier_1 = float(multiplier_1)
                damage_multiplier = multiplier_1
                
                multiplier_2 = float(1)
                if len(pokemon_obj.type) > 1 and pokemon_obj.type[1] != "":
                    multiplier_2 = row[pokemon_obj.type[1]]
                    if multiplier_2 == "":
                        multiplier_2 = float(1)
                    else:
                        multiplier_2 = float(multiplier_2)
                    
                #multiplier for abilities
                multiplier_3 = float(1)
                #if our ability affects this type
                if attack_type in ability_type_modifiers:
                    #get the data 
                    data = ability_type_modifiers[attack_type]
                    #set the multiplier
                    multiplier_3 = float(data["modifier"])
                    #change the type to include the ability name
                    attack_type += f" ({data["ability"]})"

                #calculate multiplier
                damage_multiplier = damage_multiplier * multiplier_2 * multiplier_3
                #correct it if it is absorbed
                if multiplier_3 == -1:
                    #absorb
                    damage_multiplier = -1
                #set to 0 if 0
                if damage_multiplier == float(0):
                    damage_multiplier = 0

                #if entry does not exists
                if damage_multiplier not in score:
                    #add empty list
                    score[damage_multiplier] = []
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



#function to check the abilities
def get_ability_type_modifiers(pokemon_obj):
    
    #TODO: Wonder guard

    #list of modifiers
    type_modifiers = {}
    #get the abilities of the pokemon 
    pokemon_abilities = pokemon_obj.abilities
    #used multiple times
    filename = ___CSV_TYPE_ABILITIES___
    #use the csv as data source
    with open(filename) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        try:
            #check every ability
            for row in reader:
                #get the ability
                ability = row["Ability"]
                #if we have this ability
                if ability in pokemon_abilities:
                    #get the types
                    types = row["Type"].split(",")
                    #get the number of modifiers
                    number_of_modifiers = len(types)
                    #get the modifiers
                    modifiers = row["Modifier"].split(",")
                    #for each modifier
                    for index in range(number_of_modifiers):
                        type = types[index]
                        modifier = modifiers[index]
                        #write to list
                        type_modifiers[type] = {"modifier": modifier, "ability": ability}
         #if exception
        except csv.Error as e:
            #print and exit
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    
    #handle wonderguard
    #if "Wonder Guard" in pokemon_abilities:
        #create copy
        #dummy_pokemon_obj = pokemon_obj
        #remove abilities (to prevent recursion)
        #dummy_pokemon_obj.abilities = ["",""]
        #dummy_pokemon_obj.hidden_ability = ""
        #weaknesses = get_weakness(dummy_pokemon_obj)
        #for weakness in weaknesses:
            #print(f"weakness: {weakness}")
    #print(f"type_modifiers: {type_modifiers}")
    #return the modifiers
    return type_modifiers          