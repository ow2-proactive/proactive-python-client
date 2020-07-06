

class ProactiveJob:
    """
      Represents a generic proactive job

      job_name (string)
      job_tasks (list)
      input_folder (string)
      output_folder (string)
    """

    def __init__(self):
        self.job_name = ''
        self.job_tasks = []
        self.generic_information = {}
        self.variables = {}
        self.input_folder = '.'
        self.output_folder = '.'

    def __str__(self):
        return self.getJobName()

    def __repr__(self):
        return self.getJobName()

    def setJobName(self, job_name):
        self.job_name = job_name

    def getJobName(self):
        return self.job_name

    def addTask(self, task):
        self.job_tasks.append(task)

    def removeTask(self, task):
        self.job_tasks.remove(task)

    def clearTasks(self):
        self.job_tasks.clear()

    def getTasks(self):
        return self.job_tasks

    def addVariable(self, key, value):
        self.variables[key] = value

    def getVariables(self):
        return self.variables

    def hasVariables(self):
        return True if self.variables else False

    def removeVariable(self, key):
        del self.variables[key]

    def clearVariables(self):
        self.variables.clear()

    def addGenericInformation(self, key, value):
        self.generic_information[key] = value

    def getGenericInformation(self):
        return self.generic_information

    def removeGenericInformation(self, key):
        del self.generic_information[key]

    def clearGenericInformation(self):
        self.generic_information.clear()

    def setInputFolder(self, input_folder):
        self.input_folder = input_folder

    def getInputFolder(self):
        return self.input_folder

    def setOutputFolder(self, output_folder):
        self.output_folder = output_folder

    def getOutputFolder(self):
        return self.output_folder

