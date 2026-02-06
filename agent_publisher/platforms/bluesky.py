from atproto import Client
from shared.config import config
from shared.utils import setup_logging

logger = setup_logging(__name__)

class BlueSkyPublisher:
    def __init__(self):
        self.handle = config.BLUESKY_HANDLE
        self.password = config.BLUESKY_PASSWORD

    def publish(self, title, zenn_url):
        if not self.handle or not self.password:
            logger.warning("BlueSky credentials missing. Skipping.")
            return

        try:
            client = Client()
            client.login(self.handle, self.password)
            text = f"📝 新しい記事を書きました！\n\n{title}\n\n#AI #Tech #Zenn\n{zenn_url}"
            client.send_post(text)
            logger.info("Successfully posted to BlueSky!")
        except Exception as e:
            logger.error(f"BlueSky Error: {e}")
