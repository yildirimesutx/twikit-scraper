import asyncio
import time
import csv
from datetime import datetime
from configparser import ConfigParser
from random import randint
from twikit import Client, TooManyRequests
from twikit.errors import NotFound

# Configuration
desired_tweets = 100
QUERY = 'bitcoin lang:en since:2021-01-01 until:2021-12-31'
COOKIES_FILE = 'cookies.json'
CSV_FILE = 'tweets.csv'
PAGE_SIZE = 20

# Load credentials (if needed)
config = ConfigParser()
config.read('config.ini')
username = config.get('X', 'username', fallback=None)
email    = config.get('X', 'email',    fallback=None)
password = config.get('X', 'password', fallback=None)

async def main():
    client = Client(language='en-US')
    client.load_cookies(COOKIES_FILE)
    print(f"Loaded cookies from {COOKIES_FILE}")

    all_tweets = []
    cursor = None

    while len(all_tweets) < desired_tweets:
        try:
            if cursor is None:
                print(f"{datetime.now()} - Fetching first page (Latest)...")
                # Try Latest, fallback to Top if not available
                try:
                    page = await client.search_tweet(QUERY, product='Latest', count=PAGE_SIZE)
                except NotFound:
                    print("Latest endpoint not found, falling back to Top...")
                    page = await client.search_tweet(QUERY, product='Top', count=PAGE_SIZE)
            else:
                wait = randint(5, 10)
                print(f"{datetime.now()} - Waiting {wait}s before next page...")
                await asyncio.sleep(wait)
                page = await cursor.next()
        except TooManyRequests as e:
            reset_time = datetime.fromtimestamp(e.rate_limit_reset)
            secs = (reset_time - datetime.now()).total_seconds()
            print(f"Rate limit. Sleeping {secs:.0f}s until {reset_time}")
            await asyncio.sleep(max(secs, 0))
            continue

        if not page:
            print(f"{datetime.now()} - No more tweets.")
            break

        remaining = desired_tweets - len(all_tweets)
        all_tweets.extend(page[:remaining])
        cursor = page
        print(f"{datetime.now()} - Collected {len(all_tweets)} tweets so far")

    # Save to CSV
    with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Index','Username','Text','Created_At','Retweets','Likes'])
        for idx, tw in enumerate(all_tweets, start=1):
            writer.writerow([
                idx,
                tw.user.name,
                tw.text.replace('\n',' '),
                tw.created_at,
                tw.retweet_count,
                tw.favorite_count
            ])
    print(f"Done! Saved {len(all_tweets)} tweets to {CSV_FILE}")

if __name__ == '__main__':
    asyncio.run(main())
