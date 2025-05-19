#imports
import os
from configparser import ConfigParser
from constants import ___CONFIG_FILE___, ___OPERATING_MODE_LOCAL___, ___OPERATING_MODE_ONLINE___ 



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
        set_default_config()
    #return the config
    return config_object



#function that gets the operating mode
def get_operating_mode():
    #get the config
    config = get_config()
    #get the operating mode
    operating_mode = config["DATABASE"]["mode"]
    #if not a correct config
    if operating_mode != ___OPERATING_MODE_LOCAL___ and operating_mode != ___OPERATING_MODE_ONLINE___:
        #set config back to default
        set_default_config()
        #return error
        return None, ValueError(f"Incorrect operating_mode config: {operating_mode}, reverting to {___OPERATING_MODE_LOCAL___}")
    #return operating mode
    return operating_mode, None



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



#function that writes default config
def set_default_config():
    #Create a ConfigParser object
        config_object = ConfigParser()
        #create object
        config_object["DATABASE"] = {
        "mode": ___OPERATING_MODE_LOCAL___,
        }
        # Write the configuration to a file named 'config.ini' with 
        with open(___CONFIG_FILE___, 'w') as conf: 
            config_object.write(conf)