import atexit
from multiprocessing import Process
from celery import Celery
from flask import Flask, jsonify, request, send_file
import time
from model.UserParameters import UserParameters
from server.DefaultComputeManager import DefaultComputeManager
from server.DefaultWorkerManager import DefaultWorkerManager
from storage.KeyValueCache import KeyValueCache
from celery.task.control import discard_all
from model.Config import Config
from utils import DBUtil

app = Flask(__name__)


config = Config()
kv_storage = KeyValueCache(config.db_name)
worker_manager = DefaultWorkerManager(config, config.db_name)
comp_manager = DefaultComputeManager(worker_manager,kv_storage, config)


def background_monitor(app):
    state = app.events.State()

    def announce_failed_tasks(event):
        state.event(event)
        # task name is sent only with -received event, and state
        # will keep track of this for us.
        task = state.tasks.get(event['uuid'])

        print('TASK FAILED: %s[%s] %s' % (
            task.name, task.uuid, task.info(), ))

    def announce_event(event):
        print "ABC"
    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
                'task-failed': announce_failed_tasks,
                '*': announce_event,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)



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


@app.route("/worker/<int:num_workers>")
def create_worker(num_workers):
    worker_manager.set_workers_available(num_workers)


@app.route("/job/<job_id>/status")
def get_status(job_id):
    return jsonify(comp_manager.get_status(job_id))


@app.route("/save_result/<hash_key>", methods=["POST"])
def save_result(hash_key):
    result = request.form['result']
    comp_manager.save_result(hash_key, result)
    return "asdsa"


@app.route("/job/<job_id>/result")
def get_result(job_id):
    return jsonify(comp_manager.get_result(job_id))
if __name__ == '__main__':
    worker_manager.load_workers()
    c = Celery(broker=config.broker, backend=config.backend)
    p = Process(target=background_monitor, args=(c,))
    p.start()
    app.run(host='0.0.0.0', debug=True, port=5000)


@atexit.register
def cleanup():
    worker_manager.save_ids()
    discard_all()
