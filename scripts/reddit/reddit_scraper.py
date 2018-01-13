'''
Reddit bot to scrape reddit and export submission_object and comment data for later analysis.
'''
# pylint: disable=R0914

import logging
import json
import time
import praw

def log_init():

    ''' Basic logger for HTTP requests initiated by PRAW '''

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger('prawcore')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

def create_comment_object(comment, matches_list):

    ''' Create comment object for inclusion in context file '''

    comment_object = {}
    comment_object['score'] = comment.score
    comment_object['matches'] = matches_list
    comment_object['content'] = comment.body

    return comment_object

def create_submission_object(submission, comment_list):

    ''' Create submission object for inclusion in context file'''

    submission_object = {}
    submission_object['title'] = submission.title
    submission_object['score'] = submission.score
    submission_object['comments'] = comment_list

    return submission_object

def scrape(reddit):

    '''
    Initialize praw Reddit instance.
    This bot only scrapes data, so read-only is fine.
    '''

    # Final array that will be written to reddit_output outfile.
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
    # Subpar Big(O) but...
    # relatively inconsequential for a script that only runs once every 60 minutes...
    with open('reddit_config.json', 'r') as readfile:
        reddit_config = json.load(readfile)
        subreddits_to_track = reddit_config.get('subreddits-to-track')
        last_run_time = reddit_config.get('last-run-time', 0)
        minimum_comment_score = reddit_config.get('minimum-comment-score', 0)
        subreddit_parse_limit = reddit_config.get('subreddit-parse-limit', 25)
        reddit_config.update({'last-run-time': time.time()})

    with open('reddit_config.json', 'w') as outfile:
        json.dump(reddit_config, outfile)

    for tracked_subreddit in subreddits_to_track:
        subreddit = reddit.subreddit(tracked_subreddit)

        # Final array that will be written to context data outfile.
        data = []

        # Iterate through a subreddit's top X submissions
        for submission in subreddit.hot(limit=subreddit_parse_limit):
            # List of comments tied to a specific submission thread
            comment_list = []

            # Iterate through comment tree.
            submission.comments.replace_more(limit=0)
            for comment in submission.comments:
                # Filter for comment scores that are less than a certain score
                if comment.score < minimum_comment_score:
                    continue

                # Filter for comments made after last check date
                if comment.created_utc < last_run_time:
                    continue

                # Check to see if any in cryptolist/cryptotickers are mentioned
                # Check if any cryptos were found, if none then discard comment from context.
                match_not_found = True
                # List of matches associated with a comment block, used for context
                matches_list = []
                for i in range(0, len(cryptolist_list)):
                    row = data_score[i]
                    comment_contents = comment.body.lower().split()

                    # Find matches and increment score
                    if cryptolist_list[i] in comment_contents or \
                       cryptosymbols_list[i] in comment_contents:
                        matches_list.append(cryptolist_list[i])
                        match_not_found = False
                        row[1] = row[1] + 1

                # If match not found, then don't include comment in context data.
                if match_not_found:
                    continue
                else:
                    # Append to a list for later inclusion into submission_object
                    comment_list.append(create_comment_object(comment, matches_list))

            # Create submission_object mapped to a single submission
            data.append(create_submission_object(submission, comment_list))

        # Export to JSON file. This contains some context to score data.
        with open('scripts/reddit/context_data.json', 'w') as outfile:
            json.dump(data, outfile)

        # Export to JSON file. This contains calculated score totals.
        with open('data/reddit_output.json', 'w') as outfile:
            json.dump(data_score, outfile)

def main():

    ''' Driver for program '''

    # Load from credentials file that isn't tracked by git.
    with open('credentials.json', 'r') as readfile:
        credentials = json.load(readfile).get('reddit')

    reddit = praw.Reddit(client_id=credentials.get('client_id'),
                         client_secret=credentials.get('client_secret'),
                         user_agent=credentials.get('user_agent'),
                         username=credentials.get('username'))

    log_init()
    scrape(reddit)

if __name__ == '__main__':
    main()
