import flask
import json
import os
import requests

from kubernetes import client, config
from openshift.dynamic import DynamicClient


with open('/run/secrets/kubernetes.io/serviceaccount/namespace') as fd:
    namespace = fd.read()

app = flask.Flask(__name__)
config.load_incluster_config()
api = DynamicClient(client.ApiClient())


@app.route('/')
def index():
    return '''
    <ul>
    <li><a href="/v1">version 1 (using openshift module)</a></li>
    <li><a href="/v2">version 2 (doing it the hard way)</a></li>
    </ul>
    '''


@app.route('/v1')
def v1():
    podapi = api.resources.get(api_version='v1', kind='Pod')
    pods = podapi.get(namespace=namespace)
    return app.make_response((
        json.dumps(pods.to_dict(), indent=2),
        200,
        {'Content-type': 'application/json'}
    ))


@app.route('/v2')
def v2():
    with open('/run/secrets/kubernetes.io/serviceaccount/token') as fd:
        token = fd.read()

    sess = requests.Session()
    sess.headers['Authorization'] = f'bearer {token}'
    sess.verify = '/run/secrets/kubernetes.io/serviceaccount/ca.crt'

    url = os.environ['KUBERNETES_PORT'].replace('tcp://', 'https://')
    res = sess.get(f'{url}/api/v1/namespaces/{namespace}/pods')

    return app.make_response((
        json.dumps(res.json(), indent=2),
        200,
        {'Content-type': 'application/json'}
    ))

