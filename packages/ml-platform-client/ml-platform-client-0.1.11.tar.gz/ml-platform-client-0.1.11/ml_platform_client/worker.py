import logging
from multiprocessing import Process
from multiprocessing.connection import Connection

from .config import GlobalConfig, global_config


class Worker(Process):
    def __init__(self, pipe: Connection):
        super(Worker, self).__init__()
        self.pipe = pipe
        self.model_pool = {}
        self.alg_mapping = {}

    def run(self):
        try:
            while True:
                try:
                    command, data = self.pipe.recv()
                    if command == 'exit':
                        return
                    try:
                        result = self._process(command, data)
                    except Exception as e:
                        result = False, None
                        logging.error(e)

                    self.pipe.send(result)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    def _process(self, command, data):
        if command == 'load':
            return self._process_load(data)
        if command == 'unload':
            return self._process_unload(data)
        if command == 'predict':
            return self._process_predict(data)
        if command == 'init_alg':
            return self._process_init_alg(data)
        if command == 'init_config':
            return self._process_init_config(data)
        return False, None

    def _process_init_alg(self, data):
        self.alg_mapping.update(data)

    def _process_init_config(self, data: GlobalConfig):
        global_config.minio_host = data.minio_host
        global_config.minio_access_key = data.minio_access_key
        global_config.minio_secret_key = data.minio_secret_key
        global_config.minio_secure = data.minio_secure
        return True, None

    def _process_load(self, data):
        model_id = data['model_id']
        model_path = data['model_path']
        algorithm = data['algorithm']
        if algorithm not in self.alg_mapping:
            return False, None

        model = self.alg_mapping[algorithm].load(model_id, model_path)
        self.model_pool[model_id] = model
        return True, None

    def _process_unload(self, data):
        model_id = data['model_id']
        algorithm = data['algorithm']
        self.alg_mapping[algorithm].unload(model_id)
        del self.alg_mapping[algorithm]
        return True, None

    def _process_predict(self, data):
        model_id = data['model_id']
        features = data['features']
        if model_id not in self.model_pool:
            return False, 'model [{}] not loaded'.format(model_id)
        return True, self.model_pool[model_id].predict(features)
