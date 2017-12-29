'''Generate/update cryptoscore.json file that tracks score/metrics of valid crypto'''

import json
import os

from coinmarketcap import Market

def generate_cryptoscore(current_cryptolist):

    ''' First time generation of cryptoscore list '''

    # Instantiate list for post-conversion
    new_cryptolist = {}

    # Reassemble data into a single JSON object for future update efficiency
    for values in current_cryptolist:
        new_cryptolist[values['id']] = {
            'name': values['name'],
            'symbol': values['symbol'],
            'reddit_score': 0,
            'twitter_score': 0
        }

    # Export to JSON
    with open('cryptocurrencies/cryptoscore.json', 'w') as outfile:
        json.dump(new_cryptolist, outfile)

def update_cryptoscore(current_cryptolist):

    ''' Update valid cryptocurrencies in cryptoscore'''

    # Load previous cryptoscore
    prev_cryptolist = json.load(open('cryptocurrencies/cryptoscore.json'))

    # Instantiate list for post-conversion
    new_cryptolist = {}

    # Reassemble data into a single JSON object for future update efficiency
    # Only for currencies that don't already exist in the previous list
    for values in current_cryptolist:
        if values['id'] not in prev_cryptolist:
            new_cryptolist[values['id']] = {
                'name': values['name'],
                'symbol': values['symbol'],
                'reddit_score': 0,
                'twitter_score': 0
            }

    prev_cryptolist.update(new_cryptolist)

    with open('cryptocurrencies/cryptoscore.json', 'w') as outfile:
        json.dump(prev_cryptolist, outfile)

def main():

    ''' program driver '''

    # Instantiate market object
    market = Market()

    # Grab all cryptocurrencies from coinmarketcap
    current_cryptolist = market.ticker(limit=0)

    # Check if cryptoscore exists
    cryptoscore_exists = os.path.isfile('./cryptocurrencies/cryptoscore.json')

    # Decide whether to generate file if it doesn't exist or update if it does
    if cryptoscore_exists:
        update_cryptoscore(current_cryptolist)
    else:
        generate_cryptoscore(current_cryptolist)

if __name__ == '__main__':
    main()
