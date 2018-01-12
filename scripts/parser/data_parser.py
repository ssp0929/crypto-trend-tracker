'''Parse reddit and twitter exported JSON data to track mention metrics'''

import json

def reddit_parse():

    '''Parse reddit data'''
    with open('data/reddit_output.json', 'r') as readfile:
        reddit_data = json.load(readfile)

    with open('input_data/cryptoscore.json', 'r') as readfile:
        cryptoscore_list = json.load(readfile)

    # Iterate through data and track mentions

def twitter_parse():

    '''Parse twitter data'''

    with open('data/twitter_output.json', 'r') as readfile:
        twitter_data = json.load(readfile)

def main():

    ''' program driver '''

    reddit_parse()
    # twitter_parse()

if __name__ == '__main__':
    main()
