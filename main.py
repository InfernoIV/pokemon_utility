#python3 main.py

#imports
#from stats import count_words, count_characters, sort_characters
import sys

#main function
def main() :
    #if not correct arguments
    if len(sys.argv) != 2:
        #print help message
        print("Usage: python3 main.py <cmd>")
        #stop
        sys.exit(1)
        #needed?
        return
    
    
    #define the path of the book
    #path_to_file = sys.argv[1] #"books/frankenstein.txt"
    #print_report(path_to_file)
    return