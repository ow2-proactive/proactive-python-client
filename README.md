# ProActive Python Client / SDK

![License BSD](https://img.shields.io/badge/License-BSD-blue.svg "License BSD")
![Python 3](https://img.shields.io/badge/Python-3-brightgreen.svg "Python 3")
![Proactive](https://img.shields.io/pypi/v/proactive.svg "Proactive")
[![Documentation Status](https://readthedocs.org/projects/proactive-python-client/badge/?version=latest)](https://proactive-python-client.readthedocs.io/en/latest/?badge=latest)

The ProActive Python Client (or Proactive Python SDK) enables seamless interaction with the ProActive Scheduler and Resource Manager, facilitating the automation of workflow submission and management tasks directly from Python.

## Key Features

- **Ease of Use**: Simple API for interacting with the ProActive Scheduler.
- **Workflow Management**: Submit, monitor, and manage your ProActive workflows.
- **Resource Management**: Leverage the Resource Manager for efficient computing resource allocation.

## Getting Started

### Prerequisites

- Python version 3.5 or later is required.
- Java 8 SDK.

Notes:

- If you want to build the package using the Java 11 SDK, you need to clone the git branch `gradle-5.1.1`
- Java 17+ is not supported.

### Installation

You can easily install the ProActive Python Client using pip:

```bash
pip install --upgrade proactive
```

For access to the latest features and improvements, install the pre-release version:

```bash
pip install --upgrade --pre proactive
```

### Building from Source

#### Linux or Mac

To build and install the package from source:

```bash
# Build the package
make clean_build
# or use gradlew
gradlew clean build

# Install the built package
pip install dist/proactive-XXX.zip  # Replace XXX with the actual version
```

#### Windows

```bat
REM Build the package
build.bat CLEAN_BUILD

REM Install the built package
REM Replace XXX with the actual version
pip install dist\proactive-XXX.zip
```

### Running Tests

#### With Gradle

Specify your ProActive credentials and run the tests:

```bash
./gradlew clean build -Pproactive_url=YOUR_URL -Pusername=YOUR_USERNAME -Ppassword=YOUR_PASSWORD
```

#### With Make

First, create a `.env` file with your ProActive credentials:

```ini
PROACTIVE_URL=YOUR_URL
PROACTIVE_USERNAME=YOUR_USERNAME
PROACTIVE_PASSWORD=YOUR_PASSWORD
```

Then execute:

```bash
make test
```

## Quickstart Example

This simple example demonstrates connecting to a ProActive server, creating a job, adding a Python task, and submitting the job:

```python
import getpass
from proactive import ProActiveGateway

proactive_url = "https://try.activeeon.com:8443"

print(f"Connecting to {proactive_url}...")
gateway = ProActiveGateway(proactive_url)

# Securely input your credentials
gateway.connect(username=input("Username: "), password=getpass.getpass("Password: "))
assert gateway.isConnected(), "Failed to connect to the ProActive server!"

# Create a ProActive job 
print("Creating a ProActive job...") 
job = gateway.createJob("SimpleJob")

# Create a ProActive task 
print("Creating a ProActive Python task...") 
task = gateway.createPythonTask("SimplePythonTask")
task.setTaskImplementation('print("Hello from ProActive!")')
task.addGenericInformation("PYTHON_COMMAND", "python3")

# Add the Python task to the job
job.addTask(task)

# Job submission
job_id = gateway.submitJob(job)
print(f"Job submitted with ID: {job_id}")

# Retrieve job output
print("Job output:")
print(gateway.getJobOutput(job_id))

# Cleanup
gateway.close()
print("Disconnected and finished.")
```

If you have created the `.env` file, you can replace:

```python
import getpass
from proactive import ProActiveGateway

proactive_url = "https://try.activeeon.com:8443"

print(f"Connecting to {proactive_url}...")
gateway = ProActiveGateway(proactive_url)

# Securely input your credentials
gateway.connect(username=input("Username: "), password=getpass.getpass("Password: "))
assert gateway.isConnected(), "Failed to connect to the ProActive server!"
```

by:

```python
from proactive import getProActiveGateway
gateway = getProActiveGateway()
```

If the `.env` file does not exists, it will ask you to enter the `PROACTIVE_URL`, `PROACTIVE_USERNAME` and `PROACTIVE_PASSWORD`.

## Supported programming languages

The ProActive Python SDK supports a wide range of programming languages for task execution within the ProActive Scheduler environment.
These supported languages include:

- `bash` : Linux Bash
- `cmd` : Windows Cmd
- `docker-compose` : Docker Compose
- `scalaw` : Scalaw
- `groovy` : Groovy
- `javascript` : JavaScript
- `python` : Jython (implementation of Python in Java)
- `cpython` : Python (implementation of Python in C – original Python implementation)
- `ruby` : Ruby
- `perl` : Perl
- `powershell` : PowerShell
- `R` : R Language

This comprehensive support enables you to integrate a variety of programming languages into your workflows, allowing for a flexible and versatile development experience within the ProActive Scheduler.

To print the list of supported programming languages in the ProActive Python SDK, you can use the following command:

```python
print(gateway.getProactiveScriptLanguage().get_supported_languages()) 
````

This command fetches the supported languages from the ProActive server via the Python SDK, ensuring you have access to the most up-to-date list directly from your Python script.

### Example: Creating a Groovy Task

To create a Groovy task using the ProActive Python SDK, you can follow these steps, which include creating a job, and adding a Groovy task to this job with a specific task implementation. Below is an example that demonstrates these steps:

```python
...
# Create a new ProActive job
print("Creating a new ProActive job...")
job = gateway.createJob("Groovy_Job_Example")

# Create a new task using Groovy
print("Creating a Groovy task...")
groovy_task = gateway.createTask(language="groovy")
groovy_task.setTaskName("Groovy_Task_Example")
groovy_task.setTaskImplementation("""
println "Hello from Groovy task!"
""")

# Add the Groovy task to the job
job.addTask(groovy_task)
...
```

## Task dependencies

To manage task dependencies in your ProActive Python SDK scripts, you can use the addDependency method. This method allows you to specify that a task depends on the completion of another task before it can begin execution. Here's a simplified example to illustrate how you can manage task dependencies using the ProActive Python SDK:

```python
...
# Create a ProActive job
job = gateway.createJob("Simple_Dependency_Demo")

# Create the first task (Task A)
task_A = gateway.createPythonTask("Task_A")
task_A.setTaskImplementation('print("Task A is running")')

# Create the second task (Task B) which depends on Task A
task_B = gateway.createPythonTask("Task_B")
task_B.setTaskImplementation('print("Task B is running")')
task_B.addDependency(task_A)

# Add tasks to the job
job.addTask(task_A)
job.addTask(task_B)

# Submit the job to the ProActive Scheduler
job_id = gateway.submitJob(job)
print(f"Job submitted with ID: {job_id}")
...
```

In this example:

- `Task A` is a simple Python task that prints `Task A is running`.
- `Task B` is another Python task that prints `Task B is running`.
- `Task B` has a dependency on `Task A`, meaning it will only start after `Task A` has successfully completed. This dependency is established using the `addDependency(task_A)` method.

After both tasks are created and configured, they're added to the job, which is then submitted to the ProActive Scheduler. Task B will wait for Task A to finish before executing.

## Job and task variables

In the ProActive Scheduler, managing data flow and configuration across jobs and their constituent tasks is streamlined through the use of variables. These variables can be defined both at the job level, affecting all tasks within the job, and at the individual task level, for task-specific configurations. The following example demonstrates how to set and utilize these variables using the ProActive Python SDK, showcasing a simple yet effective way to pass and access data within your ProActive workflows.

```python
...
# Create a new ProActive job
job = gateway.createJob("Example_Job")

# Define job-level variables
job.addVariable("jobVar", "jobValue")

# Create the first Python task
task = gateway.createPythonTask()
task.setTaskName("task")
task.setTaskImplementation("""
print("Job variable: ", variables.get("jobVar"))
print("Task variable: ", variables.get("taskVar"))
""")

# Define task-level variables
task.addVariable("taskVar", "taskValue")

# Add the tasks to the job
job.addTask(task)
...
```

This example illustrates the flexibility of the ProActive Python SDK in managing data flow between jobs and tasks through the use of variables. Job-level variables are useful for defining parameters that are common across all tasks in a job, while task-level variables allow for task-specific configurations.

## Data management

There are several ways to transfer data from/to a job/task, and between tasks:

### Global variables

To transfer data (variables) between TaskA and TaskB, we can use the mechanism of global variables, where the TaskA creates a global variable that is visible by the TaskB and any other tasks created on the same job.

#### TaskA: Producing a global variable

In `TaskA`, you can define a variable within the task implementation and set its value. After the task execution, you mark this variable as a global variable.

```python
...
# TaskA Implementation
taskA = gateway.createPythonTask("TaskA")
taskA.setTaskImplementation('''
# Task logic
variableA = "Hello from TaskA"
# Setting a resulting variable
variables.put("variableFromA", variableA)
''')
...
```

#### TaskB: Consuming the global variable

In `TaskB`, you access the global variable produced by `TaskA` using the `variables.get()` method. This requires `TaskB` to have a dependency on `TaskA`, ensuring `TaskA` executes before `TaskB` and the variable is available.

```python
...
# TaskB Implementation
taskB = gateway.createPythonTask("TaskB")
taskB.addDependency(taskA)
taskB.setTaskImplementation('''
# Accessing the variable from TaskA
variableFromA = variables.get("variableFromA")
print("Received in TaskB:", variableFromA)
''')
...
```

### Result variable

Using result variables is a powerful method to transfer data between tasks within the same job. This approach allows a task (e.g., `TaskA`) to produce a result that can be accessed by subsequent tasks (e.g., `TaskB`) that depend on it. Here's how you can work with result variables in ProActive workflows:

#### TaskA: Producing a result variable

`TaskA` executes its business logic and generates a result. This result is then implicitly available to any tasks that are defined as its successors, making it an effective way to pass data forward in a workflow.

```python
...
# Create a Python task A
print("Creating a Python task...")
taskA = gateway.createPythonTask("PythonTaskA")
taskA.setTaskImplementation("""
print("Hello")
result = "World"
""")
...
```

#### TaskB: Consuming the result variable

`TaskB`, which has a dependency on TaskA, can access the result produced by `TaskA`. This is done by iterating over the `results` object, which contains the outcomes of all predecessor tasks TaskB is dependent on.

```python
...
# Create a Python task B
print("Creating a Python task...")
taskB = gateway.createPythonTask("PythonTaskB")
taskB.addDependency(taskA)
taskB.setTaskImplementation("""
for res in results:
    print(str(res))
""")
...
```

To ensure that `TaskB` correctly consumes the result variable produced by `TaskA`, you must explicitly declare `TaskA` as a dependency of `TaskB`. This setup guarantees the sequential execution order where `TaskA` completes before `TaskB` starts, allowing `TaskB` to access the results produced by `TaskA`.

## Documentation

For more detailed usage and advanced functionalities, please refer to the [ProActive Python Client Documentation](https://proactive-python-client.readthedocs.io/en/latest/).

## Examples Repository

For practical examples showcasing various features of the ProActive Python Client, visit our [examples repository](https://github.com/ow2-proactive/proactive-python-client-examples).

## Contributing

Contributions are welcome! If you have an improvement or a new feature in mind, feel free to fork the repository, make your changes, and submit a pull request.
