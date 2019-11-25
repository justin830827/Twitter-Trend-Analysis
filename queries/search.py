from queries.models import Query
import findspark
import logging
from algorithms.bloomfilter import bloom_filter
from algorithms.countminsketch import CountMinSketch, topK
from queue import PriorityQueue
import json

logger = logging.getLogger(__name__)


class SearchAdapter:
    def __init__(self, elastic_config, es):
        self.es = es
        self.index = elastic_config['index']

        findspark.add_jars(elastic_config['es_hadoop_jar'])
        findspark.init()

        from pyspark import SparkContext
        self.sc = SparkContext(appName="adbi-top-k")

    def to_elasticsearch_query(self, query: Query):
        clauses = []

        logger.info('Converting query %s' % vars(query))

        if query.term:
            clauses.append({"match": {"text": query.term}})

        if query.place:
            clauses.append({"match": {"place": query.place}})

        if query.start_time and query.end_time:
            clauses.append({"range": {
                "created_at": {
                    "gte": query.start_time,
                    "lte": query.end_time
                }
            }})

        return {"query": {"bool": {"must": clauses}}}

    def find(self, query: Query):
        q_str = self.to_elasticsearch_query(query)
        print(q_str)
        es_read_conf = {
            "es.resource": "{0}/tweet".format(self.index),
            "es.query": json.dumps(q_str)
        }

        es_rdd = self.sc.newAPIHadoopRDD(
            inputFormatClass="org.elasticsearch.hadoop.mr.EsInputFormat",
            keyClass="org.apache.hadoop.io.NullWritable",
            valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
            conf=es_read_conf)

        top_k = []

        if es_rdd.isEmpty():
            return top_k

        tweets = es_rdd.map(lambda doc: doc[1]['text'])

        tweets = tweets.map(bloom_filter)

        words_df = tweets.flatMap(lambda line: line)

        # build a count min sketch table for every partition and combine them into one CMS
        cms_merged = words_df.aggregate(CountMinSketch(22000, 200),
                                        lambda cms, word: cms.add(word),
                                        lambda cms1, cms2: cms1.merge(cms2))
        words = words_df.distinct().collect()

        queue = PriorityQueue()
        for word in words:
            queue = topK(word, cms_merged, queue, query.k)

        while not queue.empty():
            top = queue.get()
            top_k.append({'word': top.value, 'count': top.count})

        return top_k
