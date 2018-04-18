# ProActive Scheduler Client

This module allows users to interact with a running ProActive Scheduler and Resource Manager.

### Usage

```
import proactive

print("Logging on proactive-server...")
proactive_host = 'try.activeeon.com'
proactive_port = '8080'
proactive_url  = "http://"+proactive_host+":"+proactive_port
print("Connecting on: " + proactive_url)
gateway = proactive.ProActiveGateway(proactive_url)

gateway.connect("bobot", "proactive")
print("Connected")

print("Creating a proactive python task...")
pythonTask = gateway.createPythonTask()
pythonTask.setTaskName("SimplePythonTask")
#pythonTask.setTaskImplementation("""print("Hello world!")""")
pythonTask.setTaskImplementationFromFile("scripts/print_python_env.py")
#pythonTask.setTaskImplementationFromLambdaFunction(lambda: 88 - 20 * 10)
#pythonTask.addGenericInformation("PYTHON_COMMAND", "/usr/bin/python3")

print("Add a fork environment to the python task")
fork_env = gateway.createDefaultForkEnvironment()
fork_env.setImplementationFromFile("scripts/fork_env.py")
pythonTask.setForkEnvironment(fork_env)

print("Add a selection script to the python task")
selection_script = gateway.createDefaultSelectionScript()
#selection_script.setImplementation("selected = True")
selection_script.setTaskImplementationFromFile("scripts/selection_script.py")
pythonTask.setSelectionScript(selection_script)

print("Creating a proactive job...")
myJob = gateway.createJob()
myJob.setJobName("SimplePythonJob")
myJob.addTask(pythonTask)

print("Submitting the job to the proactive scheduler...")
job_id = gateway.submitJob(myJob, True)
print("job_id: " + str(job_id))

## disconnect
print("Disconnecting")
gateway.disconnect()
print("Disconnected")
```
