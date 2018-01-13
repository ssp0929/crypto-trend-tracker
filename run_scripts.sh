#!/bin/bash
echo "Generating Cryptoscore Template"
pipenv run python scripts/cryptoscore/cryptscore.py
echo "Running Reddit Scraper"
pipenv run python scripts/reddit_scraper/reddit_scraper.py
echo "Running Twitter Scraper"
pipenv run python scripts/twitter_scraper/twitter_scraper.py
echo "Running Coinmarketcap Scraper"
pipenv run python scripts/coinmarketcap/cmc_scraper.py
echo "Running Data Parser"
pipenv run python scripts/parser/data_parser.py
