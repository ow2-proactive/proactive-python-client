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

## Documentation

For more detailed usage and advanced functionalities, please refer to the [ProActive Python Client Documentation](https://proactive-python-client.readthedocs.io/en/latest/).

## Examples Repository

For practical examples showcasing various features of the ProActive Python Client, visit our [examples repository](https://github.com/ow2-proactive/proactive-python-client-examples).

## Contributing

Contributions are welcome! If you have an improvement or a new feature in mind, feel free to fork the repository, make your changes, and submit a pull request.
