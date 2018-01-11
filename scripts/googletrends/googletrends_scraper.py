''' Grab info from google trends API for search trends '''

import pandas as pd
from pytrends.request import TrendReq

def main():

    ''' Program driver '''

    pytrends = TrendReq(hl='en-US', tz=360)

    data_score = []
    kw_list_id = []
    kw_list_sym = []

    with open('input_data/cryptolist.txt', 'r') as readfile:
        for line in readfile:
            data_score.append([line.strip(), 0])
            kw_list_id.append(line.split("-")[0].strip())

    with open('input_data/cryptotickers.txt', 'r') as readfile:
        for line in readfile:
            kw_list_sym.append(line.strip())

    kw_list_id = ['bitcoin', 'ethereum', 'litecoin', 'bitcoin cash']

    pytrends.build_payload(kw_list_id, cat=0, timeframe='today 3-m', geo='', gprop='')
    frame = pytrends.interest_over_time()
    print(frame)

    # Rate limiting is pretty harsh. Hard to test...

if __name__ == '__main__':
    main()
