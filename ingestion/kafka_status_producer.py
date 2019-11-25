from kafka import KafkaProducer
from converters.status_converter import StatusConverter


class KafkaStatusProducer:
    """
    Produces messages to a Kafka topic
    """

    def __init__(self, kafka_config):
        self.topic = kafka_config['topic']
        self.producer = KafkaProducer(bootstrap_servers=[kafka_config['bootstrap_server']],
                                      value_serializer=StatusConverter.to_json)

    def produce(self, message):
        """
        Produces a message to Kafka
        :param message:
        :return:
        """
        self.producer.send(self.topic, message)
