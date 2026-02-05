import requests
import logging
from datetime import datetime

def fetch_hacker_news_trends():
    """
    Fetches top stories from Hacker News and filters for AI/Python tech.
    """
    logging.info("Fetching Hacker News Top Stories")
    try:
        # Get top story IDs
        top_ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        top_ids = requests.get(top_ids_url, timeout=10).json()
        
        trends = []
        keywords = ["AI", "LLM", "GPT", "Model", "Data", "Python", "Claude", "Gemini"]
        
        # Check first 50 stories for performance
        for story_id in top_ids[:50]:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story = requests.get(story_url, timeout=5).json()
            
            if not story:
                continue
                
            score = story.get("score", 0)
            title = story.get("title", "")
            
            # Filtering: Score >= 100 and relevant keywords
            if score >= 100 and any(kw.lower() in title.lower() for kw in keywords):
                trends.append({
                    "source": "hacker_news",
                    "name": title,
                    "owner": story.get("by", "Unknown"),
                    "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                    "description": title,
                    "stars": score, # Score as a metric
                    "daily_stars": score,
                    "language": "tech",
                    "fetched_at": datetime.now().isoformat()
                })
        
        return trends
    except Exception as e:
        logging.error(f"Failed to fetch Hacker News: {e}")
        return []
