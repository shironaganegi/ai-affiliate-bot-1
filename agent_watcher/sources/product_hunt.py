import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
import logging

def fetch_product_hunt_trends():
    """
    Fetches today's top products from Product Hunt RSS.
    """
    url = "https://www.producthunt.com/feed"
    logging.info(f"Fetching Product Hunt RSS: {url}")
    
    try:
        feed = feedparser.parse(url, agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    except Exception as e:
        logging.error(f"Failed to fetch Product Hunt: {e}")
        return []
    
    products = []
    for entry in feed.entries[:10]:
        try:
            name = entry.get('title', 'Unknown')
            link = entry.get('link', '')
            raw_desc = entry.get('summary', 'New product on Product Hunt')
            desc_soup = BeautifulSoup(raw_desc, 'html.parser')
            clean_desc = desc_soup.get_text()[:200]
            
            products.append({
                "source": "product_hunt",
                "name": name,
                "owner": "ProductHunt",
                "url": link,
                "description": clean_desc,
                "stars": 0,
                "daily_stars": 100, # Score placeholder
                "language": "saas",
                "fetched_at": datetime.now().isoformat()
            })
        except Exception as e:
            logging.warning(f"Error parsing Product Hunt item: {e}")
            continue
    
    return products
