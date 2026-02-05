import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

def fetch_zenn_trends():
    """
    Scrapes trending articles from Zenn.dev tech section.
    """
    url = "https://zenn.dev/tech/trends"
    logging.info(f"Fetching Zenn trends: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        # Current CSS selector as of Feb 2026 (hypothetical/typical)
        for article in soup.select('article')[:10]:
            title_tag = article.select_one('h2')
            if not title_tag: continue
            
            title = title_tag.get_text(strip=True)
            link_tag = article.select_one('a')
            if not link_tag: continue
            
            url_suffix = link_tag.get('href')
            full_url = f"https://zenn.dev{url_suffix}"
            
            articles.append({
                "source": "zenn",
                "name": title,
                "owner": "Zenn Authors",
                "url": full_url,
                "description": title,
                "stars": 50, # Arbitrary base score for trending
                "daily_stars": 50,
                "language": "japanese",
                "fetched_at": datetime.now().isoformat()
            })
        return articles
    except Exception as e:
        logging.error(f"Failed to fetch Zenn trends: {e}")
        return []
