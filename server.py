from flask import Flask
from server.DefaultComputeManager import DefaultComputeManager
from server.DefaultWorkerManager import DefaultWorkerManager
from storage.KeyValueCache import KeyValueCache

app = Flask(__name__)

kv_storage = KeyValueCache()
comp_manager = DefaultComputeManager(kv_storage)
worker_manager = DefaultWorkerManager()


@app.route("/job", methods=['PUT'])
def create_job():
    pass


@app.route("/job/{id}", methods=['DELETE'])
def delete_job(id):
    pass


@app.route("/job/{id}/status")
def get_status(id):
    pass


@app.route("/job/{id}/result")
def get_result(id):
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
