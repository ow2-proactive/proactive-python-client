# ProActive Python Client / SDK

![License BSD](https://img.shields.io/badge/License-BSD-blue.svg "License BSD")
![Python 3](https://img.shields.io/badge/Python-3-brightgreen.svg "Python 3")
![Proactive](https://img.shields.io/pypi/v/proactive.svg "Proactive")
[![Documentation Status](https://readthedocs.org/projects/proactive-python-client/badge/?version=latest)](https://proactive-python-client.readthedocs.io/en/latest/?badge=latest)

The ProActive Python Client (or Proactive Python SDK) enables seamless interaction with the ProActive Scheduler and Resource Manager, facilitating the automation of workflow submission and the management of tasks directly from Python.

## Summary

- [ProActive Python Client / SDK](#proactive-python-client--sdk)
  - [Summary](#summary)
  - [Key Features](#key-features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Building from Source](#building-from-source)
      - [Linux or Mac](#linux-or-mac)
      - [Windows](#windows)
      - [GitHub Codespaces (Linux)](#github-codespaces-linux)
    - [Running Tests](#running-tests)
      - [With Gradle](#with-gradle)
      - [With Make](#with-make)
  - [Quickstart Example](#quickstart-example)
  - [Supported programming languages](#supported-programming-languages)
    - [Example: Creating a Groovy Task](#example-creating-a-groovy-task)
  - [Task implementation](#task-implementation)
    - [Inline Implementation](#inline-implementation)
    - [Copy Implementation from an External File](#copy-implementation-from-an-external-file)
    - [Copy Implementation from a URL File](#copy-implementation-from-a-url-file)
    - [Reference Implementation from an External File](#reference-implementation-from-an-external-file)
  - [Task dependencies](#task-dependencies)
  - [Job and task variables](#job-and-task-variables)
    - [Global variables](#global-variables)
      - [TaskA: Producing a global variable](#taska-producing-a-global-variable)
      - [TaskB: Consuming the global variable](#taskb-consuming-the-global-variable)
    - [Result variable](#result-variable)
      - [TaskA: Producing a result variable](#taska-producing-a-result-variable)
      - [TaskB: Consuming the result variable](#taskb-consuming-the-result-variable)
  - [Data management](#data-management)
    - [Data spaces](#data-spaces)
      - [Example: Managing Data Transfers with User and Global Spaces](#example-managing-data-transfers-with-user-and-global-spaces)
        - [Transferring data to the user space](#transferring-data-to-the-user-space)
        - [Transferring data from the user space](#transferring-data-from-the-user-space)
      - [Adapting for Global Space Use](#adapting-for-global-space-use)
    - [Uploading and Downloading Files](#uploading-and-downloading-files)
      - [Uploading Files to the Task's Local Space](#uploading-files-to-the-tasks-local-space)
        - [Example: Uploading Files for Task Execution](#example-uploading-files-for-task-execution)
      - [Downloading Files from the Task's Local Space](#downloading-files-from-the-tasks-local-space)
        - [Example: Downloading Task Results](#example-downloading-task-results)
  - [Documentation](#documentation)
  - [Examples Repository](#examples-repository)
  - [Contributing](#contributing)

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

To access to the latest features and improvements, install the pre-release version:

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
# gradlew clean build

# Install the built package
pip install dist/*.zip  # Replace XXX with the actual version
```

#### Windows

```bat
REM Build the package
build.bat CLEAN_BUILD

REM Install the built package
REM Replace XXX with the actual version
pip install dist\*.zip
```

#### GitHub Codespaces (Linux)

To set up your environment in GitHub Codespaces for building the ProActive Python Client, follow these steps:

1. **Update the package list and install the Java 8 SDK:**

    ```bash
    sudo apt update
    sudo apt install openjdk-8-jdk
    ```

2. **Clone the `jenv` repository and set up `jenv`:**

    ```bash
    git clone https://github.com/jenv/jenv.git ~/.jenv
    echo 'export PATH="$HOME/.jenv/bin:$PATH"' >> ~/.bash_profile
    echo 'eval "$(jenv init -)"' >> ~/.bash_profile
    source ~/.bash_profile
    ```

3. **Add Java 8 to `jenv` and set it as the global version:**

    ```bash
    jenv add /usr/lib/jvm/java-8-openjdk-amd64/jre/
    jenv global 1.8
    java -version
    ```

4. **Build and install the package from source:**

    ```bash
    # Build the package
    make clean_build
    # or use gradlew
    # ./gradlew clean build

    # Install the built package
    pip install dist/*.zip
    ```

By following these steps, you'll have the Java 8 SDK installed and configured with `jenv`, and you will be able to build and install the ProActive Python Client package from source within GitHub Codespaces.

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

This simple example demonstrates how to connect to a ProActive server, create a job, add a Python task, and submit the job:

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

If the `.env` file does not exists, it will prompt you to enter the `PROACTIVE_URL`, `PROACTIVE_USERNAME` and `PROACTIVE_PASSWORD`.

Please see [demo_basic.py](https://github.com/ow2-proactive/proactive-python-client-examples/blob/main/demo_basic.py) for a complete example.

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

This comprehensive support enables you to integrate a variety of programming languages into your workflows, fostering for a flexible and versatile development experience within the ProActive Scheduler.

To print the list of supported programming languages in the ProActive Python SDK, you can use the following command:

```python
print(gateway.getProactiveScriptLanguage().get_supported_languages()) 
````

This command fetches the supported languages from the ProActive server via the Python SDK, ensuring that you have access to the most up-to-date list directly from your Python script.

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

Please see [demo_multilanguage_job.py](https://github.com/ow2-proactive/proactive-python-client-examples/blob/main/demo_multilanguage_job.py) for a complete example.

## Task implementation

Task implementations are central to defining the operations a task will perform within the ProActive Scheduler. The ProActive Python Client offers several methods to specify these implementations, catering to a variety of use cases and preferences. Below, we explore these methods in detail:

### Inline Implementation

Inline implementation allows you to directly embed the task logic within your script. This approach is straightforward and ideal for simple tasks or quick prototyping.

**Example:**

```python
task.setTaskImplementation('print("Hello from ProActive!")')
```

Please see [demo_basic.py](https://github.com/ow2-proactive/proactive-python-client-examples/blob/main/demo_basic.py) for a complete example.

### Copy Implementation from an External File

For tasks with more complex logic, or when you wish to maintain a cleaner script, you can specify the task implementation from an external Python file. This method simplifies code management and enhances readability.

**Example:**

```python
task.setTaskImplementationFromFile('path/to/your_script.py')
```

Please see [demo_impl_file.py](https://github.com/ow2-proactive/proactive-python-client-examples/blob/main/demo_impl_file.py) for a complete example.

### Copy Implementation from a URL File

When your task implementation resides online, for instance, in a GitHub repository, you can load it directly via its URL. This method ensures your tasks are always up-to-date with the latest version of the script hosted online.

**Example:**

```python
task.setTaskImplementationFromURL('https://path/to/your_script.py')
```

Please see [demo_impl_url.py](https://github.com/ow2-proactive/proactive-python-client-examples/blob/main/demo_impl_url.py) for a complete example.

### Reference Implementation from an External File

Advanced scenarios might require running a Python script with arguments or using specific Python modules. In such cases, you can reference the main script and include additional resources, such as libraries or datasets, ensuring all necessary files are available for the task execution.

**Example:**

```python
# Specify the main script and arguments
task.setTaskExecutionFromFile('main_script.py', ['arg1', 'arg2'])

# Include an entire directory as input files
task.addInputFile('path/to/directory/**')
```

**Important:** When using `addInputFile` and `addOutputFile`, remember to invoke `submitJobWithInputsAndOutputsPaths(job)` instead of `submitJob(job)` to ensure proper handling of file paths.

Please see [demo_exec_file.py](https://github.com/ow2-proactive/proactive-python-client-examples/blob/main/demo_exec_file.py) for a complete example.

These methods provide the flexibility to structure your tasks in a way that best fits your project's requirements, whether for simplicity, code organization, or integration with external resources.

## Task dependencies

To manage task dependencies in your ProActive Python SDK scripts, you can use the `addDependency` method. This method allows you to specify the task dependence on the completion of another task before it can begin execution. Here's a simplified example to illustrate how you can manage task dependencies using the ProActive Python SDK:

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

After both tasks are created and configured, they're added to the job, which is then submitted to the ProActive Scheduler. `Task B` will wait for `Task A` to finish before executing.

Please see [demo_task_dependency.py](https://github.com/ow2-proactive/proactive-python-client-examples/blob/main/demo_task_dependency.py) for a complete example.

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

Please see [demo_job_task_var.py](https://github.com/ow2-proactive/proactive-python-client-examples/blob/main/demo_job_task_var.py) for a complete example.

### Global variables

To transfer data (variables) between `TaskA` and `TaskB`, we can use the mechanism of global variables, where the `TaskA` creates a global variable that is visible by the `TaskB` and any other tasks created on the same job.

#### TaskA: Producing a global variable

In `TaskA`, you can define a variable within the task implementation and set its value. After the task execution, you mark this variable as a global variable.

```python
...
# TaskA Implementation
taskA = gateway.createPythonTask("TaskA")
taskA.setTaskImplementation('''
# Task logic
variableA = "Hello from TaskA"
# Setting a global variable
variables.put("variableFromA", variableA)
''')
...
```

#### TaskB: Consuming the global variable

In `TaskB`, you access the global variable produced by `TaskA` using the `variables.get()` method. This requires `TaskB` to have a dependency on `TaskA`, ensuring that `TaskA` executes before `TaskB` and the variable becomes available.

```python
...
# TaskB Implementation
taskB = gateway.createPythonTask("TaskB")
taskB.addDependency(taskA)
taskB.setTaskImplementation('''
# Accessing the global variable created by TaskA
variableFromA = variables.get("variableFromA")
print("Received in TaskB:", variableFromA)
''')
...
```

Please see [demo_global_var.py](https://github.com/ow2-proactive/proactive-python-client-examples/blob/main/demo_global_var.py) for a complete example.

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

`TaskB`, which has a dependency on `TaskA`, can access the result produced by `TaskA`. This is achieved by iterating over the `results` object, which encompasses the outcomes of all predecessor tasks that `TaskB` is dependent on.

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

Please see [demo_task_result.py](https://github.com/ow2-proactive/proactive-python-client-examples/blob/main/demo_task_result.py) for a complete example.

## Data management

Efficient data management is pivotal in executing distributed tasks with the ProActive Scheduler. This encompasses handling input and output files, managing data flow between tasks, and storing or sharing resources across different executions. The ProActive Python Client facilitates robust data management through various mechanisms, enabling you to manipulate data spaces and directly transfer files to/from the task's execution environment. This section elucidates two primary aspects of data management: "Data Spaces" and "Uploading and Downloading Files," highlighting their applications and differences to cater to diverse workflow requirements.

### Data spaces

Data spaces in the ProActive Scheduler offer a robust mechanism for managing file transfers across different spaces, including user and global data spaces. These spaces facilitate the storage and retrieval of files, allowing for efficient data management within jobs and tasks.

- **User Space**: A private storage area accessible only to the user's jobs, ideal for personal or sensitive data.
- **Global Space**: A shared storage space accessible by all users, suitable for commonly used data or resources.

#### Example: Managing Data Transfers with User and Global Spaces

The following example illustrates how to perform file transfers between the task's local space (where the task is running) and the ProActive Scheduler's data spaces, showcasing both user and global spaces.

**Scenario**:

1. A text file named `hello_world.txt` containing "Hello World" is created in the task's local space.
2. The file is then transferred to the user space using `userspaceapi` for demonstration purposes.
3. Instructions are provided to modify the code to utilize the global space instead, using `globalspaceapi`.

Note that the task's `local space` is the data space where the `TaskA` is running (e.g. `/tmp/PA_*/*/*`).

The default path to the user and global spaces are usually defined as:

- `$PA_SCHEDULER_HOME/data/defaultuser/`

- `$PA_SCHEDULER_HOME/data/defaultglobal/`

##### Transferring data to the user space

To transfer files from the task's local space to the user space in `TaskA`, you can use the following approach:

```python
...
# Task A: Creating and transferring a file to the user space
taskA = gateway.createPythonTask("TaskA")
taskA.setTaskImplementation("""
import os

file_name = 'hello_world.txt'
with open(file_name, 'w') as file:
    file.write("Hello World")
print("File created: " + file_name)

# Define the data space path
dataspace_path = 'path/in/user/space/' + file_name

# Transferring file to the user space
print("Transferring file to the user space")
userspaceapi.connect()
userspaceapi.pushFile(gateway.jvm.java.io.File(file_name), dataspace_path)
print("Transfer complete")

# Transfer the file info to the next task
variables.put("TASK_A_FILE_NAME", file_name)
variables.put("TASK_A_DATASPACE_PATH", dataspace_path)
""")
...
```

##### Transferring data from the user space

In `TaskB`, to import files from the user space back to the task's local space, use the following method:

```python
...
# Task B: Importing and displaying the file from the user space
taskB = gateway.createPythonTask("TaskB")
taskB.addDependency(taskA)
taskB.setTaskImplementation("""
import os

# Get the file info from the previous task
file_name = variables.get("TASK_A_FILE_NAME")
dataspace_path = variables.get("TASK_A_DATASPACE_PATH")

# Transfer file from the user space to the local space
print("Importing file from the user space")
userspaceapi.connect()
userspaceapi.pullFile(dataspace_path, gateway.jvm.java.io.File(file_name))
if os.path.exists(file_name):
    with open(file_name, 'r') as file:
        print("File contents: " + file.read())
else:
    print("File does not exist.")
""")
...
```

#### Adapting for Global Space Use

To adapt the above example for transferring data to and from the global space, replace the `userspaceapi` calls with `globalspaceapi` as demonstrated below:

**For Transferring to Global Space in TaskA**:

```python
print("Transferring file to the global space")
globalspaceapi.connect()
globalspaceapi.pushFile(gateway.jvm.java.io.File(file_name), dataspace_path)
print("Transfer complete")
```

**For Importing from Global Space in TaskB**:

```python
print("Importing file from the global space")
globalspaceapi.connect()
globalspaceapi.pullFile(dataspace_path, gateway.jvm.java.io.File(file_name))
print("Import complete")
```

This comprehensive guide and example provide clear instructions on how to effectively manage data transfers within ProActive Scheduler workflows, utilizing both user and global data spaces for flexible data management solutions.

Please see [demo_dataspace_api.py](https://github.com/ow2-proactive/proactive-python-client-examples/blob/main/demo_dataspace_api.py) for a complete example.

### Uploading and Downloading Files

When working with ProActive workflows, you may need to upload files from your local machine to the execution environment where your tasks run (the "local space" of the task) and download the results back to your machine after the task execution. This process is facilitated by two key methods in the ProActive Python Client: `addInputFile` for uploading and `addOutputFile` for downloading files.

#### Uploading Files to the Task's Local Space

Before a task is executed, you can specify files to be uploaded to the task's local space (where the task will be executed) using the `addInputFile` method. This is particularly useful for tasks that require specific data files or scripts present to perform their computation.

##### Example: Uploading Files for Task Execution

```python
# Assuming 'task' is your task object
# Upload files located in 'local_directory_path/' on your local machine
# to the task's local space before execution
task.addInputFile('local_directory_path/**')
```

This code snippet demonstrates how to upload all files from a local directory (`local_directory_path/`) to the task's local space. The `**` pattern is used to include all files and subdirectories within that directory.

#### Downloading Files from the Task's Local Space

After the task execution, you can specify files or directories to be downloaded from the task's local space back to your local machine using the `addOutputFile` method. This allows you to easily retrieve results, logs, or any other files generated by your task.

##### Example: Downloading Task Results

```python
# Assuming 'task' is your task object
# Download files from the task's local space to your local machine
# after task execution
task.addOutputFile('path/in/task/local/space/**')
```

In this example, `path/in/task/local/space/**` should be replaced with the specific path in the task's local space where the output files are located. The `**` pattern ensures that all files and subdirectories under this path are downloaded.

The `addInputFile` and `addOutputFile` methods provide a straightforward approach to manage file transfers directly between your local machine and the ProActive task's execution environment. This mechanism simplifies the process of providing input data to your tasks and retrieving the results, enhancing the efficiency and flexibility of your ProActive workflows. Note that this process is distinct from using the ProActive Scheduler's user or global data spaces, which involve transferring files within the server's data space rather than between the user's local machine and the task's local space.

Please see [demo_transf_file.py](https://github.com/ow2-proactive/proactive-python-client-examples/blob/main/demo_transf_file.py) for a complete example.

## Documentation

For more detailed usage and advanced functionalities, please refer to the [ProActive Python Client Documentation](https://proactive-python-client.readthedocs.io/en/latest/).

## Examples Repository

For practical examples showcasing various features of the ProActive Python Client, visit our [examples repository](https://github.com/ow2-proactive/proactive-python-client-examples).

## Contributing

Contributions are welcome! If you have an improvement or a new feature in mind, feel free to fork the repository, make your changes, and submit a pull request.
