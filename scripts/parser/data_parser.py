'''Parse reddit/twitter/cmc JSON data to track mention metrics and combine into end file.'''

# pylint: disable=C1801

import json
import os

def parse_data(cryptoscore_list=None):

    '''Parse reddit data'''

    prev_cryptoscore_exist = True
    if cryptoscore_list is None:
        prev_cryptoscore_exist = False
        with open('scripts/cryptoscore/cryptoscore_template.json', 'r') as readfile:
            cryptoscore_list = json.load(readfile)

    length = len(cryptoscore_list[0])

    with open('data/reddit_output.json', 'r') as readfile:
        reddit_data = json.load(readfile)

    with open('data/twitter_output.json', 'r') as readfile:
        twitter_data = json.load(readfile)

    with open('data/cmc_output.json', 'r') as readfile:
        cmc_data = json.load(readfile)

    # Check on cryptoscore_list, if prev_cryptoscore_exist and len are not same
    # Something is probably wrong in that case.
    if len(reddit_data) != length or len(twitter_data) != length or len(cmc_data) != length:
        print('The reddit/twitter/cmc output lists do not match length of cryptoscore list.')
        return

    with open('scripts/cryptoscore/cryptoscore_template.json', 'r') as readfile:
        data_score = json.load(readfile)[0]

    for i in range(0, length):
        row = data_score[i]
        # Add existing values from existing cryptoscore
        row[1] = reddit_data[i][1]
        row[2] = twitter_data[i][1]
        row[3] = cmc_data[i][1]

    if prev_cryptoscore_exist:
        cryptoscore_list.append(data_score)
    else:
        temp_list = []
        temp_list.append(data_score)
        with open('data/cryptoscore.json', 'w') as outfile:
            json.dump(temp_list, outfile)
        return

    with open('data/cryptoscore.json', 'w') as outfile:
        json.dump(cryptoscore_list, outfile)
    return

def main():

    ''' program driver '''

    if os.path.isfile('data/cryptoscore.json'):
        with open('data/cryptoscore.json', 'r') as readfile:
            cryptoscore_list = json.load(readfile)
        parse_data(cryptoscore_list)
    else:
        parse_data()

if __name__ == '__main__':
    main()
