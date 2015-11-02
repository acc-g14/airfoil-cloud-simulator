

class Job:
    def __init__(self, job_id=None, tasks=None, result=None, user_params=None, starttime=None):
        self.id = job_id
        self.tasks = tasks
        self.result = result
        self.user_params = user_params
        self.starttime = starttime
