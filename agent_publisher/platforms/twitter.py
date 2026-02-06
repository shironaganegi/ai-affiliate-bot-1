import tweepy
from shared.config import config
from shared.utils import setup_logging

logger = setup_logging(__name__)

class TwitterPublisher:
    def __init__(self):
        self.client = None
        if all([config.X_API_KEY, config.X_API_SECRET, config.X_ACCESS_TOKEN, config.X_ACCESS_SECRET]):
             self.client = tweepy.Client(
                consumer_key=config.X_API_KEY,
                consumer_secret=config.X_API_SECRET,
                access_token=config.X_ACCESS_TOKEN,
                access_token_secret=config.X_ACCESS_SECRET
            )
        else:
             logger.warning("X API credentials are missing.")

    def publish(self, custom_text=None, article_url=None):
        if not self.client:
            logger.warning("Skipping X post due to missing credentials.")
            return

        if custom_text:
            post_text = custom_text
            if article_url and article_url not in post_text:
                 post_text += f"\n\n{article_url}"
        else:
            post_text = f"🤖 今日のAIトレンド情報をお届け！\n\n詳細はZennブログで公開予定です！\n\n#AI #Tech\n{article_url or ''}"

        try:
            logger.info(f"Posting to X: {post_text[:30]}...")
            response = self.client.create_tweet(text=post_text)
            logger.info(f"Successfully posted to X! ID: {response.data['id']}")
        except Exception as e:
            logger.error(f"Failed to post to X: {e}")
