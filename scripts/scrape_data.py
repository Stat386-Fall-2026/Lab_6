"""Collect talk metadata from one official General Conference index.

Run from the repository root:
    uv run python scripts/scrape_data.py

The script deliberately saves extracted values before downstream cleaning.
It does not attempt to crawl other conferences or the wider website.
"""
from __future__ import annotations

import csv
import logging
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

CONFERENCE = "2025/10"
INDEX_URL = (
    "https://www.churchofjesuschrist.org/study/general-conference/"
    "2025/10?lang=eng"
)
BASE_HOST = "www.churchofjesuschrist.org"
OUTPUT = Path("data/raw/talks_raw.csv")
USER_AGENT = (
    "STAT386-Lab6-StudentProject/1.0 "
    "(educational data collection; limited requests)"
)
TIMEOUT_SECONDS = 20
POLITE_DELAY_SECONDS = 1.0
MAX_TALK_PAGES = 40

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def canonicalize_url(url: str) -> str:
    """Drop query/fragment components for stable deduplication."""
    parsed = urlparse(url)
    path = re.sub(r"/+$", "", parsed.path)
    return urlunparse((parsed.scheme, parsed.netloc, path, "", "", ""))


def fetch_html(session: requests.Session, url: str) -> str:
    """Fetch a page and fail clearly for HTTP/network errors."""
    try:
        response = session.get(url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Could not retrieve {url}: {exc}") from exc

    content_type = response.headers.get("Content-Type", "")
    if "html" not in content_type.lower():
        raise RuntimeError(
            f"Expected HTML from {url}, received Content-Type={content_type!r}"
        )
    return response.text
def discover_talk_urls(index_html: str) -> list[str]:
    """Find individual talk pages that belong to the selected conference."""
    soup = BeautifulSoup(index_html, "html.parser")
    urls: list[str] = []
    seen: set[str] = set()

    for anchor in soup.select("a[href]"):
        href = anchor.get("href", "").strip()
        if not href:
            continue
        absolute = urljoin(INDEX_URL, href)
        parsed = urlparse(absolute)

        if parsed.netloc != BASE_HOST:
            continue
        if f"/study/general-conference/{CONFERENCE}/" not in parsed.path:
            continue

        # The index itself and session pages are not individual talk pages.
        tail = parsed.path.split(f"/study/general-conference/{CONFERENCE}/", 1)[-1]
        if not tail or "/" in tail:
            continue
        if tail.endswith("-session"):
            continue

        canonical = canonicalize_url(absolute)
        if canonical not in seen:
            seen.add(canonical)
            urls.append(canonical)

    if not urls:
        raise RuntimeError(
            "No individual talk URLs were found. The page layout may have changed; "
            "inspect the live index and update the selectors/rules deliberately."
        )

    return urls[:MAX_TALK_PAGES]


def extract_talk_record(url: str, html: str) -> dict[str, str]:
    """Extract conservative metadata and the visible article text."""
    soup = BeautifulSoup(html, "html.parser")

    # Prefer the page's primary heading, with <title> as a fallback.
    heading = soup.select_one("h1")
    title = heading.get_text(" ", strip=False) if heading else ""
    if not title.strip() and soup.title:
        title = soup.title.get_text(" ", strip=False)

    # Meta descriptions often contain a byline or summary, but are not assumed
    # to be the speaker's name. The speaker field stays blank unless a byline
    # is identified with a conservative, inspectable heuristic.
    speaker = ""
    for selector in [
        "[itemprop='author']",
        "[rel='author']",
        ".byline",
        ".author",
    ]:
        node = soup.select_one(selector)
        if node:
            speaker = node.get_text(" ", strip=False)
            break

    article = soup.select_one("main article") or soup.select_one("article") or soup.select_one("main")
    if article is None:
        raise RuntimeError(f"Could not find a main article/content region on {url}")

    # Preserve the extracted text as-is apart from HTML-to-text extraction.
    # Do not collapse whitespace or apply the cleaning rules from Lab 5 here.
    text = article.get_text(separator="\n", strip=False)

    return {
        "talk_name": title,
        "speaker": speaker,
        "conference": "October 2025",
        "date": "",
        "link": url,
        "text": text,
    }


def main() -> None:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
        }
    )

    logging.info("Fetching conference index: %s", INDEX_URL)
    index_html = fetch_html(session, INDEX_URL)
    talk_urls = discover_talk_urls(index_html)
    logging.info("Found %s candidate talk pages (maximum %s).", len(talk_urls), MAX_TALK_PAGES)

    records: list[dict[str, str]] = []
    failures: list[str] = []

    for number, url in enumerate(talk_urls, start=1):
        if number > 1:
            time.sleep(POLITE_DELAY_SECONDS)
        try:
            logging.info("Fetching talk %s/%s", number, len(talk_urls))
            html = fetch_html(session, url)
            records.append(extract_talk_record(url, html))
        except RuntimeError as exc:
            failures.append(str(exc))
            logging.warning("%s", exc)

    if not records:
        raise RuntimeError(
            "No talk records were extracted. No output file was written. "
            "Inspect the live page and adjust extraction logic."
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["talk_name", "speaker", "conference", "date", "link", "text"]
    with OUTPUT.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    logging.info("Saved %s raw records to %s", len(records), OUTPUT)
    if failures:
        logging.warning("%s page(s) failed. See warnings above.", len(failures))


if __name__ == "__main__":
    main()
