import logging.config
import logging

from flask_injector import FlaskInjector
from injector import inject

from flask import Flask, Blueprint, request, render_template
from flask_restplus import Api, Resource, fields

from queries.models import Query

logging.config.fileConfig('logging.conf')

from queries.search import SearchAdapter
from ingestion.twitter_ingestor import TwitterIngestor
from indexing.kafka_consumer import KafkaStatusConsumer
from ioc.modules import AppModule

logger = logging.getLogger(__name__)

api_v1 = Blueprint('api', __name__, url_prefix='/api')

app = Flask(__name__,
            static_folder='templates/public',
            template_folder="templates/static")

api = Api(api_v1,
          version='1.0',
          title='Heavy Hitters API',
          description='API for running Heavy Hitters for a real-time Twitter status update feed')

ns = api.namespace('heavyhitters', description='Heavy Hitters operations')

query_model = api.model('Query', {
    'term': fields.String(description='Search term'),
    'place': fields.String(description='Geographical places, i.e. CA, New-York, etc.'),
    'startTime': fields.String(description='Start time stamp in UTF'),
    'endTime': fields.String(description='End time stamp in UTF'),
    'k': fields.Integer(description='How many results to show?')
})


@ns.route('/ingestion/start')
class IngestionStarter(Resource):
    @inject
    def __init__(self, *args, twitter_ingestor: TwitterIngestor, **kwargs):
        self.twitter_ingestor = twitter_ingestor
        super().__init__(*args, **kwargs)

    @ns.doc(description='Starts Ingestion of Twitter data')
    def get(self):
        self.twitter_ingestor.start()
        return 'Ingestion Started'


@ns.route('/ingestion/stop')
class IngestionStopper(Resource):
    @inject
    def __init__(self, *args, twitter_ingestor: TwitterIngestor, **kwargs):
        self.twitter_ingestor = twitter_ingestor
        super().__init__(*args, **kwargs)

    @ns.doc(description='Stops Ingestion of Twitter data')
    def get(self):
        self.twitter_ingestor.stop()
        return 'Ingestion Stopped'


@ns.route('/indexing/start')
class IndexingStarter(Resource):
    @inject
    def __init__(self, *args, kafka_consumer: KafkaStatusConsumer, **kwargs):
        self.kafka_consumer = kafka_consumer
        super().__init__(*args, **kwargs)

    @ns.doc(description='Starts Indexing of Twitter data')
    def get(self):
        self.kafka_consumer.start()
        return 'Indexing Started'


@ns.route('/indexing/stop')
class IndexingStopper(Resource):
    @inject
    def __init__(self, *args, kafka_consumer: KafkaStatusConsumer, **kwargs):
        self.kafka_consumer = kafka_consumer
        super().__init__(*args, **kwargs)

    @ns.doc(description='Stops Indexing of Twitter data')
    def get(self):
        self.kafka_consumer.stop()
        return 'Indexing Stopped'


@ns.route('/search')
class Search(Resource):
    @inject
    def __init__(self, *args, search_adapter: SearchAdapter, **kwargs):
        self.search_adapter = search_adapter
        super().__init__(*args, **kwargs)

    @ns.doc(description='Runs a search query in ElasticSearch and returns the first page')
    @ns.expect(query_model)
    def post(self):
        json_data = request.json

        query = Query(json_data.get('term', None),
                      json_data.get('place', None),
                      json_data.get('startTime', None),
                      json_data.get('endTime', None),
                      json_data.get('k', 10))

        logger.info('Executing search query')
        hits = self.search_adapter.find(query)
        logger.info('Done executing search query')
        return hits


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.register_blueprint(api_v1)
    FlaskInjector(app=app, modules=[AppModule])
    app.run(debug=True, threaded=True)
