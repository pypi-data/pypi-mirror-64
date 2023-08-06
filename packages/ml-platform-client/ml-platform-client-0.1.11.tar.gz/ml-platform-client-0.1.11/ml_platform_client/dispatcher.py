import random
from collections import defaultdict
from multiprocessing import Pipe

from .algorithm_manager import alg_manager
from .service_response import success_response, success_response_with_data, format_service_response, error_response
from .server.util.api_util import catch_exception
from .server.validation.exceptions import ArgValueError
from .worker import Worker


class Dispatcher:
    def __init__(self):
        self.num_process = 1
        self.workers = []
        self.pipes = []
        self.load_info = defaultdict(set)
        self.all_loaded_models = set()
        self.model_mapping = defaultdict(list)
        for i in range(self.num_process):
            pipe1, pipe2 = Pipe(True)
            self.pipes.append(pipe1)
            worker = Worker(pipe2)
            self.workers.append(worker)
            worker.start()

    def get_load_info(self):
        result = {}
        for idx in self.load_info:
            models = []
            for each in self.load_info[idx]:
                models.append(each)
            result[idx] = models
        return format_service_response(success_response_with_data({'info': result}))

    def register(self, name, alg):
        alg_manager.register(name, alg)
        try:
            for pipe in self.pipes:
                pipe.send(('init_alg', alg_manager.alg_mapping))
                pipe.recv()
        except Exception as e:
            print(e)

    def set_config(self, config):
        try:
            for pipe in self.pipes:
                pipe.send(('init_config', config))
                pipe.recv()
        except Exception as e:
            print(e)

    @catch_exception
    def dispatch_predict(self, model_id, features):
        if model_id not in self.all_loaded_models:
            raise ArgValueError(message='model [{}] not loaded'.format(model_id))

        candidates = self.model_mapping[model_id]
        index = random.choice(candidates)

        self.pipes[index].send(('predict', {'model_id': model_id, 'features': features}))
        success, predictions = self.pipes[index].recv()

        if success:
            return format_service_response(success_response_with_data({'prediction': predictions}))
        else:
            return format_service_response(error_response())

    @catch_exception
    def dispatch_unload(self, model_id):
        if model_id not in self.all_loaded_models:
            return success_response()

        for index in self.load_info:
            load_set = self.load_info[index]
            if model_id in load_set:
                self.pipes[index].send(('unload', {'model_id': model_id}))
                success, _ = self.pipes[index].recv()
                if success:
                    load_set.remove(model_id)
                else:
                    return format_service_response(error_response())

        self.all_loaded_models.remove(model_id)
        self.model_mapping[model_id] = []
        return format_service_response(success_response())

    @catch_exception
    def dispatch_load(self, algorithm, model_id, model_path):
        if algorithm not in alg_manager.alg_mapping:
            raise ArgValueError(message='algorithm [{}] not support'.format(algorithm))

        if model_id in self.all_loaded_models:
            raise ArgValueError(message='model [{}] already loaded'.format(model_id))

        index = random.randint(0, self.num_process - 1)
        pipe = self.pipes[index]
        pipe.send(('load', {
            'model_id': model_id,
            'model_path': model_path,
            'algorithm': algorithm
        }))
        success, _ = pipe.recv()
        if success:
            self.all_loaded_models.add(model_id)
            self.load_info[index].add(model_id)
            self.model_mapping[model_id].append(index)
            return format_service_response(success_response())
        else:
            return format_service_response(error_response())


dispatcher = Dispatcher()


def register(name, alg):
    global dispatcher
    dispatcher.register(name, alg())


def set_config(config):
    global dispatcher
    dispatcher.set_config(config)
