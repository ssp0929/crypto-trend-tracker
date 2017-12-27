import logging
import praw

def log_init():
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger('prawcore')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

def scrape():
    # Initialize praw Reddit instance.
    # This bot only scrapes data, so read-only is fine.
    # Hardcode for now because repo is private.
    reddit = praw.Reddit(client_id='dSDs-_PW0eb4RA',
                         client_secret='A6a2PTksaeweAs5Ev-fiYmbrHe8',
                         user_agent='crypto-bot-ua',
                         username='crypto-trend-tracker-bot')

    # Subreddits to scrape, for now one.
    subreddit = reddit.subreddit('cryptocurrency')

    f = open('reddit_scraper/data.txt', 'w')
    # Iterate through a subreddit's top X submissions
    for submission in subreddit.hot(limit=20):
        f.write(submission.title + '\n' +
                str(submission.score) + '\n' +
                str(submission.id) + '\n' +
                submission.url + '\n\n')

    f.close()

def main():
    log_init()
    scrape()

if __name__ == '__main__':
    main()
