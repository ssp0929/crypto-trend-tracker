'''
Twitter bot to scrape twitter and export tweet data for later analysis.
'''
# pylint: disable=E0401, C0301, W0212

import json
import io
import tweepy
from tweepy import OAuthHandler

def create_status_object(status):

    ''' Create status object to append to list of tweets '''

    status_object = {}
    status = status._json
    status_object['username'] = status.get('user').get('name')
    status_object['twitter_handle'] = status.get('user').get('screen_name')
    status_object['favorites'] = status.get('favorite_count')
    status_object['retweets'] = status.get('retweet_count')
    status_object['text'] = status.get('full_text', status.get('text'))

    return status_object

def get_list_timeline(api):

    ''' Get timeline of curated twitter followers '''

    # Public list created by Moes19
    with open('twitter_config.json', 'r') as readfile:
        twitter_config = json.load(readfile)
        list_name = twitter_config.get('list-name')
        list_owner = twitter_config.get('list-owner')
        last_run_id = twitter_config.get('last-run-id', '1')

    # Get timeline of tweets/retweets to terminal
    # include_rts = False refers to reteweets being included or not
    list_timeline = api.list_timeline(list_owner, list_name, since_id=last_run_id, page=5)
    data = []
    data_score = []
    last_run_id_not_logged = True

    for status in list_timeline:
        # Skip retweets and favorites from showing up
        if status.retweeted or 'RT @' in status.text:
            continue

        # Log tweet ID so keep track of previously fetched tweets
        if last_run_id_not_logged:
            twitter_config.update({'last-run-id': status.id_str})
            last_run_id_not_logged = False

        # If tweet truncated then re-search using extended mode
        if status.truncated:
            extended_status = api.get_status(status.id_str, tweet_mode='extended')
            data.append(create_status_object(extended_status))
        else:
            data.append(create_status_object(status))

    # Log last_run_id to twitter_config and write out
    with open('twitter_config.json', 'w') as outfile:
        json.dump(twitter_config, outfile)

    # Export context score to file, need encoding specification because emojis in tweets break ASCII
    with io.open('scripts/twitter/context_data.json', mode='w', encoding='utf-8') as outfile:
        json.dump(data, outfile)

    # Export data score to file, need encoding specification because emojis in tweets break ASCII
    with io.open('data/twitter_output.json', mode='w', encoding='utf-8') as outfile:
        json.dump(data_score, outfile)

def get_rate_limit(api):

    ''' Get rate limit data and export to file + terminal '''

    # Check rate limit status each run
    rate_limit_json = api.rate_limit_status()
    rate_limit_remaining = rate_limit_json.get('resources').get('application').get('/application/rate_limit_status').get('remaining')
    print('App-wide API requests remaining for current hour: ' + str(rate_limit_remaining))

    # Export to file disabled for now...
    # with open('scripts/twitter/rate_limit_log.json', 'w') as outfile:
    #    json.dump(rate_limit_json, outfile)

def main():

    ''' Program driver '''

    # Load credentials from non-git tracked file.
    with open('credentials.json', 'r') as readfile:
        credentials = json.load(readfile).get('twitter')

    consumer_key = credentials.get('consumer_key')
    consumer_secret = credentials.get('consumer_secret')
    access_token_key = credentials.get('access_token_key')
    access_token_secret = credentials.get('access_token_secret')

    # OAuth
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    # Map auth to API calls
    api = tweepy.API(auth)

    # Check rate limit status each run
    get_rate_limit(api)

    # Get timeline of curated twitter followers
    get_list_timeline(api)

if __name__ == '__main__':
    main()
