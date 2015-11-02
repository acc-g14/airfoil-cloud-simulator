from multiprocessing import Process
import time
from ComputeManager import ComputeManager
from model.ComputeParameters import ComputeParameters
from model.Job import Job
from storage.SwiftStorage import SwiftStorage
from model.ModelParameters import ModelParameters
from model.Task import Task
from utils import server_ip, generate_hash
import workertasks
import uuid
import numpy
import json


class ComputationException(BaseException):
    pass


class DefaultComputeManager(ComputeManager):
    def __init__(self, worker_manager, storage, config):
        super(DefaultComputeManager, self).__init__(storage)
        self._worker_manager = worker_manager
        self._config = config
        self._jobs = {}
        swift = SwiftStorage(config.swift_config, config.container)
        for objectName in swift.get_entries():
            objectData = swift.get_result_hash(objectName)
            storage.save_result_hash(objectName, objectData)

    def stop_computation(self, job_id):
        job = self._jobs.get(job_id)
        if job is None:
            raise ComputationException("No valid key specified")
        for task in job.tasks:
            try:
                task.workertask.revoke()
            except Exception:
                pass
        self._jobs.pop(job_id)

    def get_status(self, job_id):
            job = self._jobs.get(job_id)
            if job is None:
                raise ComputationException("No valid key specified")

            tasks_ready = 0
            tasks_total = len(job.tasks)
            for task in job.tasks:
                if self._storage.has_result(task.model_params, task.compute_params):
                    tasks_ready += 1
            return {"tasks_ready": tasks_ready,
                    "tasks_total": tasks_total,
                    "finished": tasks_ready == tasks_total}

    def get_result(self, job_id):
            job = self._jobs.get(job_id)
            if job is None:
                raise ComputationException("No valid key specified")
            taskresults = []
            finished_tasks = 0
            total_tasks = len(job.tasks)
            last_finished_task = 0
            for task in job.tasks:
                if self._storage.has_result(task.model_params, task.compute_params):
                    result_row = self._storage.get_result(task.model_params, task.compute_params)
                    result = json.loads(result_row[0])
                    finished_tasks += 1
                    taskresults.append(result)
                    if result_row[1] is not None and result_row[2] is not None:
                        endtime = result_row[1] + result_row[2]
                        if endtime > last_finished_task:
                            last_finished_task = endtime
            if last_finished_task < job.starttime:
                runtime = 0.0
            else:
                runtime = last_finished_task - job.starttime
            return {"finished_tasks": finished_tasks,
                    "total_tasks": total_tasks,
                    "results": taskresults,
                    "runtime": runtime}

    def start_computation(self, user_params):
        """
        This method starts the computation with the defined parameters.

        :param model.UserParameters.UserParameters user_params: UserParameters
        :rtype : UUID
        """
        job_id = uuid.uuid4()
        tasks = self._convert_user_params_to_tasks(user_params, job_id)
        tasklist = []
        for task in tasks:
            # check
            self._start_task(task)
            tasklist.append(task)
        job = Job(job_id, tasklist, [], user_params, time.time())
        self._jobs[str(job_id)] = job
        # TODO: we don't want workers to be started here anymore
        #self._start_workers(job)
        return job_id

    def _start_task(self, task):
        hash_key = generate_hash(task.model_params, task.compute_params)
        if self._storage.has_result(task.model_params, task.compute_params):
            task.finished = True
            task.result = json.loads(self._storage.get_result(task.model_params, task.compute_params)[0])
        else:
            string = json.dumps(self._config.swift_config)
            while len(string) % 16 != 0:
                string += " "
            config = self._config.crypt_obj.encrypt(string)
            workertask = workertasks.simulate_airfoil.apply_async((task.model_params, task.compute_params,
                                                                   config, self._config.container),
                                                                  task_id=hash_key)
            self._storage.save_result(task.model_params, task.compute_params, None)
            task.workertask = workertask
            task.id = workertask.id

    @staticmethod
    def _convert_user_params_to_tasks(user_params, job):
        """

        :param model.UserParameters.UserParameters user_params: UserParameters
        :param uuid.UUID job: uuid.UUID
        :return: model.Task.Task[]
        """
        tasks = []
        compute_parameters = ComputeParameters(user_params.num_samples, user_params.viscosity, user_params.speed,
                                               user_params.time, server_ip())
        angles = numpy.arange(user_params.min_angle, user_params.max_angle, user_params.step)
        for angle in angles:
            model_parameters = ModelParameters(user_params.naca4, job, angle, user_params.num_nodes,
                                               user_params.refinement_level)
            task = Task(None, None, model_parameters, compute_parameters, None)
            tasks.append(task)
        model_parameters = ModelParameters(user_params.naca4, job, user_params.max_angle, user_params.num_nodes,
                                           user_params.refinement_level)
        task = Task(None, None, model_parameters, compute_parameters, None)
        tasks.append(task)
        return tasks

    def save_result(self, hash_key, result):
        self._storage.save_result_hash(hash_key, result)

    def _start_workers(self, job):
        num_not_finished = len([task for task in job.tasks if not task.finished])
        num_workers = self._worker_manager.get_number_of_workers()
        if num_not_finished > num_workers:
            self._worker_manager.set_workers_available(num_not_finished - num_workers)

    def get_jobs(self):
        return self._jobs
