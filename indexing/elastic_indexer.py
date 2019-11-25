from elasticsearch import Elasticsearch
import logging

logger = logging.getLogger(__name__)


class ElasticIndexer:
    """Indexes documents via ElasticSearch"""

    def __init__(self, elastic_config, es=Elasticsearch()):
        """

        :param elastic_config: Dictionary containing `index` fields which is the name of index in ElasticSearch where
        documents will be indexed
        :param es: ElasticSearch instance
        """
        self.es_index = elastic_config['index']
        self.es = es
        logger.info('Initialized ElasticSearch indexer')

    def index(self, document):
        """
        Stores a document in an ElasticSearch index
        :param document: Document to be inserted
        :return: ElasticSearch response
        """

        # Create a document and index it in ElasticSearch
        response = self.es.index(index=self.es_index, doc_type='tweet', body=document.value, timeout='5m')
        logger.debug('Twitter status indexing response: %s', response)
        return response
