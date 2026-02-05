import json
import os
from datetime import datetime
import logging

# Import trend sources
from agent_watcher.sources.github import fetch_github_trending
from agent_watcher.sources.product_hunt import fetch_product_hunt_trends
from agent_watcher.sources.hacker_news import fetch_hacker_news_trends
from agent_watcher.sources.zenn import fetch_zenn_trends
from agent_watcher.sources.qiita import fetch_qiita_trends

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_trends(data, filename_prefix="trends"):
    """Saves the raw trend data to a daily file."""
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(output_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filepath = os.path.join(output_dir, f"{filename_prefix}_{date_str}.json")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    logging.info(f"Saved {len(data)} trends to {filepath}")

def main():
    """
    Main execution flow to hunt trends from all sources.
    """
    logging.info("--- Project Trend-Hunter Started ---")
    
    # 1. Gather all trends
    all_trends = []
    
    # GitHub (General & Python)
    all_trends.extend(fetch_github_trending())
    all_trends.extend(fetch_github_trending("python"))
    
    # Product Hunt
    all_trends.extend(fetch_product_hunt_trends())
    
    # Hacker News
    all_trends.extend(fetch_hacker_news_trends())
    
    # Japanese tech trends
    all_trends.extend(fetch_zenn_trends())
    all_trends.extend(fetch_qiita_trends())
    
    # 2. Deduplication based on URL
    seen_urls = set()
    unique_trends = []
    for trend in all_trends:
        if trend["url"] not in seen_urls:
            unique_trends.append(trend)
            seen_urls.add(trend["url"])
            
    # 3. Sort by 'daily_stars' (Ranking signal)
    # This ensures the best potential tools are at the top for the analyst.
    sorted_trends = sorted(unique_trends, key=lambda x: x.get("daily_stars", 0), reverse=True)
    
    # 4. Save results
    save_trends(sorted_trends)
    logging.info("--- Project Trend-Hunter Completed ---")

if __name__ == "__main__":
    main()
