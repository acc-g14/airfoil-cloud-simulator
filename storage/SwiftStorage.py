from storage.Storage import Storage


class SwiftStorage(Storage):
    def save_result(self, model_params, compute_params, result):
        pass

    def get_result(self, model_params, compute_params):
        pass

    def has_result(self, model_params, compute_params):
        pass

    def generate_hash(self, model_params, compute_params):
        pass
