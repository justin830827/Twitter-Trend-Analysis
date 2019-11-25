import logging
from tweepy import OAuthHandler, Stream
from ingestion.twitter_listener import TwitterListener

logger = logging.getLogger(__name__)


class TwitterIngestor():
    """
    Ingests data from Twitter
    """

    def __init__(self, twitter_config, callback):
        """
        Creates an OAuth handler and a Twitter stream
        :param twitter_config:
        :param callback:
        """
        self.callback = callback
        self.auth = OAuthHandler(twitter_config['customer_key'], twitter_config['customer_secret'])
        self.auth.set_access_token(twitter_config['access_token'], twitter_config['access_secret'])
        self.twitter_stream = Stream(self.auth, TwitterListener(self.callback))
        logger.info('Initialized Twitter Ingestor')

    def start(self):
        """
        Starts Twitter streaming
        :return:
        """
        logger.info('Starting Twitter feed ingestion')
        self.twitter_stream.sample(is_async=True, languages=['en'])
        logger.info('Started Twitter feed ingestion')

    def stop(self):
        """
        Requests Twitter stream to start receiving messages
        :return:
        """
        logger.info('Stopping Twitter feed ingestion')
        self.twitter_stream.disconnect()
        logger.info('Stopped Twitter feed ingestion')
