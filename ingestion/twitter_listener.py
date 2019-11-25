from tweepy import StreamListener, API


class TwitterListener(StreamListener):
    """
    Adaptor for Twitter stream
    """

    def __init__(self, callback):
        """
        Stores callback
        :param callback:
        """
        self.api = API()
        self.callback = callback

    def on_status(self, status):
        """
        Invokes callback when called
        :param status:
        :return:s
        """
        self.callback(status)
