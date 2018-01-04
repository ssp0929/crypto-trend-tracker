'''
Twitter bot to scrape twitter and export tweet data for later analysis.
'''
# pylint: disable=E0401, C0301, W0212

import json
import io
import tweepy
from tweepy import OAuthHandler

def get_list_timeline(api):

    ''' Get timeline of curated twitter followers '''

    # Public list created by Moes19
    list_name = 'Crypto'
    list_owner = 'derek_finley'

    # Get timeline of tweets/retweets to terminal
    curated_list_timeline = api.list_timeline(list_owner, list_name)

    # Export to file, need encoding specification because emojis in tweets break ASCII
    with io.open('scripts/twitter/timeline_dump.txt', mode='w', encoding='utf-8') as outfile:
        for status in curated_list_timeline:
            outfile.write("-------------\n" + status.text + "\n")

def get_rate_limit(api):

    ''' Get rate limit data and export to file + terminal '''

    # Check rate limit status each run
    rate_limit_json = api.rate_limit_status()
    rate_limit_remaining = rate_limit_json['resources']['application']['/application/rate_limit_status']['remaining']
    print('App-wide API requests remaining for current hour: ' + str(rate_limit_remaining))

    # Export to file
    with open('scripts/twitter/rate_limit_log.json', 'w') as outfile:
        json.dump(rate_limit_json, outfile)

def main():

    ''' Program driver '''

    # Keys, secrets, and tokens. Hard coded because code isn't open-source and visible.
    # IMPERATIVE THAT THIS CODE IS NOT MADE PUBLIC.
    # At least until I obfuscate and open source this myself
    consumer_key = 'Foxiwn9uPMr717PyncbHC45Kk'
    consumer_secret = 'MS0V32zOnpt3JuMX9sBHFVWD4gPZP1yzvsECgNfIerODlL6mZT'
    access_token = '461520833-5pgg2wYQUxlCjjWBfaft7Xbw5jC2U8c5JymH7xab'
    access_secret = '9HFVyWeoFQhc2ERx2CvjxvjIqzVMvJkSHMkzQ3hvdhqdv'

    # OAuth
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # Map auth to API calls
    api = tweepy.API(auth)

    # Check rate limit status each run
    get_rate_limit(api)

    # Get timeline of curated twitter followers
    get_list_timeline(api)

if __name__ == '__main__':
    main()
