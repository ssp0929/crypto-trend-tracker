import coinmarketcap
import pandas as pd
import numpy as np
import time
#######################################################################
#######################################################################
# Simple time-series data collector to establish a dataframe of       #
# cryptocurrency prices over discrete time points. The crypto-        #
# currencies to analyze will be targeted from a list given in a .txt  #
# file. Initial assessment is to be conducted hourly over a monthly   #
# time period. Results are output into a CSV file to later analyze    #
#######################################################################
#######################################################################


#######################################################################
#######################################################################
#initial stuff


#initialize parameters 
market = coinmarketcap.Market()
discrete_points = 720 
cryptolist = []


#function to return price of a cryptocurrency from cmc api
def price(currency):
	crypto = market.ticker(currency)[0]
	crypto_price = float(crypto.get('price_usd'))
	return crypto_price



#create list of cryptos from file containing targets 
with open("cryptolist.txt", "r") as f:
	for line in f:
		currency = line.split()[0]
		cryptolist.append(currency)



#pre-allocate a pandas dataframe to avoid 
#memory/efficieny problems
CryptoArray = pd.DataFrame(index=np.arange(0, discrete_points), 
	                                   columns=(i for i in cryptolist))


#######################################################################
#######################################################################
#main process 


#update dataframe entries (i,j) by iterating through 
#and retrieving data from api. Look at upgrading this method.
for row in range(discrete_points):
	for currency in cryptolist:
		CryptoArray.at[row, currency] = price(currency)
    #set to repeat after one hour
	time.sleep(3600)




#output dataframe to a csv for later analysis
CryptoArray.to_csv('example2.csv')

#######################################################################
#######################################################################