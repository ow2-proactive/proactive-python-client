![License BSD](https://img.shields.io/badge/License-BSD-blue.svg "License BSD")
![Python 3](https://img.shields.io/badge/Python-3-brightgreen.svg "Python 3")

# ProActive Scheduler Client

This module allows users to interact with a running ProActive Scheduler and Resource Manager.

### 1. Requirements
* Python 3

### 2. Installation
`pip install proactive --upgrade`

### 3. Usage

```
import os
import proactive

print("Logging on proactive-server...")
proactive_host = 'try.activeeon.com'
proactive_port = '8080'
proactive_url  = "http://"+proactive_host+":"+proactive_port
print("Connecting on: " + proactive_url)
javaopts=[]
# uncomment for detailed logs
# javaopts.append('-Dlog4j.configuration=file:'+os.path.join(os.getcwd(),'log4j.properties'))
gateway = proactive.ProActiveGateway(proactive_url, javaopts)

gateway.connect(username="", password="")  # put your login here!
assert gateway.isConnected() is True
print("Connected")

try:
  print("Creating a proactive task...")
  proactive_task = gateway.createPythonTask()
  proactive_task.setTaskName("SimplePythonTask")
  proactive_task.setTaskImplementationFromFile('main.py', ['param1', 'param2'])
  proactive_task.addInputFile('scripts/__init__.py')
  proactive_task.addInputFile('scripts/hello.py')

  print("Adding a fork environment to the proactive task...")
  proactive_fork_env = gateway.createDefaultForkEnvironment()
  proactive_fork_env.setImplementationFromFile("scripts/fork_env.py")
  proactive_task.setForkEnvironment(proactive_fork_env)

  print("Adding a selection script to the proactive task...")
  proactive_selection_script = gateway.createDefaultSelectionScript()
  proactive_selection_script.setImplementationFromFile("scripts/selection_script.py")
  proactive_task.setSelectionScript(proactive_selection_script)

  print("Creating a proactive job...")
  proactive_job = gateway.createJob()
  proactive_job.setJobName("SimpleJob")
  proactive_job.addTask(proactive_task)
  proactive_job.setInputFolder(os.getcwd())
  proactive_job.setOutputFolder(os.getcwd())

  print("Submitting the job to the proactive scheduler...")
  job_id = gateway.submitJob(proactive_job, debug=False)
  print("job_id: " + str(job_id))

  print("Getting job output...")
  job_result = gateway.getJobResult(job_id)
  print(job_result)

finally:
  print("Disconnecting")
  gateway.disconnect()
  print("Disconnected")
  gateway.terminate()
  print("Finished")
```

### 4. Examples

#### 4.1 Creating a Python task
```
...
my_task = gateway.createPythonTask()
my_task.setTaskName("SimplePythonTask")
my_task.setTaskImplementation("""print("Hello world!")""")

# or by
# my_task.setTaskImplementationFromFile("scripts/print_python_env.py")
# my_task.setTaskImplementationFromLambdaFunction(lambda: 88 - 20 * 10)

# add attached files
# my_task.addInputFile('scripts/hello.py')

# select your python version
# my_task.addGenericInformation("PYTHON_COMMAND", "/usr/bin/python3")
...
```

#### 4.2 Adding a fork environment
```
...
fork_env = gateway.createDefaultForkEnvironment()
fork_env.setImplementationFromFile("scripts/fork_env.py")

my_task.setForkEnvironment(fork_env)
...
```

#### 4.3 Adding a selection script
```
...
selection_script = gateway.createDefaultSelectionScript()
selection_script.setImplementationFromFile("scripts/selection_script.py")

my_task.setSelectionScript(selection_script)
...
```

#### 4.4 Create a job and add your task
```
...
my_job = gateway.createJob()
my_job.setJobName("SimpleJob")
my_job.addTask(my_task)

# for file transfer
# my_job.setInputFolder(os.getcwd())
# my_job.setOutputFolder(os.getcwd())
...
```

#### 4.5 Submit your job to the scheduler
```
...
job_id = gateway.submitJob(my_job, debug=False) # set debug=True for more debug info
...
```

#### 4.6 Get the job results
```
...
print("Getting job output...")
job_result = gateway.getJobResult(job_id)
print(job_result)
...
```