'''
Twitter bot to scrape twitter and export tweet data for later analysis.
'''
# pylint: disable=E0401, C0301, W0212

import json
import io
import tweepy
from tweepy import OAuthHandler

def create_status_object(status, matches_list):

    ''' Create status object to append to list of tweets '''

    status_object = {}
    status = status._json
    status_object['username'] = status.get('user').get('name')
    status_object['twitter_handle'] = status.get('user').get('screen_name')
    status_object['favorites'] = status.get('favorite_count')
    status_object['retweets'] = status.get('retweet_count')
    status_object['matches'] = matches_list
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

    # Multi-word / hyphenated crypto IDs will be stripped to first word.
    # Also populate score array with nonstripped crypto IDs.
    # ASSUMPTION: Cryptolist and Cryptotickers are sorted for a 1 to 1 mapping.
    # Convert files to list
    cryptolist_list = []
    cryptosymbols_list = []
    data = []
    data_score = []

    with open('input_data/cryptolist.txt', 'r') as readfile:
        for line in readfile:
            data_score.append([line.strip(), 0])
            cryptolist_list.append(line.split("-")[0].strip())

    with open('input_data/cryptotickers.txt', 'r') as readfile:
        for line in readfile:
            cryptosymbols_list.append(line.strip())

    # Get timeline of tweets/retweets to terminal
    # include_rts = False refers to reteweets being included or not
    last_run_id_not_logged = True

    for status in tweepy.Cursor(api.list_timeline, owner_screen_name=list_owner, slug=list_name, since_id=last_run_id).items():
        # Skip retweets and favorites from showing up
        if status.retweeted or 'RT @' in status.text:
            continue

        # Log tweet ID so keep track of previously fetched tweets
        if last_run_id_not_logged:
            twitter_config.update({'last-run-id': status.id_str})
            last_run_id_not_logged = False

        # If tweet truncated then re-search using extended mode
        if status.truncated:
            status = api.get_status(status.id_str, tweet_mode='extended')

        # Check to see if any in cryptolist/cryptotickers are mentioned
        # Check if any cryptos were found, if none then discard comment from context.
        match_not_found = True

        # If full_text exists grab it, otherwise use text
        tweet_contents = ''
        try:
            status.full_text
        except AttributeError:
            tweet_contents = status.text.lower().split()
        else:
            tweet_contents = status.full_text.lower().split()

        # List of matches associated with a comment block, used for context
        matches_list = []
        for i in range(0, len(cryptolist_list)):
            row = data_score[i]
            # Find matches and increment score
            if cryptolist_list[i] in tweet_contents or \
                cryptosymbols_list[i] in tweet_contents:
                matches_list.append(cryptolist_list[i])
                match_not_found = False
                row[1] = row[1] + 1

        # If match not found, then don't include comment in context data.
        if match_not_found:
            data.append(create_status_object(status, matches_list))
        else:
            # Append to a list for later inclusion into submission_object
            data.append(create_status_object(status, matches_list))

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
