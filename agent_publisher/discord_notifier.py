import os
import glob
import json
import re
from datetime import datetime
from shared.utils import setup_logging, safe_requests_post

logger = setup_logging(__name__)

def send_discord_notification(webhook_url, title, zenn_url, x_post_text):
    """
    Sends a notification to Discord with article details and drafts.
    """
    # Simply use the provided title as tool name for now
    tool_name = title.split(":")[0].strip()

    # Generate Note Draft
    note_draft = generate_note_draft(title, zenn_url)

    # Create Discord Embed message
    embed = {
        "title": f"📝 記事配信完了: {tool_name}",
        "description": f"新規記事が公開されました！\n\n📌 **Zenn/Blog**: {zenn_url}",
        "color": 5763719, # Green
        "fields": [
            {"name": "X (旧Twitter) 投稿内容", "value": f"```\n{x_post_text}\n```", "inline": False},
            {"name": "Note 誘導記事ドラフト", "value": f"```\n{note_draft}\n```", "inline": False},
            {"name": "Generated At", "value": datetime.now().strftime("%Y-%m-%d %H:%M"), "inline": True}
        ],
        "footer": {"text": "AI Affiliate Bot - 集客支援システム"}
    }

    payload = {
        "username": "白ネギ・テック編集部",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
        "content": "**記事の配信と拡散準備が完了しました！** 🚀",
        "embeds": [embed]
    }
    
    response = safe_requests_post(webhook_url, json_data=payload)
    if response and (response.status_code == 200 or response.status_code == 204):
        logger.info("Discord notification sent successfully!")
        return True
    else:
        logger.error(f"Discord notification failed.")
        return False

def generate_note_draft(title, url):
    """
    Generates a draft text for note.mu.
    """
    note_title = f"【AI活用】{title} で作業効率が劇的に上がる件"
    note_body = f"""
{note_title}

最近話題のAIツール「{title}」を使ってみました。
これ、エンジニアじゃなくても実はめちゃくちゃ便利なんです。

✅ **ここがすごい！**
- 面倒な作業が自動化できる
- 無料（または低コスト）で始められる
- 今すぐ使える

詳しい使い方や、導入手順は私の技術ブログ（TechTrend Watch）で完全解説しています！
アフィリエイトリンクもバッチリ貼って収益化も狙えます（笑）

興味のある方はぜひチェックしてみてください👇

{url}

#AI #業務効率化 #副業 #便利ツール
    """
    return note_body.strip()

if __name__ == "__main__":
    # Get webhook URL from environment variable
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not webhook_url:
        print("ERROR: DISCORD_WEBHOOK_URL environment variable not set.")
        exit(1)
        
    # Find the latest article
    articles_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "articles")
    markdown_files = glob.glob(os.path.join(articles_dir, "*.md"))
    
    if not markdown_files:
        print("No articles found to notify.")
        exit(0)
        
    # Sort by modification time, newest first
    latest_file = max(markdown_files, key=os.path.getmtime)
    print(f"Latest article found: {latest_file}")
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract title (simple regex for markdown header or frontmatter)
        # Assuming frontmatter title: "title: ..."
        title_match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip().strip('"').strip("'")
        else:
            # Fallback to H1
            h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = h1_match.group(1).strip() if h1_match else "No Title Found"
            
        # Construct a dummy URL (since we don't know the deployed URL yet easily)
        # Using filename as slug
        filename = os.path.basename(latest_file)
        slug = os.path.splitext(filename)[0]
        # Assuming typical GitHub Pages structure
        zenn_url = f"https://shironaganegi.github.io/ai-affiliate-bot-1/articles/{slug}/"
        
        x_post_text = f"【最新記事】{title}\n\nAIがトレンドを分析して自動執筆しました！\n詳細はこちら 👉 {zenn_url} #AI #Tech"
        
        send_discord_notification(webhook_url, title, zenn_url, x_post_text)
        
    except Exception as e:
        print(f"Failed to parse article or send notification: {e}")
        exit(1)

