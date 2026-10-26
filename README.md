# Lab 6: Collecting Data from the Web

## Objective

Inspect a website's scraping guidance, complete a small HTML-extraction function, and collect records from one General Conference. Preserve the raw output, create a processed dataset, and evaluate two proposed AI changes to the scraper.

## Create your personal repository

1. Click **Use this template** and select **Create a new repository**.
2. For **Owner**, select `Stat386-Fall-2026`.
3. Name your repository using the format `your_netid_lab_6`.
4. Set the repository visibility to **Private**.
5. Click **Create repository**.

## Clone and set up the project

Clone your personal repository inside your `School/STAT_386` folder:

```bash
git clone <your-repository-url>
cd <your-repository-name>
uv sync
```

The first time you run `uv sync`, it will create a `uv.lock` file. Include that file in your commits.

Open the repository folder in Positron. Select the Python interpreter inside the `.venv` folder created by `uv`.

## Complete the lab

Open `lab_6.qmd` and replace `Your Name` with your name. Work through the sections in order.

Before running the scraper, complete the source-guidance check and the `extract_title()` function in `scripts/scrape_data.py`. The supplied code handles requests, delays, link discovery, and CSV output.

After completing the function and checking the source guidance, collect the data from the repository root:

```bash
uv run python scripts/scrape_data.py
```

The scraper creates `data/raw/talks_raw.csv`. Complete the remaining code and written responses in `lab_6.qmd`, including code that creates `data/processed/talks_clean.csv`.

Once the raw data have been collected successfully, keep that file unchanged while cleaning and rendering. Rendering the document should read the saved CSV rather than run the scraper again.

You can preview your document with:

```bash
uv run quarto preview lab_6.qmd
```

Stop the preview by pressing `Ctrl+C` in the terminal. Make several meaningful commits as you work. For example:

```bash
git add scripts/scrape_data.py lab_6.qmd uv.lock
git commit -m "Complete title extraction and source inspection"
git push
```

## Work with the AI Collaborator

After completing the collection, cleaning, and written responses, commit and push your work. You will then review two proposed additions to your scraper. Each interaction creates a Pull Request.

Both reviews ask whether an additional function is appropriate for this lab. Inspect its code, the requested path, the website's guidance, and the assignment's scope. You can evaluate a proposed request without executing it. Adding a function definition does not by itself send a request.

### First AI Collaborator interaction

Create a new Issue using the **Lab 6 Complete** Issue template. If the template is unavailable, create a regular Issue titled `Lab 6 complete`; its description can be empty.

Post the following command as a **new comment**, not in the Issue description:

```text
@local-llm-user process config-dir: Lab_6/metadata_01.yml in instructor-repo: Stat386-Fall-2026/Instructor_Repo
```

Once the collaborator creates a Pull Request:

1. Read the Pull Request description.
2. Inspect the proposed code in **Files changed**.
3. Answer every review question in a comment on that Pull Request.
4. Explain whether the proposed addition fits the lab and respects the website's guidance.
5. Merge the Pull Request if appropriate, or close it without merging if inappropriate.

You are evaluated on your reasoning, not on accepting the change. You do not need to execute the proposed function or make a separate code revision to reject it.

If you merge the Pull Request, update your local repository before continuing:

```bash
git pull
```

### Second AI Collaborator interaction

After reviewing the first Pull Request, return to the **same Lab 6 completion Issue**. If the Issue was closed automatically, reopen it before posting the next command.

Post the following command as a new comment:

```text
@local-llm-user process config-dir: Lab_6/metadata_02.yml in instructor-repo: Stat386-Fall-2026/Instructor_Repo
```

Review the second Pull Request using the same process. Answer all questions in a comment and explain your decision to merge or close it. If you merge it, run `git pull` again.

## Render and submit

After both reviews, render the final document from a fresh session:

```bash
uv run quarto render lab_6.qmd
```

Commit and push your source document, rendered HTML, completed script, dependency lockfile, and both datasets:

```bash
git add lab_6.qmd lab_6.html scripts/scrape_data.py uv.lock data/raw/talks_raw.csv data/processed/talks_clean.csv
git commit -m "Complete Lab 6"
git push
```

Follow the submission directions provided in Canvas.

## Before you finish

- [ ] Your name appears in the document header.
- [ ] The source-guidance check is documented before collection.
- [ ] `extract_title()` is complete and works on both supplied examples.
- [ ] Every code section and written response is complete.
- [ ] Raw and processed data are saved separately and committed.
- [ ] Cleaning is performed in code, without manually editing the raw CSV.
- [ ] Validation results and extraction limitations are explained.
- [ ] Both AI Pull Requests have your answers and a justified merge/close decision.
- [ ] `lab_6.qmd` renders without errors using the saved raw data.
- [ ] `lab_6.html`, scripts, and `uv.lock` are committed.
- [ ] All commits are pushed to GitHub.

## Repository contents

```text
Lab_6/
├── .github/
│   └── ISSUE_TEMPLATE/
│       └── lab-6-complete.md
├── .gitignore
├── README.md
├── lab_6.qmd
├── pyproject.toml
├── data/
│   └── HeadsUp.md
└── scripts/
    └── scrape_data.py
```

Your work will add `uv.lock`, `lab_6.html`, `data/raw/talks_raw.csv`, and `data/processed/talks_clean.csv`.