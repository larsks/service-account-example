import flask
import requests
import yaml

from kubernetes import client, config
from openshift.dynamic import DynamicClient


with open('/run/secrets/kubernetes.io/serviceaccount/token') as fd:
    token = fd.read()

with open('/run/secrets/kubernetes.io/serviceaccount/namespace') as fd:
    namespace = fd.read()

app = flask.Flask(__name__)
config.load_incluster_config()
api = DynamicClient(client.ApiClient())

sess = requests.Session()
sess.headers['Authorization'] = f'bearer {token}'
sess.verify = '/run/secrets/kubernetes.io/serviceaccount/ca.crt'


@app.route('/')
def index():
    return '''
    <ul>
    <li><a href="/v1">version 1 (using openshift module)</a></li>
    <li><a href="/v2">version 2 (doing it the hard way)</a></li>
    </ul>
    <p>See the code for these examples <a href="https://github.com/larsks/service-account-example">here</a>.</p>
    '''


def filter_managed_fields(data):
    for item in data['items']:
        del item['metadata']['managedFields']


@app.route('/v1')
def v1():
    podapi = api.resources.get(api_version='v1', kind='Pod')
    pods = podapi.get(namespace=namespace)
    data = pods.to_dict()

    filter_managed_fields(data)

    return app.make_response((
        yaml.safe_dump(data, default_flow_style=False),
        200,
        {'Content-type': 'text/plain'}
    ))


@app.route('/v2')
def v2():
    url = 'https://kubernetes.default.svc'
    res = sess.get(f'{url}/api/v1/namespaces/{namespace}/pods')
    data = res.json()

    filter_managed_fields(data)

    return app.make_response((
        yaml.safe_dump(data, default_flow_style=False),
        200,
        {'Content-type': 'text/plain'}
    ))
