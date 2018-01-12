'''Generate/update cryptoscore.json file that tracks score/metrics of valid crypto'''
# pylint: disable=W0612, E0401

import json
from coinmarketcap import Market

def generate_cryptoscore(current_cryptolist, curated_cryptolist):

    ''' First time generation of cryptoscore list based on curated list'''

    # Instantiate list for post-conversion
    new_cryptolist = []

    # Reassemble data into a single JSON object for future update efficiency
    # Index of new_cryptolist respectively refer to...
    # Crypto-id, twitter_score, reddit_score, and usd_price.
    for values in current_cryptolist:
        if values['id'] in curated_cryptolist:
            new_cryptolist.append([values['id'], 0, 0, 0.0])

    # Time vs. score array.
    t_score = []

    # 720 points corresponding to hourly scrape data.
    for i in range(720):
        t_score.append(new_cryptolist)

    # Export to JSON
    with open('scripts/cryptoscore/cryptoscore_template.json', 'w') as outfile:
        json.dump(t_score, outfile)

def main():

    ''' program driver '''

    # Instantiate market object
    market = Market()

    # Load curated list into hashtable
    curated_cryptolist = {}
    with open('input_data/cryptolist.txt') as readfile:
        for line in readfile:
            curated_cryptolist[line.strip()] = 1 # placeholder, really just need the hash table.

    # Grab all cryptocurrencies from coinmarketcap
    current_cryptolist = market.ticker(limit=0)

    # Generate cryptoscore
    generate_cryptoscore(current_cryptolist, curated_cryptolist)

if __name__ == '__main__':
    main()
