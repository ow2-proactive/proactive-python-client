

class ProactiveJob:
  """
    Represent a generic proactive job

    job_name (string)
    job_tasks (list)
  """
  job_name = ''
  job_tasks = []

  input_folder = '.'
  output_folder = '.'

  def __init__(self):
    self.job_name = ''
    self.job_tasks = []

  def setJobName(self, job_name):
    self.job_name = job_name

  def getJobName(self):
    return self.job_name

  def addTask(self, task):
    self.job_tasks.append(task)

  def getTasks(self):
    return self.job_tasks

  def setInputFolder(self, input_folder):
    self.input_folder = input_folder

  def getInputFolder(self):
    return self.input_folder

  def setOutputFolder(self, output_folder):
    self.output_folder = output_folder

  def getOutputFolder(self):
    return self.output_folder

