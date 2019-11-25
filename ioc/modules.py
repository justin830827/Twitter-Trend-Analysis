from injector import Module, singleton, provider

from indexing.kafka_consumer import KafkaStatusConsumer
from indexing.elastic_indexer import ElasticIndexer

from configparser import ConfigParser
from elasticsearch import Elasticsearch

from ingestion.kafka_status_producer import KafkaStatusProducer
from ingestion.twitter_ingestor import TwitterIngestor

from queries.search import SearchAdapter


class AppModule(Module):
    def configure(self, binder):
        self.config_parser = ConfigParser()
        self.config_parser.read('config.ini')

        binder.bind(
            TwitterIngestor,
            to=self.get_twitter_ingestor,
            scope=singleton,
        )

        binder.bind(
            KafkaStatusProducer,
            to=KafkaStatusProducer(self.config_parser['kafka']),
            scope=singleton
        )

        binder.bind(
            Elasticsearch,
            to=Elasticsearch(timeout=60, max_retries=10, retry_on_timeout=True),
            scope=singleton
        )

        binder.bind(
            ElasticIndexer,
            to=self.get_elastic_indexer,
            scope=singleton
        )

        binder.bind(
            ElasticIndexer,
            to=self.get_elastic_indexer,
            scope=singleton
        )

        binder.bind(
            KafkaStatusConsumer,
            to=self.get_kafka_status_consumer,
            scope=singleton
        )

        binder.bind(SearchAdapter, to=self.get_search_adapter, scope=singleton)

    @provider
    def get_twitter_ingestor(self, kafka_producer: KafkaStatusProducer) -> TwitterIngestor:
        return TwitterIngestor(self.config_parser['twitter'], kafka_producer.produce)

    @provider
    def get_elastic_indexer(self, es: Elasticsearch) -> ElasticIndexer:
        return ElasticIndexer(self.config_parser['elastic'], es)

    @provider
    def get_kafka_status_consumer(self, elastic_indexer: ElasticIndexer) -> KafkaStatusConsumer:
        return KafkaStatusConsumer(self.config_parser['kafka'], elastic_indexer.index)

    @provider
    def get_search_adapter(self, es: Elasticsearch) -> SearchAdapter:
        return SearchAdapter(self.config_parser['elastic'], es)
