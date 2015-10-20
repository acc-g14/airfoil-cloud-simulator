import atexit
from flask import Flask, jsonify, request, send_file
from model.UserParameters import UserParameters
from server.DefaultComputeManager import DefaultComputeManager
from server.DefaultWorkerManager import DefaultWorkerManager
from storage.KeyValueCache import KeyValueCache
from celery.task.control import discard_all


app = Flask(__name__)

kv_storage = KeyValueCache()
comp_manager = DefaultComputeManager(kv_storage)
worker_manager = DefaultWorkerManager()

@app.route('/interface', methods=['GET'])
def web_interface():
    return send_file("interface.html")

@app.route("/job", methods=['POST', 'GET'])
def create_job():
    user_params = UserParameters()
    print "a"
    user_params.naca4[0] = float(request.form["n0"])
    print "a"
    user_params.naca4[1] = float(request.form["n1"])
    print "a"
    user_params.naca4[2] = float(request.form["n2"])
    print "a"
    user_params.naca4[3] = float(request.form["n3"])
    print "a"
    user_params.min_angle = float(request.form["min_angle"])
    print "a"
    user_params.max_angle = float(request.form["max_angle"])
    print "a"
    user_params.step = float(request.form["step"])
    print "a"
    user_params.num_nodes = int(request.form["num_nodes"])
    user_params.refinement_level = int(request.form["refinement_level"])
    user_params.num_samples = int(request.form["num_samples"])
    user_params.viscosity = float(request.form["viscosity"])
    print "a"
    user_params.speed = float(request.form["speed"])
    user_params.time = float(request.form["time"])

    print "wullu"

    return jsonify({"job_id": comp_manager.start_computation(user_params)})


@app.route("/job/<job_id>", methods=['DELETE'])
def delete_job(job_id):
    comp_manager.stop_computation(job_id)
    return True


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
