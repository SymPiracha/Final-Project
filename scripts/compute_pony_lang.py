import sys
import json
import argparse
import csv
import copy
# maybe check for stopwords

def file_trim(file):
    # trimming the dictionary to only have words that appear atleast 5 times
    # need to iterate over the first level of keys in the json
    # then the second level and filter only for works with that appear 5 or more times
    # also need to take out words that contain non-alpha characters
    file1 = copy.deepcopy(file) # deepycopy used to iterate over since a runtime error occured when iterating over og
    # could probably also work with the list thing as long as you keep the same thing at line 25
    for character in file1.keys():
        for word in file1[character].keys():
            if not word.isalpha() or file1[character][word] < 5:
                try:
                    file[character].pop(word)
                except:
                    continue           
    return file

def replace_better(old, new, string):
    ''' Takes a string, list of words to replace and replacement work, iterates over the words in
    old and replaces them with new returns the string that has been altered
    '''
    for word in old:
        string = string.replace(word, new)
    return string

def update_word(line, name, file):
    # add the helper function for this
    # takes the line, character name and json file
    # updates the wordcount for that character 
    # returns the whole json dictionary 
    to_replace = ["(",")",",","-",".","?","!",":",";","#","&","]","["] # may need to add quotation marks
    line = replace_better(to_replace, ' ', line)
    words = line.split()
    for word in words:
        # update the dictionary
        if word.lower() in file[name].keys():
            file[name][word.lower()] += 1
        else:
            # add the key if it isnt there yet
            file[name][word.lower()] = 1
    return file

def compute_word_counts(input_file, output):
    # opening the input file
    file_open = csv.reader(open(input_file), delimiter='\t')
    # creating the json output
    output_file = {'transition':{},'scandal_trump':{},'scandal_biden':{},'policy_trump':{},\
    'policy_biden':{},'opinion':{}, 'election_fraud':{}, 'election_results':{}, 'other':{}} 
    # hopefull this^ line break works fine
    for line in file_open:
        # checking to see which pony is speaking
        if line[2].lower() == "t":
            # do update word with their dirctionary
            output_file = update_word(line[1],'transition', output_file)
        elif line[2].lower() == 'ts':
            output_file = update_word(line[1],'scandal_trump', output_file)
        elif line[2].lower() == 'bs':
            output_file = update_word(line[1],'scandal_biden', output_file)
        elif line[2].lower() == 'tp':
            output_file = update_word(line[1],'policy_trump', output_file)
        elif line[2].lower() == "bp":
            output_file = update_word(line[1],'policy_biden', output_file)
        elif line[2].lower() == 'o':
            output_file = update_word(line[1],'opinion', output_file)
        elif line[2].lower() == 'ef':
            output_file = update_word(line[1],'election_fraud', output_file)
        elif line[2].lower() == 'er':
            output_file = update_word(line[1],'election_results', output_file)
        elif line[2].lower() == 'other':
            output_file = update_word(line[1],'other', output_file)

    # trimming the words down
    output_file = file_trim(output_file)
    # write the output file to the specified location
    output = open(output, 'w')
    json.dump(output_file, output)
    output.close()
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', help="This is the json file that the results will be written to")
    parser.add_argument('input')
    args = parser.parse_args()
    compute_word_counts(args.input, args.o)

if __name__ == '__main__':
    main()
