# Crypto trend tracker.

## Reddit scrape script

Basic scrape of top X posts from a subreddit.

> pipenv run python scripts/reddit/reddit_scraper.py

Output in data/reddit_data.json

---

## Parser

TODO: Parses data generated from reddit scrape script to track mentions of cryptocurrencies.

> pipenv run python scripts/parser/data_parser.py

Output in data/mention_count.json (not implemented yet)

---

## CMC script

Grabs cryptocurrency metric data every 60 minutes from coinmarketcap. Does stuff with Pandas. Yeah...

> pipenv run python scripts/timeseries/cmc_datacollector.py

---

## Cryptoscore Generator/Updater

Generates cryptoscore if it does not exist...
Updates if it does with any new coins added to the coinmarketcap database without overwriting existing data.

> pipenv run python scripts/coinmarketcap/cryptoscore.py

Output in cryptocurrencies/cryptoscore.json

---