'''Parse reddit and twitter exported JSON data to track mention metrics'''
import json
from pprint import pprint

def reddit_parse():

    '''Parse reddit data'''

    reddit_data = json.load(open('data/reddit_data.json'))
    cryptoscore_list = json.load(open('cryptocurrencies/cryptoscore.json'))

    # Iterate through data and track mentions

def twitter_parse():

    '''Parse twitter data'''

    twitter_data = json.load(open('data/twitter_data.json'))

def main():

    ''' program driver '''

    reddit_parse()
    # twitter_parse()

if __name__ == '__main__':
    main()
