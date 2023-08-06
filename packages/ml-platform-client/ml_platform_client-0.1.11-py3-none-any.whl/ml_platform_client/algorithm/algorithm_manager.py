import logging
import threading

from ..data.service_response import success_response_with_data, format_service_response
from ..server.util.api_util import catch_exception
from ..server.validation.exceptions import ArgValueError


class AlgorithmManager:
    alg_mapping = {}

    def register(self, name, algorithm):
        self.alg_mapping[name] = algorithm

    @catch_exception
    def train(self, algorithm, model_path, data_config, parameters, extend):
        if algorithm not in self.alg_mapping:
            raise ArgValueError(message='algorithm [{}] not support'.format(algorithm))

        model_id = self.alg_mapping[algorithm].generate_model_id()
        threading.Thread(target=self._train_async,
                         args=(algorithm, model_id, model_path, data_config, parameters, extend)).start()

        return format_service_response(success_response_with_data({'model_id': model_id}))

    def _train_async(self, algorithm, model_id, model_path, data_config, parameters, extend):
        try:
            result = self.alg_mapping[algorithm].train(model_id, model_path, data_config, parameters, extend)
            self._train_call_back(model_id, result)
            logging.info('train model [{}] success'.format(model_id))
        except Exception as e:
            logging.error(e)
            logging.error('train model [{}] failed'.format(model_id))

    def _train_call_back(self, model_id, success):
        pass


alg_manager = AlgorithmManager()
