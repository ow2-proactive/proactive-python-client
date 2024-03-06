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
    proactive_job.setJobName("ai_machine_learning_workflow")

    print("Getting the ai-machine-learning bucket")
    bucket = gateway.getBucket("ai-machine-learning")

    # ------------------------------------------------------------------------

    print("Creating the Load_Iris_Dataset task...")
    load_iris_dataset_task = bucket.create_Load_Iris_Dataset_task()
    proactive_job.addTask(load_iris_dataset_task)

    print("Creating the Split_Data task...")
    split_data_task = bucket.create_Split_Data_task()
    split_data_task.addDependency(load_iris_dataset_task)
    proactive_job.addTask(split_data_task)

    print("Creating the Logistic_Regression task...")
    logistic_regression_task = bucket.create_Logistic_Regression_task()
    proactive_job.addTask(logistic_regression_task)

    print("Creating the Train_Model task...")
    train_model_task = bucket.create_Train_Model_task()
    train_model_task.addDependency(split_data_task)
    train_model_task.addDependency(logistic_regression_task)
    proactive_job.addTask(train_model_task)

    print("Creating the Download_Model task...")
    download_model_task = bucket.create_Download_Model_task()
    download_model_task.addDependency(train_model_task)
    proactive_job.addTask(download_model_task)

    print("Creating the Predict_Model task...")
    predict_model_task = bucket.create_Predict_Model_task()
    predict_model_task.addDependency(split_data_task)
    predict_model_task.addDependency(train_model_task)
    proactive_job.addTask(predict_model_task)

    print("Creating the Preview_Results task...")
    preview_results_task = bucket.create_Preview_Results_task()
    preview_results_task.addDependency(predict_model_task)
    proactive_job.addTask(preview_results_task)

    # ------------------------------------------------------------------------

    # gateway.saveJob2XML(proactive_job, "ai-machine-learning-workflow.xml")
    # print("Job exported to XML")

    print("Submitting the job to the proactive scheduler...")
    job_id = gateway.submitJob(proactive_job)
    print("job_id: " + str(job_id))

    # print("Getting job output...")
    # job_output = gateway.printJobOutput(job_id)
    # print(job_output)

    # print("Getting job result...")
    # job_result = gateway.getJobResult(job_id)
    # print(job_result)

finally:
    print("Disconnecting")
    gateway.disconnect()
    print("Disconnected")
    gateway.terminate()
    print("Finished")
