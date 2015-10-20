from ComputeManager import ComputeManager
import uuid
import numpy
from model.ComputeParameters import ComputeParameters
from model.Job import Job
from model.ModelParameters import ModelParameters
import workertasks


class ComputationException(BaseException):
    pass


class DefaultComputeManager(ComputeManager):
    def __init__(self, storage):
        super(DefaultComputeManager, self).__init__(storage)
        self._jobs = {}

    def stop_computation(self, job_id):
        try:
            job = self._jobs.get(job_id)
        except KeyError:
            raise ComputationException("No valid key specified")
        # TODO
        pass

    def get_status(self, job_id):
        try:
            job = self._jobs.get(job_id)
            for task in job.tasks:
                if task['task'].ready():
                    print task['task'].result
                else:
                    print "task not ready"
        except KeyError:
            raise ComputationException("No valid key specified")
        # TODO
        pass

    def get_result(self, job_id):
        try:
            job = self._jobs.get(job_id)
        except KeyError:
            raise ComputationException("No valid key specified")
        # TODO
        pass

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
            workertask = workertasks.simulate_airfoil.delay(task["model_parameters"], task["compute_parameters"])
            tasklist.append({"task": workertask, "result": None})
        self._jobs[str(job_id)] = Job(job_id, tasklist)
        return job_id

    @staticmethod
    def _convert_user_params_to_tasks(user_params, job):
        """

        :param model.UserParameters.UserParameters user_params: UserParameters
        :param uuid.UUID job: uuid.UUID
        :return:
        """
        tasks = []
        compute_parameters = ComputeParameters(user_params.num_samples, user_params.viscosity, user_params.speed,
                                               user_params.time)
        angles = numpy.arange(user_params.minAngle, user_params.maxAngle, user_params.step)
        for angle in angles:
            model_parameters = ModelParameters(user_params.naca4, job, angle, user_params.numNodes,
                                               user_params.refinementLevel)
            tasks.append({"model_parameters": model_parameters, "compute_parameters": compute_parameters})
        return tasks
