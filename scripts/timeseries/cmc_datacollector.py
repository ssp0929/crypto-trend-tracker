import time

import coinmarketcap
import pandas as pd
import numpy as np

#######################################################################
#######################################################################
# Simple time-series data collector to establish a dataframe of       #
# cryptocurrency prices over discrete time points. The crypto-        #
# currencies to analyze will be targeted from a list given in a .txt  #
# file. Initial assessment is to be conducted hourly over a monthly   #
# time period. Results are output into a CSV file to later analyze    #
#######################################################################
#######################################################################

# function to return price of a cryptocurrency from cmc api
def get_price(currency, market):
    crypto = market.ticker(currency)[0]
    crypto_price = float(crypto.get('price_usd'))

    return crypto_price

# create list of cryptos from file containing targets
def gen_list():
    c_list = []
    with open("crypto_list.txt", "r") as readfile:
        for line in readfile:
            currency = line.split()[0]
            c_list.append(currency)

    return c_list

# update dataframe entries (i,j) by iterating through
# and retrieving data from api. Look at upgrading this method.
def update_dataframe(crypto_array, crypto_list, discrete_points, market):
    for row in range(discrete_points):
        for currency in crypto_list:
            price = get_price(currency, market)
            crypto_array.at[row, currency] = price
            # debug prints
            print(price)
        time.sleep(3600)

def main():
    # initialize parameters
    market = coinmarketcap.Market()
    discrete_points = 720
    crypto_list = gen_list()

    # memory/efficieny problems
    crypto_array = pd.DataFrame(index=np.arange(0, discrete_points), columns=(i for i in crypto_list))
    update_dataframe(crypto_array, crypto_list, discrete_points, market)

    # output dataframe to a csv for later analysis
    crypto_array.to_csv('data/crypto_dataframe.csv')

if __name__ == '__main__':
    main()
