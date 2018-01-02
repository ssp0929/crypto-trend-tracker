# Crypto trend tracker.

## Reddit scrape script

Scrape top 25 posts of a given subreddit(s) and parse comments for tracked list mentions.

> pipenv run python scripts/reddit/reddit_scraper.py

Output in data/reddit_data.json

---

## Parser

TODO: Parses data generated from reddit scrape script to track mentions of cryptocurrencies.

> pipenv run python scripts/parser/data_parser.py

Output in data/mention_count.json (not implemented yet)

---

## CMC script

Grabs cryptocurrency price data every 60 minutes from coinmarketcap.

> pipenv run python scripts/coinmarketcap/cmc_scraper.py

---

## Cryptoscore Generator

Generates cryptoscore if it does not exist...
Updates if it does with any new coins added to the coinmarketcap database without overwriting existing data.

> pipenv run python scripts/cryptoscore/cryptoscore.py

---