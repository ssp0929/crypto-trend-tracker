#!/bin/bash
echo "Generating Cryptoscore Template"
python3 scripts/cryptoscore/cryptoscore.py
echo "Running Reddit Scraper"
python3 scripts/reddit/reddit_scraper.py
echo "Running Twitter Scraper"
python3 scripts/twitter/twitter_scraper.py
echo "Running Coinmarketcap Scraper"
python3 scripts/coinmarketcap/cmc_scraper.py
echo "Running Data Parser"
python3 scripts/parser/data_parser.py
echo "Generating daily snapshot"
python3 scripts/snapshot/snapshot_script.py
echo "Sleeping for 30 seconds... check for errors."
sleep 30s
