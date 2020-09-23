![License BSD](https://img.shields.io/badge/License-BSD-blue.svg "License BSD")
![Python 3](https://img.shields.io/badge/Python-3-brightgreen.svg "Python 3")
![Proactive](https://img.shields.io/pypi/v/proactive.svg "Proactive")
[![Documentation Status](https://readthedocs.org/projects/proactive-python-client/badge/?version=latest)](https://proactive-python-client.readthedocs.io/en/latest/?badge=latest)

# ProActive Python Client

This module allows users to interact with a running ProActive Scheduler and Resource Manager.

NOTE: To know how to use the Proactive Python Client in a more advanced way, please follow the link to see our [documentation](https://proactive-python-client.readthedocs.io/en/latest/).

### 1. Requirements
* Python 2 and 3

### 2. Installation
`pip install proactive --upgrade`

### 3. How to build
Just run `gradlew clean build`

This will generate the `proactive-XXX.zip` file inside project's `dist` folder.

Run `pip install dist/proactive-XXX.zip` to install the package in your python environment.

### 4. Build and run tests
`./gradlew clean build -Pproactive_url=XXX -Pusername=XXX -Ppassword=XXX`

Replace `XXX` with the respective information.

### 5. Usage

```
import os
import getpass
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
# Or uncomment the following line to protect your password
# gateway.connect(username="", password=getpass.getpass(prompt='Password: '))
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

### 6. Examples

#### 6.1 Creating a Python task
```
...
proactive_task = gateway.createPythonTask()
proactive_task.setTaskName("SimplePythonTask")
proactive_task.setTaskImplementation("""print("Hello world!")""")

# or by
# proactive_task.setTaskImplementationFromFile("scripts/print_python_env.py")
# proactive_task.setTaskImplementationFromLambdaFunction(lambda: 88 - 20 * 10)

# add attached files
# proactive_task.addInputFile('scripts/hello.py')

# select your python version
# proactive_task.addGenericInformation("PYTHON_COMMAND", "/usr/bin/python3")
...
```

#### 6.2 Adding a fork environment
```
...
fork_env = gateway.createDefaultForkEnvironment()
fork_env.setImplementationFromFile("scripts/fork_env.py")

proactive_task.setForkEnvironment(fork_env)
...
```

#### 6.3 Adding a selection script
```
...
selection_script = gateway.createDefaultSelectionScript()
selection_script.setImplementationFromFile("scripts/selection_script.py")

proactive_task.setSelectionScript(selection_script)
...
```

#### 6.4 Create a job and add your task
```
...
proactive_job = gateway.createJob()
proactive_job.setJobName("SimpleJob")
proactive_job.addTask(proactive_task)

# for file transfer
# proactive_job.setInputFolder(os.getcwd())
# proactive_job.setOutputFolder(os.getcwd())
...
```

#### 6.5 Submit your job to the scheduler
```
...
job_id = gateway.submitJob(proactive_job, debug=False) # set debug=True for more debug info
...
```

#### 6.6 Get the job results
```
...
print("Getting job output...")
job_result = gateway.getJobResult(job_id)
print(job_result)
...
```
