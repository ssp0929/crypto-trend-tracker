'''
Simple time-series data collector to establish a dataframe of
cryptocurrency prices over discrete time points. The crypto-
currencies to analyze will be targeted from a list given in a .txt
file. Initial assessment is to be conducted hourly over a monthly
time period. Results are output into a CSV file to later analyze
'''
# pylint: disable=E0401

import json
import pandas as pd
import numpy as np

def populate_dataframe(crypto_array, discrete_points):

    '''
    update dataframe entries (i,j) by iterating through
    and retrieving data from api. Look at upgrading this method.
    '''

    # TODO: Don't retrieve from API, retrieve from local flat file cryptoscore.json

def gen_list():

    '''create list of cryptos from file containing targets'''

    crypto_list = []
    with open("input_data/cryptolist.txt", "r") as readfile:
        for line in readfile:
            crypto_list.append(line.strip())

    return crypto_list

def main():

    ''' program driver '''

    # initialize parameters
    with open('pandas_config.json', 'r') as readfile:
        discrete_points = json.load(readfile).get('discrete-points')

    crypto_list = gen_list()

    # Create dataframe
    crypto_array = pd.DataFrame(index=np.arange(0, discrete_points),
                                columns=(i for i in crypto_list))

    # populate dataframe
    populate_dataframe(crypto_array, discrete_points)

    # output dataframe to a csv for later analysis
    crypto_array.to_csv('data/crypto_dataframe.csv')

if __name__ == '__main__':
    main()
