from ComputeManager import ComputeManager
import uuid
import numpy
from model.ComputeParameters import ComputeParameters
from model.Job import Job
from model.ModelParameters import ModelParameters
from model.Task import Task
import workertasks


class ComputationException(BaseException):
    pass


class DefaultComputeManager(ComputeManager):
    def __init__(self, storage):
        super(DefaultComputeManager, self).__init__(storage)
        self._jobs = {}

    def stop_computation(self, job_id):
        job = self._jobs.get(job_id)
        if job is None:
            raise ComputationException("No valid key specified")
        for task in job.tasks:
            task.workertask.revoke()
        pass

    def get_status(self, job_id):
            job = self._jobs.get(job_id)

            if job is None:
                raise ComputationException("No valid key specified")

            tasks_ready = 0
            tasks_total = len(job.tasks)
            for task in job.tasks:
                if task.finished:
                    tasks_ready += 1
                elif task.workertask.ready():
                    task.result = task.workertask.result
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
            for task in job.tasks:
                if task.finished:
                    # result already associated with task
                    taskresults.append(task.result)
                    finished_tasks += 1
                elif task.workertask.ready():
                    task.finished = True
                    task.result = task.workertask.result
                    taskresults.append(task.result)
                    finished_tasks += 1

            return {"finished_tasks": finished_tasks,
                    "total_tasks": total_tasks,
                    "results": taskresults}

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
            print task
            workertask = workertasks.simulate_airfoil.delay(task.model_params, task.compute_params)
            task.workertask = workertask
            task.id = workertask.id
            tasklist.append(task)
        self._jobs[str(job_id)] = Job(job_id, tasklist)
        return job_id

    @staticmethod
    def _convert_user_params_to_tasks(user_params, job):
        """

        :param model.UserParameters.UserParameters user_params: UserParameters
        :param uuid.UUID job: uuid.UUID
        :return: model.Task.Task[]
        """
        tasks = []
        compute_parameters = ComputeParameters(user_params.num_samples, user_params.viscosity, user_params.speed,
                                               user_params.time)
        angles = numpy.arange(user_params.minAngle, user_params.maxAngle, user_params.step)
        for angle in angles:
            model_parameters = ModelParameters(user_params.naca4, job, angle, user_params.numNodes,
                                               user_params.refinementLevel)
            task = Task(None, None, model_parameters, compute_parameters, None)
            tasks.append(task)
        return tasks
