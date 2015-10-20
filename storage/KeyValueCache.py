from Storage import Storage


class KeyValueCache(Storage):
    def has_result(self, model_params, compute_params):
        pass

    def get_result(self, model_params, compute_params):
        pass

    def save_result(self, model_params, compute_params, result):
        pass

    def generate_hash(self, model_params, compute_params):
        pass
