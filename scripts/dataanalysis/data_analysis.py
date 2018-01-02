'''
Simple time-series data collector to establish a dataframe of
cryptocurrency prices over discrete time points. The crypto-
currencies to analyze will be targeted from a list given in a .txt
file. Initial assessment is to be conducted hourly over a monthly
time period. Results are output into a CSV file to later analyze
'''

import pandas as pd
import numpy as np

def update_dataframe(crypto_array):

    '''
    update dataframe entries (i,j) by iterating through
    and retrieving data from api. Look at upgrading this method.
    '''

    # TODO: Don't retrieve from API, retrieve from local flat file cryptoscore.json

def gen_list():

    '''create list of cryptos from file containing targets'''

    crypto_list = []
    with open("crypto_list.txt", "r") as readfile:
        for line in readfile:
            crypto_list.append(line.strip())

    return crypto_list

def main():

    ''' program driver '''

    # initialize parameters
    discrete_points = 720
    crypto_list = gen_list()

    # memory/efficieny problems
    crypto_array = pd.DataFrame(index=np.arange(0, discrete_points),
                                columns=(i for i in crypto_list))

    # update dataframe, sleep 60 minute intervals.
    update_dataframe(crypto_array)

    # output dataframe to a csv for later analysis
    crypto_array.to_csv('data/crypto_dataframe.csv')

if __name__ == '__main__':
    main()