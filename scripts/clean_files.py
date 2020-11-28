import re
import json
import argparse
import pandas as pd

def to_tsv(dataframe,output_file):
    dataframe.to_csv(output_file, sep = '\t', index=False)


def extract_relevent_fields(list_of_all_posts):
    all_names = []
    all_titles = []
    # iterate through all the posts in our list of posts
    for post in list_of_all_posts:
        # store the name and title key in variables
        name = post['name']
        title = post['title']

        # check if the title contains mention of Trump or Biden
        # if it does, add this tou our final lists
        if identify_name(title):
            all_names.append(name)
            all_titles.append(title)

    # create a dictionary with our relevent lists
    data = {'Name': all_names, 'Title': all_titles}
    # create a dataframe from our data dictionary with relevent column headings
    df = pd.DataFrame (data, columns = ['Name','Title'])
    df["Coding"] = ""

    return df

def read_json(json_file):
    # create a list of posts and iterate through the file to add each post to this list
    list_of_all_posts = []
    with open(json_file, 'r') as f:
        for line in f:
            post = json.loads(line)
            list_of_all_posts.append(post)

    return list_of_all_posts

def identify_name(title):
    # convert title string to lower case
    title = title.lower()
    # remove anything which is not a lower case char and recplace by whitespace
    title = re.sub("[^a-z]+", " ", title)
    # split string into an array based on white space
    title = title.split()

    # iterate through the list and check if any array element is 'trump' or 'biden', return True if it is
    for word in title:
        if 'trump' in word or 'biden' in word:
            return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('json_file', type=str, help='json file we are looking at at')
    parser.add_argument('tsv_file', type=str, help='tsv file to output after filtering')
    arg = parser.parse_args()

    list_of_all_posts = read_json(arg.json_file)
    df = extract_relevent_fields(list_of_all_posts)
    to_tsv(df,arg.tsv_file)
 

if __name__ == '__main__':
    main()