import requests
from bs4 import BeautifulSoup
import json
import logging

def fetch_x_trends():
    """
    Fetches hot topics/keywords that are currently trending in Japan to help AI craft trend-aware tweets.
    Since official X API is restricted, we use a public aggregator or search results.
    """
    logging.info("Fetching X (Twitter) trends via aggregator...")
    
    # We can use a site like 'getdaytrends.com' or similar public aggregators for Japanese trends.
    url = "https://getdaytrends.com/japan/"
    trends = []
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for trend strings
            trend_items = soup.select('td.a.trend-name a')
            for item in trend_items[:15]: # Top 15 trends
                trends.append(item.text.strip())
        
        if not trends:
             # Fallback: search-based extraction or hardcoded hot keywords if scraping fails
             trends = ["AI", "ChatGPT", "新NISA", "副業", "エンジニア"]
             
    except Exception as e:
        logging.error(f"Failed to fetch X trends: {e}")
        trends = ["AI", "エンジニア", "自動化"]

    return trends

if __name__ == "__main__":
    print(json.dumps(fetch_x_trends(), ensure_ascii=False, indent=2))
