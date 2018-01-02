'''Generate/update cryptoscore.json file that tracks score/metrics of valid crypto'''

import json

from coinmarketcap import Market

def generate_cryptoscore(current_cryptolist, curated_cryptolist):

    ''' First time generation of cryptoscore list based on curated list'''

    # Instantiate list for post-conversion
    new_cryptolist = []

    # Reassemble data into a single JSON object for future update efficiency
    for values in current_cryptolist:
        if values['id'] in curated_cryptolist:
            new_cryptolist.append([0,0])

    # Time vs. score array.
    t_score = []

    # Generate Time vs score objects in array, 720 points.
    for i in range(720):
        t_score.append(new_cryptolist)

    # Export to JSON
    with open('cryptocurrencies/cryptoscore.json', 'w') as outfile:
        json.dump(t_score, outfile)

def main():

    ''' program driver '''

    # Instantiate market object
    market = Market()

    # Load curated list into hashtable
    curated_cryptolist = {}
    with open('cryptocurrencies/cryptolist.txt') as f:
        for line in f:
            curated_cryptolist[line.strip()] = 1 # placeholder, really just need the hash table.

    # Grab all cryptocurrencies from coinmarketcap
    current_cryptolist = market.ticker(limit=0)

    # Generate cryptoscore
    generate_cryptoscore(current_cryptolist, curated_cryptolist)

if __name__ == '__main__':
    main()
