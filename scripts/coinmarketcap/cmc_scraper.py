'''
Grab bitcoin price of crypto targets.
'''
# pylint: disable=E0401

import json
from coinmarketcap import Market

def get_price(currency, market):

    '''function to return price of a cryptocurrency from cmc api'''

    # Cached every 120 seconds so no harm "calling" this 20 times in a smaller time span
    crypto = market.ticker(limit=0)

    # I think looping through a data structure in memory O(N^2)
    # and fetching from SQLite cache 20 times is still faster than
    # relying on 20 separate API calls to coinmarketcap (uncached!).
    currency_found = False
    for crypto_currency in crypto:
        if currency == crypto_currency.get('id'):
            currency_found = True
            print(currency + ' found')
            crypto = crypto_currency
            break

    if currency_found:
        crypto_price = float(crypto.get('price_usd'))
    else:
        # Return -1 to indicate some sort of error
        crypto_price = -1.0

    return crypto_price

def main():

    ''' program driver '''

    # initialize parameters
    market = Market()
    data_price = []

    # Populate crypto/price list
    with open('input_data/cryptolist.txt', 'r') as readfile:
        for line in readfile:
            print(line.strip())
            price = get_price(line.strip(), market)
            data_price.append([line.strip(), price])

    # Export to JSON
    with open('data/cmc_output.json', 'w') as outfile:
        json.dump(data_price, outfile)

if __name__ == '__main__':
    main()
