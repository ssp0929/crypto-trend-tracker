# Crypto trend tracker.

Reddit scrape script:

> pipenv run python scripts/reddit/reddit_scraper.py

Output in data/data.json

---

Parser:

> pipenv run python scripts/parser/data_parser.py

Output in data/mention_count.json

---

CMC script:

> pipenv run python scripts/timeseries/cmc_datacollector.py

---