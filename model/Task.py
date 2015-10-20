class Task:
    def __init__(self, task_id=None, workertask=None, model_params=None, compute_params=None, result=None,
                 finished=False):
        self.id = task_id
        self.workertask = workertask
        self.model_params = model_params
        self.compute_params = compute_params
        self.result = result
        self.finished = finished