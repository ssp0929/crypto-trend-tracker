'''
Twitter bot to scrape twitter and export tweet data for later analysis.
'''

import tweepy
from tweepy import OAuthHandler

def scrape():

    ''' Scrape method '''




def main():

    ''' Program driver '''

    # Keys, secrets, and tokens. Hard coded because code isn't open-source and visible.
    # IMPERATIVE THAT THIS CODE IS NOT MADE PUBLIC.
    consumer_key = 'Foxiwn9uPMr717PyncbHC45Kk'
    consumer_secret = 'MS0V32zOnpt3JuMX9sBHFVWD4gPZP1yzvsECgNfIerODlL6mZT'
    access_token = '461520833-5pgg2wYQUxlCjjWBfaft7Xbw5jC2U8c5JymH7xab'
    access_secret = '9HFVyWeoFQhc2ERx2CvjxvjIqzVMvJkSHMkzQ3hvdhqdv'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

if __name__ == '__main__':
    main()
