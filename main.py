from flask import Flask, request, jsonify
from watson_developer_cloud import DiscoveryV1

from flask import Flask
application = Flask(__name__)


discovery = DiscoveryV1(
  username="f85b6942-7f92-413d-a5ee-ed4572f7a522",
  password="wXrInIO8KFoy",
  version="2016-12-01"
)

environment_id = 'fca8abb5-36d4-463f-b258-735436b8cba7'
collection_id = 'b192ab08-51d9-4ed0-9f4c-3002ad80493e'


@application.route('/search', methods=['POST'])
def search():
    data = request.get_json(force=True)
    q = data['q']
    context = data['context'] if 'context' in data else {}
    results = discovery.query(environment_id,
                              collection_id,
                              {'natural_language_query': q})
    return jsonify({
        'results': results['results'],
        'suggestions': ['farming', 'atmosphere', 'canada'],
        'new_context': {}
    })
