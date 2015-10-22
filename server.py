import atexit
import os
from flask import Flask, jsonify, request, send_file
from model.UserParameters import UserParameters
from server.DefaultComputeManager import DefaultComputeManager
from server.DefaultWorkerManager import DefaultWorkerManager
from storage.KeyValueCache import KeyValueCache
from celery.task.control import discard_all


app = Flask(__name__)

db_name = "server.db"
swiftconfig = {'user': os.environ['OS_USERNAME'],
               'key': os.environ['OS_PASSWORD'],
               'tenant_name': os.environ['OS_TENANT_NAME'],
               'authurl': os.environ['OS_AUTH_URL']}
novaconfig = {'username': os.environ['OS_USERNAME'],
              'api_key': os.environ['OS_PASSWORD'],
              'project_id': os.environ['OS_TENANT_NAME'],
              'auth_url': os.environ['OS_AUTH_URL'],
              }

kv_storage = KeyValueCache(db_name)
comp_manager = DefaultComputeManager(kv_storage, swiftconfig)
worker_manager = DefaultWorkerManager(novaconfig)

@app.route('/interface', methods=['GET'])
def web_interface():
    return send_file("interface.html")

@app.route("/job", methods=['POST', 'GET'])
def create_job():
    user_params = UserParameters()
    user_params.naca4[0] = int(request.form["n0"])
    user_params.naca4[1] = int(request.form["n1"])
    user_params.naca4[2] = int(request.form["n2"])
    user_params.naca4[3] = int(request.form["n3"])
    user_params.min_angle = float(request.form["min_angle"])
    user_params.max_angle = float(request.form["max_angle"])
    user_params.step = float(request.form["step"])
    user_params.num_nodes = int(request.form["num_nodes"])
    user_params.refinement_level = int(request.form["refinement_level"])
    user_params.num_samples = int(request.form["num_samples"])
    user_params.viscosity = float(request.form["viscosity"])
    user_params.speed = float(request.form["speed"])
    user_params.time = float(request.form["time"])

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
