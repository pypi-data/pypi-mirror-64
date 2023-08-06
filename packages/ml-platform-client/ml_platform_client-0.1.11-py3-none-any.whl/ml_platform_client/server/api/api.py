import algorithm_manager
from .. import dispatcher
from ..util.api_util import arg_parse_validation, adapt_to_http_response
from .base import BaseApi
from .setup import *


class TrainApi(BaseApi):
    api_url = 'train'

    @arg_parse_validation(arg_setup=train_arg_setup, validate_setup=train_validate_setup)
    @adapt_to_http_response
    def post(self, args):
        return algorithm_manager.alg_manager.train(args['algorithm'], args['model_path'], args['data'],
                                                   args['parameters'], args['extend'])


class PredictApi(BaseApi):
    api_url = 'predict'

    @arg_parse_validation(arg_setup=predict_arg_setup, validate_setup=predict_validate_setup)
    @adapt_to_http_response
    def post(self, args):
        return dispatcher.predict(args['model_id'], args['features'])


class LoadApi(BaseApi):
    api_url = 'load'

    @arg_parse_validation(arg_setup=load_arg_setup, validate_setup=load_validate_setup)
    @adapt_to_http_response
    def post(self, args):
        return dispatcher.load(args['algorithm'], args['model_id'], args['model_path'])


class UnloadApi(BaseApi):
    api_url = 'unload'

    @arg_parse_validation(arg_setup=unload_arg_setup, validate_setup=unload_validate_setup)
    @adapt_to_http_response
    def post(self, args):
        return dispatcher.unload(args['model_id'])


class MonitorApi(BaseApi):
    api_url = 'monitor'

    @arg_parse_validation()
    @adapt_to_http_response
    def get(self, args):
        return dispatcher.get_load_info()
