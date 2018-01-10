'''
Reddit bot to scrape reddit and export submission_object and comment data for later analysis.
'''
# pylint: disable=C0200, R0914

import logging
import json
import praw

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

    # Load from credentials file that isn't tracked by git.
    credentials = json.load(open('credentials.json'))['reddit']
    reddit = praw.Reddit(client_id=credentials['client_id'],
                         client_secret=credentials['client_secret'],
                         user_agent=credentials['user_agent'],
                         username=credentials['username'])

    # Final array that will be written to score outfile.
    data_score = []

    # Multi-word / hyphenated crypto IDs will be stripped to first word.
    # Also populate score array with nonstripped crypto IDs.
    # ASSUMPTION: Cryptolist and Cryptotickers are sorted for a 1 to 1 mapping.
    # Convert files to list
    cryptolist_list = []
    cryptosymbols_list = []

    with open('input_data/cryptolist.txt', 'r') as readfile:
        for line in readfile:
            data_score.append([line.strip(), 0])
            cryptolist_list.append(line.split("-")[0].strip())

    with open('input_data/cryptotickers.txt', 'r') as readfile:
        for line in readfile:
            cryptosymbols_list.append(line.strip())

    # Subreddits to scrape
    # TODO: Clean up this method. Big O(n*m*k*l) not good.
    # Relatively inconsequential for a script that only runs once every 60 minutes...
    subreddits_to_track = ['cryptocurrency']
    for tracked_subreddit in subreddits_to_track:
        subreddit = reddit.subreddit(tracked_subreddit)

        # Final array that will be written to score_context outfile.
        data = []

        # Iterate through a subreddit's top X submissions
        for submission in subreddit.hot(limit=25):
            submission_object = {}
            comment_list = []

            # Iterate through comment tree.
            submission.comments.replace_more(limit=0)
            for comment in submission.comments:
                comment_object = {}

                # Filter for comment scores that are less than a certain score
                if comment.score < 2:
                    continue

                # Check to see if any in cryptolist/cryptotickers are mentioned
                # Check if any cryptos were found, if none then discard comment from context.
                match_found = False
                # List of matches associated with a comment block, used for context
                matches_list = []
                for i in range(len(cryptolist_list)):
                    row = data_score[i]
                    comment_contents = comment.body.lower().split()

                    # Find matches
                    if cryptolist_list[i] in comment_contents or \
                       cryptosymbols_list[i] in comment_contents:
                        matches_list.append(cryptolist_list[i])
                        match_found = True
                        row[1] = row[1] + 1

                # If match not found, then don't include comment in context data.
                if not match_found:
                    continue
                else:
                    comment_object['score'] = comment.score
                    comment_object['matches'] = matches_list
                    comment_object['content'] = comment.body

                    # Append to a list for later inclusion into submission_object
                    comment_list.append(comment_object)

            # Create submission_object mapped to a single submission
            submission_object['title'] = submission.title
            submission_object['score'] = submission.score
            submission_object['comments'] = comment_list
            data.append(submission_object)

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
