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
gateway = proactive.ProActiveGateway(base_url=proactive_url)

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
    proactive_task_1.setTaskExecutionFromFile('demo_exec_file/main.py', ['param1', 'param2'])
    proactive_task_1.addInputFile('demo_exec_file/hellopkg/__init__.py')
    proactive_task_1.addInputFile('demo_exec_file/hellopkg/hello.py')
    proactive_task_1.addGenericInformation("PYTHON_COMMAND", "python3")

    print("Adding a pre-script to task #1...")
    pre_script = gateway.createPreScript(gateway.getProactiveScriptLanguage().linux_bash())
    pre_script.setImplementation("""echo "This is a pre-script"; pwd; ls -la;""")
    proactive_task_1.setPreScript(pre_script)

    print("Adding a post-script to task #1...")
    post_script = gateway.createPostScript(gateway.getProactiveScriptLanguage().linux_bash())
    post_script.setImplementation("""echo "This is a post-script"; pwd; ls -la;""")
    proactive_task_1.setPostScript(post_script)

    print("Adding proactive tasks to the proactive job...")
    proactive_job.addTask(proactive_task_1)

    print("Submitting the job to the proactive scheduler...")
    job_id = gateway.submitJobWithInputsAndOutputsPaths(proactive_job)
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
