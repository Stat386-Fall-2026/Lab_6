# Data files

After completing the source-guidance check and title-extraction function, run `uv run python scripts/scrape_data.py` from the repository root. It creates `data/raw/talks_raw.csv` from the live October 2025 conference index and its individual article pages.

Record the collection date and any warnings in `lab_6.qmd`. Once collection works, keep the raw CSV unchanged. Perform transformations in code and save processed records to `data/processed/talks_clean.csv`.

The extracted text may include headings, bylines, and notes. The `date` field is intentionally blank, and speaker extraction may be incomplete. Document these limitations rather than inventing values.

Commit both CSV files to your private course repository. Rendering the document should use the saved raw data rather than trigger another scrape.