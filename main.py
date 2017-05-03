from flask import Flask, request, jsonify
from watson_developer_cloud import DiscoveryV1

application = Flask(__name__)


discovery = DiscoveryV1(
  username="f85b6942-7f92-413d-a5ee-ed4572f7a522",
  password="wXrInIO8KFoy",
  version="2016-12-01"
)

environment_id = 'fca8abb5-36d4-463f-b258-735436b8cba7'
collection_id = 'b192ab08-51d9-4ed0-9f4c-3002ad80493e'

levels = ['Category', 'Term', 'Topic',
          'VariableLevel1', 'VariableLevel2', 'VariableLevel3']


@application.route('/search', methods=['POST'])
def search():
    """Search and suggest filters for datasets."""
    data = request.get_json(force=True)
    q = data['q']
    context = data['context'] if 'context' in data else {}
    if 'q' not in context:
        context['q'] = q
        context['filters'] = {}
        depth = 0
    else:
        depth = len(context['filters'])
        context['filters'][levels[depth]] = q
        depth += 1
    qfilter = ','.join(['umm.ScienceKeywords.%s:%s' % (k, v)
                        for k, v in context['filters'].iteritems()])
    qaggr = 'term(umm.ScienceKeywords.%s)' % levels[depth]
    response = discovery.query(environment_id,
                               collection_id,
                               {
                                   'query': context['q'],
                                   'aggregation': qaggr,
                                   'filter': qfilter
                               })

    suggestions = [x['key'] for x in response['aggregations'][0]['results']]
    return jsonify({
        'matching_results': response['matching_results'],
        'results': response['results'],
        'suggestions': suggestions,
        'new_context': context
    })
