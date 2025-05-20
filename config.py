#imports
import os
from configparser import ConfigParser
from constants import ___CONFIG_FILE___, ___OPERATING_MODE_LOCAL___, ___OPERATING_MODE_ONLINE___, ___LOOKUP_LIMIT___



#get the config
def get_config(): 
    #create config object
    config_object = ConfigParser()
    #check if config exists
    if os.path.isfile(___CONFIG_FILE___):
        # Read the configuration from the 'config.ini' file
        config_object.read(___CONFIG_FILE___)
    #no config exists
    else: 
        #create default config
        repair_config()
    #return the config
    return config_object



#function that gets the operating mode
def get_operating_mode():
    #get the config
    config = get_config()
    #get the operating mode
    operating_mode = config.get("DATABASE", "mode", fallback=___OPERATING_MODE_LOCAL___) #config["DATABASE"]["mode"]
    #if not a correct config
    if operating_mode != ___OPERATING_MODE_LOCAL___ and operating_mode != ___OPERATING_MODE_ONLINE___:
        #set config back to default
        repair_config()
        #return error
        return None, ValueError(f"Incorrect operating_mode config: {operating_mode}, reverting to {___OPERATING_MODE_LOCAL___}")
    #return operating mode
    return operating_mode, None



#function that gets the limit of online retrieval
def get_retrieval_limit():
    #get the config
    config = get_config()
    #get the operating mode
    retrieval_limit = config.get("ONLINE", "limit", fallback=___LOOKUP_LIMIT___)
    #return operating mode
    return int(retrieval_limit)



#function that changes operating mode
def set_operating_mode(arguments):
    #guard clauses
    #if no argument
    if len(arguments) == 0:
        return SyntaxError(f"Not enough arguments: {len(arguments)} / 1")
    #if too many arguments
    elif len(arguments) > 1:
        return SyntaxError(f"Too many arguments: {len(arguments)} / 1")
    #get the key
    operating_mode = arguments[0]
    #check if it is a correct option
    if operating_mode != ___OPERATING_MODE_LOCAL___ and operating_mode != ___OPERATING_MODE_ONLINE___:
        return ValueError(f"Incorrect operating_mode config: '{operating_mode}', possible options: '{___OPERATING_MODE_LOCAL___}', '{___OPERATING_MODE_ONLINE___}'")
    
    # Create a ConfigParser object
    config_object = ConfigParser()
    # Read the configuration from the 'config.ini' file
    config_object.read(___CONFIG_FILE___)
    
    # Access the database section
    userinfo = config_object["DATABASE"]
    
    #if the current config is not the same
    if userinfo["mode"] != operating_mode:
        # Update the password in the USERINFO section
        userinfo["mode"] = operating_mode
        # Write the updated configuration back to the 'config.ini' file
        with open(___CONFIG_FILE___, 'w') as conf:
            config_object.write(conf)
    
    #print message
    print(f"Updated operating_mode to {operating_mode}")
    #return no error
    return None



#check and add missing config
def repair_config():
    #create a empty config parser
    config_object = ConfigParser()
    #check if config exists
    if os.path.isfile(___CONFIG_FILE___):
        #get the config instead
        config_object = get_config()    

    #for each desired section
    sections = ["DATABASE", "ONLINE", "GAMES"]
    #for each section
    for section in sections:
        #if section does not exist
        if not config_object.has_section(section):
            #add the section
            config_object.add_section(section)

    #get and set the values
    operating_mode = config_object.get("DATABASE", "mode", fallback=___OPERATING_MODE_LOCAL___)
    #if not an allowed value
    if operating_mode != ___OPERATING_MODE_LOCAL___ and operating_mode != ___OPERATING_MODE_ONLINE___:
        #set back to local
        operating_mode = ___OPERATING_MODE_LOCAL___

    #set the values
    config_object.set("DATABASE", "mode", operating_mode)
    config_object.set("ONLINE", "limit", config_object.get("ONLINE", "limit", fallback=f"{___LOOKUP_LIMIT___}"))
    config_object.set("GAMES", "games_with_hidden_ability", config_object.get("GAMES", "games_with_hidden_ability", fallback="False"))
    config_object.set("GAMES", "games_with_beast_ball", config_object.get("GAMES", "games_with_beast_ball", fallback="False"))

    # Write the configuration to a file named 'config.ini' with 
    with open(___CONFIG_FILE___, 'w') as conf: 
        config_object.write(conf)


def get_game_search_filters():
    #get the config instead
    config_object = get_config()    
    #get config for hidden ability
    hidden_ability = config_object.get("GAMES", "games_with_hidden_ability", fallback="False")
    #get config for beast ball
    beast_ball = config_object.get("GAMES", "games_with_beast_ball", fallback="False")
    #return the flags
    return hidden_ability == "True", beast_ball == "True"


