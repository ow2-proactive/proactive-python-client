import os
import proactive
import getpass

print("Logging on proactive-server...")
proactive_host = 'try.activeeon.com'
proactive_port = '8443'
proactive_url  = "https://"+proactive_host+":"+proactive_port

print("Connecting on: " + proactive_url)
gateway = proactive.ProActiveGateway(base_url=proactive_url, debug=False, javaopts=[], log4j_props_file=None, log4py_props_file=None)

gateway.connect(username=input("Login: "), password=getpass.getpass(prompt="Password: "))
assert gateway.isConnected() is True
print("Connected")

try:
    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("SimpleJob")

    print("Creating a proactive task #1...")
    proactive_task_1 = gateway.createPythonTask()
    proactive_task_1.setTaskName("SimplePythonTask1")
    proactive_task_1.setTaskImplementation("""print("Hello from ", variables.get("PA_TASK_NAME"))""")
    proactive_task_1.addGenericInformation("PYTHON_COMMAND", "python3")

    print("Adding a fork environment to the proactive task #1...")
    proactive_task_1_fork_env = gateway.createForkEnvironment(language="groovy")
    proactive_task_1_fork_env.setImplementationFromFile("scripts/fork_env.groovy")
    proactive_task_1.setForkEnvironment(proactive_task_1_fork_env)
    proactive_job.addVariable("CONTAINER_PLATFORM", "docker")

    print("Adding a selection script to the proactive task #1...")
    proactive_task_1_selection_script = gateway.createSelectionScript(language="groovy")
    proactive_task_1_selection_script.setImplementationFromFile("scripts/check_node_source_name.groovy")
    proactive_task_1.setSelectionScript(proactive_task_1_selection_script)
    proactive_job.addVariable("NODE_SOURCE_NAME", "local")

    print("Creating a proactive task #2...")
    proactive_task_2 = gateway.createPythonTask()
    proactive_task_2.setTaskName("SimplePythonTask2")
    proactive_task_2.setTaskImplementation("""print("Hello from ", variables.get("PA_TASK_NAME"))""")
    proactive_task_2.addGenericInformation("PYTHON_COMMAND", "python3")
    proactive_task_2.addDependency(proactive_task_1)

    print("Adding proactive tasks to the proactive job...")
    proactive_job.addTask(proactive_task_1)
    proactive_job.addTask(proactive_task_2)

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
