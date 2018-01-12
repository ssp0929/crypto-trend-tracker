'''
Twitter bot to scrape twitter and export tweet data for later analysis.
'''
# pylint: disable=E0401, C0301, W0212

import json
import io
import twitter

def get_list_timeline(api):

    ''' Get timeline of curated twitter followers '''

    # Public list created by Moes19
    with open('twitter_config.json', 'r') as readfile:
        twitter_config = json.load(readfile)
        list_name = twitter_config.get('list-name')
        list_owner = twitter_config.get('list-owner')

    # Get timeline of tweets/retweets to terminal
    # include_rts = False refers to reteweets being included or not
    list_timeline = api.GetListTimeline(slug=list_name, owner_screen_name=list_owner, include_rts=False)

    # Export to file, need encoding specification because emojis in tweets break ASCII
    with io.open('scripts/twitter/timeline_dump.txt', mode='w', encoding='utf-8') as outfile:
        for status in list_timeline:
            outfile.write("-------------\n" + status.text + "\n")

def main():

    ''' Program driver '''

    # Load credentials from non-git tracked file.
    with open('credentials.json', 'r') as readfile:
        credentials = json.load(readfile).get('twitter')

    api = twitter.Api(consumer_key=credentials.get('consumer_key'),
                      consumer_secret=credentials.get('consumer_secret'),
                      access_token_key=credentials.get('access_token_key'),
                      access_token_secret=credentials.get('access_token_secret'))

    # Get timeline of curated twitter followers
    get_list_timeline(api)

if __name__ == '__main__':
    main()
