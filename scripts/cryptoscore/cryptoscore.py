'''Generate/update cryptoscore.json file that tracks score/metrics of valid crypto'''
# pylint: disable=W0612, E0401

import json
from coinmarketcap import Market

def generate_cryptoscore(curated_cryptolist):

    ''' First time generation of cryptoscore list based on curated list'''

    # Instantiate list for post-conversion
    new_cryptolist = []

    # Reassemble data into a single JSON object for future update efficiency
    # Index of new_cryptolist respectively refer to...
    # Crypto-id, twitter_score, reddit_score, and usd_price.
    for currency in curated_cryptolist:
        new_cryptolist.append([currency, 0, 0, 0.0])

    # Time vs. score array.
    t_score = []

    # 720 points corresponding to hourly scrape data.
    for i in range(1):
        t_score.append(new_cryptolist)

    # Export to JSON
    with open('scripts/cryptoscore/cryptoscore_template.json', 'w') as outfile:
        json.dump(t_score, outfile)

def main():

    ''' program driver '''

    # Instantiate market object
    market = Market()

    # Load curated list into hashtable
    curated_cryptolist = []
    with open('input_data/cryptolist.txt') as readfile:
        for line in readfile:
            curated_cryptolist.append(line.strip())

    # Generate cryptoscore
    generate_cryptoscore(curated_cryptolist)

if __name__ == '__main__':
    main()
