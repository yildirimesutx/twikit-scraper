# Twitter Archive Scraper

A Python tool for scraping historic tweets (e.g. 2018–2020) using the Twikit library without the official API.

## Features

* Full-archive keyword search (no 7-day limit)
* Automatic pagination (handles cursor and rate limits)
* Saves results to CSV

---

## Prerequisites

* macOS/Linux or Windows with WSL
* Python 3.8+ installed
* Git (for cloning this repo)

---

## Quickstart



### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv        # create venv
source .venv/bin/activate    # activate on macOS/Linux
# .venv\Scripts\activate   # activate on Windows PowerShell
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install twikit
```

### 3. Configure login credentials

Create a `config.ini` file in the project root with your X.com (Twitter) credentials:

```ini
[X]
username = your_username_or_email
email    = your_email_if_required
password = your_password
```

> These credentials are used only once to log in and save cookies.

### 4. Save cookies for authenticated requests

Run the login step to generate `cookies.json`:

```bash
python main.py --save-cookies
```

> This will open a browser session, perform login, and write `cookies.json`.

### 5. Scrape tweets to CSV

Once cookies are saved, run the scraper:

```bash
python main.py
```

* Tweets matching your `QUERY` are fetched (default: 2021 Bitcoin tweets).
* Results are written to `tweets.csv` in the project directory.

---

## Configuration

* **`main.py`**: Adjust the following constants at the top:

  * `DESIRED_TWEETS`: How many tweets to fetch total.
  * `QUERY`: Your search query (keywords, date filters, language, user filters).
  * `COOKIES_FILE`: Cookies filename (default: `cookies.json`).
  * `CSV_FILE`: Output CSV filename.

---

## Notes

* The first run requires login to save cookies; subsequent runs skip login.
* If rate-limited, the script will automatically wait until reset.
* For very large volumes, increase `DESIRED_TWEETS` and adjust `PAGE_SIZE` in `main.py`.

---


