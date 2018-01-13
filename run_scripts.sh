#!/bin/bash
echo "Generating Cryptoscore Template"
pipenv run python scripts/cryptoscore/cryptoscore.py
echo "Running Reddit Scraper"
pipenv run python scripts/reddit/reddit_scraper.py
echo "Running Twitter Scraper"
pipenv run python scripts/twitter/twitter_scraper.py
echo "Running Coinmarketcap Scraper"
pipenv run python scripts/coinmarketcap/cmc_scraper.py
echo "Running Data Parser"
pipenv run python scripts/parser/data_parser.py
echo "Generating daily snapshot"
pipenv run python scripts/snapshot/snapshot_script.py
echo "Sleeping for 30 seconds... check for errors."
sleep 30s
