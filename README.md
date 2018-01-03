# Crypto trend tracker.

---

## Twitter scrape script

Scrape from curated twitter accounts and parse tweets for tracked list mentions.

> pipenv run python scripts/twitter/twitter_scraper.py

Output in data/twitter\_data\_score.json

Additional output in data/twitter_data.json for verbose context.

## Reddit scrape script

Scrape top 25 posts of a given subreddit(s) and parse comments for tracked list mentions.

> pipenv run python scripts/reddit/reddit_scraper.py

Output in data/reddit\_data\_score.json.

Additional output in data/reddit_data.json for verbose context.

---

## Parser

TODO: Parses data generated from reddit scrape script to track mentions of cryptocurrencies.

> pipenv run python scripts/parser/data_parser.py

Output in data/mention_count.json.

---

## CMC script

Grabs cryptocurrency price data from coinmarketcap.

> pipenv run python scripts/coinmarketcap/cmc_scraper.py

---

## Cryptoscore Generator

Generates example file of what final data table will look like before analysis is run.

> pipenv run python scripts/cryptoscore/cryptoscore.py

---