'''
Grab bitcoin price of crypto targets.
'''

import json
from coinmarketcap import Market

def get_price(currency, market):

    '''function to return price of a cryptocurrency from cmc api'''

    crypto = market.ticker(currency)[0]
    crypto_price = float(crypto['price_usd'])

    return crypto_price

def main():

    ''' program driver '''

    # initialize parameters
    market = Market()
    data_price = []

    # Populate crypto/price list
    with open('cryptocurrencies/cryptolist.txt', 'r') as readfile:
        for line in readfile:
            print(line)
            data_price.append([line.strip(), get_price(line.strip(), market)])

    # Export to JSON
    with open('data/cmc_data_price.json', 'w') as outfile:
        json.dump(data_price, outfile)

if __name__ == '__main__':
    main()
