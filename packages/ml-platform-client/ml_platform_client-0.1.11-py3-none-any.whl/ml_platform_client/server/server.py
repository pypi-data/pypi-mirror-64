import inspect
import os
import sys

from flask import Flask
from flask_restful import Api

from .api.base import BaseApi

app = Flask(__name__)
api = Api(app)

for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj):
        if issubclass(obj, BaseApi) and hasattr(obj, 'api_url'):
            full_path = os.path.join(obj.api_base_url, obj.api_url)
            api.add_resource(obj, full_path)


def run_app(port, debug=True):
    global app
    app.run(port=port, debug=debug)
