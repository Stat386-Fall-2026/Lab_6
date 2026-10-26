# Data files

`scripts/scrape_data.py` writes extracted records to `raw/talks_raw.csv`. This file is the raw output of a live scrape of the official October 2025 General Conference index and its linked talk pages.

Do not edit the raw file manually. Re-run the script to recollect data. Keep transformations in code and write processed records to `processed/talks_clean.csv`.

The source website can change over time. Record when you ran the scraper and inspect failures or unexpected empty fields rather than assuming the source is unchanged.
