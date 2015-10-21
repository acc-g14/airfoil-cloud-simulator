import atexit
from flask import Flask, jsonify
from model.UserParameters import UserParameters
from server.DefaultComputeManager import DefaultComputeManager
from server.DefaultWorkerManager import DefaultWorkerManager
from storage.KeyValueCache import KeyValueCache
from celery.task.control import discard_all


app = Flask(__name__)

kv_storage = KeyValueCache()
comp_manager = DefaultComputeManager(kv_storage)
worker_manager = DefaultWorkerManager()


@app.route("/job", methods=['POST', 'GET'])
def create_job():
    user_params = UserParameters()
    return jsonify({"job_id": comp_manager.start_computation(user_params)})


@app.route("/job/<job_id>", methods=['DELETE'])
def delete_job(job_id):
    comp_manager.stop_computation(job_id)
    return jsonify(True)


@app.route("/worker")
def create_worker():
    worker_manager.set_workers_available(1)


@app.route("/job/<job_id>/status")
def get_status(job_id):
    return jsonify(comp_manager.get_status(job_id))


@app.route("/job/<job_id>/result")
def get_result(job_id):
    return jsonify(comp_manager.get_result(job_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)


@atexit.register
def cleanup():
    discard_all()