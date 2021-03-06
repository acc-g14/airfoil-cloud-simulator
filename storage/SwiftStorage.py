from storage.Storage import Storage
from utils import generate_hash
import swiftclient.client
import json


class SwiftStorage(Storage):

    def __init__(self, config, container):
        self.connection = swiftclient.client.Connection(auth_version=2, **config)
        self._container = container

    def save_result_hash(self, hash_key, result):
        j_result = json.dumps(result)
        self.connection.put_object(self._container, hash_key, j_result)

    def save_result(self, model_params, compute_params, result):
        self.save_result_hash(
            generate_hash(model_params, compute_params),
            result)
        
    def get_result_hash(self, hash_key):
        response, object_content = self.connection.get_object(self._container, hash_key)
        return object_content
                          
    def get_result(self, model_params, compute_params):
        if self.has_result(model_params, compute_params):
            hash_key = generate_hash(model_params, compute_params)
            return self.get_result_hash(hash_key)

    def has_result(self, model_params, compute_params):
        response, objects = self.connection.get_container(self._container)
        objects = map(lambda x: x["name"], objects)
        hash_key = generate_hash(model_params, compute_params)
        return hash_key in objects

    def generate_hash(self, model_params, compute_params):
        return generate_hash(model_params, compute_params)

    def get_entries(self):
        response, objects = self.connection.get_container(self._container)
        return map(lambda x: x["name"], objects)

    def clear(self):
        for o in self.get_entries():
            self.connection.delete_object(self._container, o)
