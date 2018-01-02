'''
Reddit bot to scrape reddit and export post and comment data for later analysis.
'''

import logging
import json
import praw
from praw.models import MoreComments

def log_init():

    ''' Basic logger for HTTP requests initiated by PRAW '''

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger('prawcore')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

def scrape():

    '''
    Initialize praw Reddit instance.
    This bot only scrapes data, so read-only is fine.
    '''

    # Hardcode for now because repo is private.
    reddit = praw.Reddit(client_id='dSDs-_PW0eb4RA',
                         client_secret='A6a2PTksaeweAs5Ev-fiYmbrHe8',
                         user_agent='crypto-bot-ua',
                         username='crypto-trend-tracker-bot')

    # Final array that will be written to score outfile.
    data_score = []

    # Multi-word / hyphenated crypto IDs will be stripped to first word.
    # Also populate score array with nonstripped crypto IDs.
    # ASSUMPTION: Cryptolist and Cryptotickers are sorted for a 1 to 1 mapping.
    # Convert files to list
    cryptolist_list = []
    cryptosymbols_list = []

    with open('cryptocurrencies/cryptolist.txt', 'r') as c_list:
        for line in c_list:
            data_score.append([line.strip(), 0])
            cryptolist_list.append(line.split("-")[0].strip())

    with open('cryptocurrencies/cryptotickers.txt', 'r') as c_symbol:
        for line in c_symbol:
            cryptosymbols_list.append(line.strip())

    # Subreddits to scrape
    subreddit_list = ['cryptocurrency']
    for subreddit_to_track in subreddit_list:
        subreddit = reddit.subreddit(subreddit_to_track)

        # Final array that will be written to score_context outfile.
        data = []

        # Iterate through a subreddit's top X submissions
        for submission in subreddit.hot(limit=25):
            thread_metadata = {}
            comment_list = []

            # Iterate through comment tree.
            submission.comments.replace_more(limit=0)
            for comment in submission.comments:
                comment_metadata = {}

                # Filter for comment scores that are less than a certain score
                if comment.score < 2:
                    continue

                # Check to see if any in cryptolist/cryptotickers are mentioned
                # Bool to check if any cryptos were found, if none then discard comment from context.
                match_found = False
                # List of matches associated with a comment block, used for context
                matches_list = []
                for i in range(len(cryptolist_list)):
                    row = data_score[i]
                    temp_body = comment.body.lower().split()
                    if cryptolist_list[i] in temp_body or cryptosymbols_list[i] in temp_body:
                        matches_list.append(cryptolist_list[i])
                        match_found = True
                        row[1] = row[1] + 1

                if not match_found:
                    continue
                else:
                    comment_metadata['score'] = comment.score
                    comment_metadata['matches'] = matches_list
                    comment_metadata['content'] = comment.body

                    # Append to a list for later inclusion into thread_metadata
                    comment_list.append(comment_metadata)

            # Create thread object mapped to a single thread
            thread_metadata['title'] = submission.title
            thread_metadata['score'] = submission.score
            thread_metadata['comments'] = comment_list
            data.append(thread_metadata)

        # Export to JSON file. This contains some context to score data.
        with open('data/reddit_data.json', 'w') as outfile:
            json.dump(data, outfile)

        # Export to JSON file. This contains calculated score totals.
        with open('data/reddit_data_score.json', 'w') as outfile:
            json.dump(data_score, outfile)

def main():

    ''' Driver for program '''
    log_init()
    scrape()

if __name__ == '__main__':
    main()
