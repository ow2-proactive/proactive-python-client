import os
import proactive
import getpass

from dotenv import load_dotenv
load_dotenv()

print("Logging on proactive-server...")
proactive_url = os.getenv("PROACTIVE_URL")
if not proactive_url:
    proactive_url = input("Server (default: https://try.activeeon.com:8443): ")
if proactive_url == "":
    proactive_url  = "https://try.activeeon.com:8443"
if not proactive_url.startswith("http"):
    proactive_url  = "https://"+proactive_url+".activeeon.com:8443"

print("Connecting on: " + proactive_url)
gateway = proactive.ProActiveGateway(base_url=proactive_url, debug=False, javaopts=[], log4j_props_file=None, log4py_props_file=None)

username = os.getenv("PROACTIVE_USERNAME")
password = os.getenv("PROACTIVE_PASSWORD")
if not (username and password):
    username = input("Login: ")
    password = getpass.getpass(prompt="Password: ")
gateway.connect(username, password)
assert gateway.isConnected() is True
print("Connected")

try:
    print("Creating a proactive job...")
    proactive_job = gateway.createJob()
    proactive_job.setJobName("SimpleJob")

    print("Creating a proactive task #1...")
    proactive_task_1 = gateway.createPythonTask()
    proactive_task_1.setTaskName("SimplePythonTask1")
    proactive_task_1.addVariable("TASK_ENABLED", "True")
    proactive_task_1.addVariable("INPUT_VARIABLES", "{}")
    proactive_task_1.addVariable("SCORING", "accuracy")
    proactive_task_1.setTaskImplementationFromURL(proactive_url + "/catalog/buckets/ai-machine-learning/resources/Logistic_Regression_Script/raw")
    proactive_task_1.addGenericInformation("PYTHON_COMMAND", "python3")

    print("Adding a fork environment to the proactive task #1...")
    proactive_task_1_fork_env = gateway.createForkEnvironment(language="groovy")
    proactive_task_1_fork_env.setImplementationFromURL(proactive_url + "/catalog/buckets/scripts/resources/fork_env_ai/raw")
    proactive_task_1.setForkEnvironment(proactive_task_1_fork_env)
    proactive_job.addVariable("CONTAINER_PLATFORM", "docker")

    print("Adding proactive tasks to the proactive job...")
    proactive_job.addTask(proactive_task_1)

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
