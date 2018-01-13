''' Generate snapshot of Cryptoscore and stores it in cryptscore_snapshot '''

import json
from datetime import date

def main():

    ''' Program driver '''

    date_str = str(date.today())
    data = []

    with open('data/cryptoscore.json', 'r') as readfile:
        data = json.load(readfile)

    with open('data/cryptoscore_snapshot/cryptoscore_' + date_str + '.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == '__main__':
    main()
