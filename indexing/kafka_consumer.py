import json
import logging
import threading

from kafka import KafkaConsumer

logger = logging.getLogger(__name__)


class KafkaStatusConsumer:
    """
    Consumes documents from Kafka
    """

    def __init__(self, kafka_config, consume_callback):
        """

        :param kafka_config:
        :param consume_callback: Method that will be invoked when a new message is available in Kafka
        """
        self.topic = kafka_config['topic']
        self.consume_callback = consume_callback
        self.consumer = KafkaConsumer(bootstrap_servers=[kafka_config['bootstrap_server']],
                                      auto_offset_reset='earliest',
                                      value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                      consumer_timeout_ms=60000)
        self._stop_event = None
        logger.info('Initialized Kafka Status Consumer')

    def start(self):
        logger.info('Starting Kafka Status Consumer')
        if self._stop_event and not self._stop_event.is_set():
            logger.warning('Kafka Status Consumer is already running')
            return
        self.consumer_thread = threading.Thread(target=self.consume, args=())
        self.consumer_thread.daemon = True  # Daemonize thread
        self._stop_event = threading.Event()
        self.consumer_thread.start()
        logger.info('Started Kafka Status Consumer')

    def stop(self):
        logger.info('Stopping Kafka Status Consumer')
        if not self._stop_event or self._stop_event.is_set():
            logger.warning('Kafka Status Consumer is not running')
            return
        self._stop_event.set()
        self._stop_event.wait()
        logger.info('Stopped Kafka Status Consumer')

    def consume(self):
        """

        :return: Message/messages from Kafka to be processed
        """
        self.consumer.subscribe(self.topic)
        for message in self.consumer:
            if self._stop_event.is_set():
                return
            logger.debug('Consuming Kafka message: %s', message)
            self.consume_callback(message)

