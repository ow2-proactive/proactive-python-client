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
redirectJVMOutput=False
gateway = proactive.ProActiveGateway(proactive_url, javaopts, redirectJVMOutput)

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
