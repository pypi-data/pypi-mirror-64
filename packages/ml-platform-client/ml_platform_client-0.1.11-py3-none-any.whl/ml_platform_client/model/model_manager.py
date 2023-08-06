from service_response import success_response, success_response_with_data, format_service_response
from server.util.api_util import catch_exception
from server.validation.exceptions import ArgValueError


class ModelManager:
    model_pool = {}

    def load(self, model_id, model):
        self.model_pool[model_id] = model

    @catch_exception
    def predict(self, model_id, features):
        if model_id not in self.model_pool:
            raise ArgValueError(message='model [{}] not loaded'.format(model_id))

        model = self.model_pool[model_id]
        predict = model.predict(features)
        return format_service_response(success_response_with_data({'prediction': predict}))

    @catch_exception
    def unload(self, model_id):
        if model_id in self.model_pool:
            del self.model_pool[model_id]
        return format_service_response(success_response())


model_manager = ModelManager()
