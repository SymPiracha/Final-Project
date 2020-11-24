import re


def identify_name(title):
    # convert title string to lower case
    title = title.lower()
    # remove anything which is not a lower case char and replace by whitespace
    title = re.sub("[^a-z]+", " ", title)
    # split string into an array based on white space
    title = title.split()

    # iterate through the list and check if any array element is 'trump' or 'biden', return True if it is
    for word in title:
        if 'trump' in word or 'biden' in word:
            return True
    return False

def main():
    print(identify_name("Lalatrubidelala 123Trump's"))
 

if __name__ == '__main__':
    main()