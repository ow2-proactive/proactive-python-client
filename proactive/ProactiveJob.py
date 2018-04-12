

class ProactiveJob:
  """
    Represent a generic proactive job

    job_name (string)
    job_tasks (list)
  """
  job_name = ''
  job_tasks = []

  def __init__(self):
    pass

  def setJobName(self, job_name):
    self.job_name = job_name

  def getJobName(self):
    return self.job_name

  def addTask(self, task):
    self.job_tasks.append(task)

  def getTasks(self):
    return self.job_tasks