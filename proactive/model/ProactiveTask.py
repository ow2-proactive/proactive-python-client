import os
import subprocess
import cloudpickle
import codecs

from tempfile import TemporaryDirectory

from .ProactiveScriptLanguage import *
from .ProactiveSelectionScript import *
from .ProactiveRuntimeEnv import *

class ProactiveTask(object):
    """
    Represents a generic proactive task

    script_language (ProactiveScriptLanguage)
    fork_environment (ProactiveForkEnv)
    task_name (string)
    task_implementation (string)
    generic_information (map)
    input_files (list)
    output_files (list)
    dependencies (list[ProactiveTask])
    pre_script (ProactivePreScript)
    post_script (ProactivePostScript)
    flow_script (ProactiveFlowScript)
    flow_block (ProactiveFlowBlock)
    """

    def __init__(self, script_language=None, task_name=''):
        self.script_language = script_language
        self.fork_environment = None
        self.selection_script = None
        self.task_name = task_name
        self.task_implementation = ''
        self.task_implementation_url = None
        self.variables = {}
        self.generic_information = {}
        self.input_files = []
        self.output_files = []
        self.dependencies = []
        self.description = []
        self.pre_script = None
        self.post_script = None
        self.flow_script = None
        self.flow_block = None
        self.precious_result = False

    def __str__(self):
        return self.getTaskName()

    def __repr__(self):
        return self.getTaskName()

    def setScriptLanguage(self, script_language):
        self.script_language = script_language

    def getScriptLanguage(self):
        return self.script_language

    def setPreciousResult(self, precious_result):
        self.precious_result = precious_result

    def getPreciousResult(self):
        return self.precious_result

    def setForkEnvironment(self, fork_environment):
        self.fork_environment = fork_environment

    def getForkEnvironment(self):
        return self.fork_environment

    def hasForkEnvironment(self):
        return True if self.fork_environment is not None else False

    def setRuntimeEnvironment(self, type=None, image=None, nvidia_gpu=None, mount_host_path=None, mount_container_path=None, rootless=None, isolation=None, no_home=None, host_network=None, verbose=None):
        """
        Defines and sets the runtime environment for executing a task within a containerized environment.
        Parameters:
        - type (str): Specifies the type of container technology to use for running the task. 
        Options include "docker", "podman", "singularity", or any other value to indicate a non-containerized execution.
        - image (str): The container image to use for running the task. Ensure that the 'py4j' Python package is available in the specified image.
        - nvidia_gpu (bool): Whether to enable NVIDIA GPU support within the container. Automatically set to False if no NVIDIA GPUs are present.
        - mount_host_path (str): The host machine path to mount into the container, providing the container access to specific directories or files from the host.
        - mount_container_path (str): The path inside the container where the host's file system (or a part of it) specified by `mount_host_path` will be accessible.
        - rootless (bool): Enables or disables rootless mode for the container execution, applicable to all container types (default False).
        - isolation (bool): Enables or disables isolation mode specifically for Singularity containers (default False). This parameter is only applicable if 'type' is set to "singularity".
        - no_home (bool): When set to True, the user's home directory is not mounted inside the container if the home directory is not the current working directory. Only applicable to Singularity containers (default False).
        - host_network (bool): Configures the container to use the host's network stack directly, bypassing the default or custom network namespaces (default False).
        - verbose (bool): Enables verbose output for the container runtime environment setup process (default False).
        """
        self.fork_environment = ProactiveRuntimeEnv().create(type, image, nvidia_gpu, mount_host_path, mount_container_path, rootless, isolation, no_home, host_network, verbose)

    def setSelectionScript(self, selection_script):
        self.selection_script = selection_script

    def getSelectionScript(self):
        return self.selection_script

    def hasSelectionScript(self):
        return True if self.selection_script is not None else False

    def setTaskName(self, task_name):
        self.task_name = task_name

    def getTaskName(self):
        return self.task_name

    def setTaskImplementationFromURL(self, task_url):
        self.task_implementation_url = task_url
        self.task_implementation = ''

    def getTaskImplementationFromURL(self):
        return self.task_implementation_url

    def setTaskImplementationFromFile(self, task_file):
        if os.path.exists(task_file):
            with open(task_file, 'r') as content_file:
                self.setTaskImplementation(content_file.read())

    def setTaskImplementation(self, task_implementation):
        self.task_implementation = "\n"
        self.task_implementation += task_implementation
        self.task_implementation_url = None

    def getTaskImplementation(self):
        return self.task_implementation

    def addVariable(self, key, value):
        self.variables[key] = value

    def getVariables(self):
        return self.variables

    def hasVariables(self):
        return True if self.variables else False

    def removeVariable(self, key):
        del self.variables[key]

    def clearVariables(self):
        self.variables.clear()

    def addGenericInformation(self, key, value):
        self.generic_information[key] = value

    def getGenericInformation(self):
        return self.generic_information

    def removeGenericInformation(self, key):
        del self.generic_information[key]

    def clearGenericInformation(self):
        self.generic_information.clear()

    def addInputFile(self, input_file):
        self.input_files.append(input_file)

    def removeInputFile(self, input_file):
        self.input_files.remove(input_file)

    def clearInputFiles(self):
        self.input_files.clear()

    def getInputFiles(self):
        return self.input_files

    def addOutputFile(self, output_file):
        self.output_files.append(output_file)

    def removeOutputFile(self, output_file):
        self.output_files.remove(output_file)

    def clearOutputFiles(self):
        self.output_files.clear()

    def getOutputFiles(self):
        return self.output_files

    def addDependency(self, task):
        self.dependencies.append(task)

    def removeDependency(self, task):
        self.dependencies.remove(task)

    def clearDependencies(self):
        self.dependencies.clear()

    def getDependencies(self):
        return self.dependencies

    def setDescription(self, description):
        self.description = description

    def getDescription(self):
        return self.description

    def setPreScript(self, pre_script):
        self.pre_script = pre_script

    def getPreScript(self):
        return self.pre_script

    def hasPreScript(self):
        return True if self.pre_script is not None else False

    def setPostScript(self, post_script):
        self.post_script = post_script

    def getPostScript(self):
        return self.post_script

    def hasPostScript(self):
        return True if self.post_script is not None else False

    def setFlowScript(self, flow_script):
        self.flow_script = flow_script

    def getFlowScript(self):
        return self.flow_script

    def hasFlowScript(self):
        return True if self.flow_script is not None else False

    def setFlowBlock(self, flow_block):
        self.flow_block = flow_block

    def getFlowBlock(self):
        return self.flow_block

    def hasFlowBlock(self):
        return True if self.flow_block is not None else False
    
    def setSignals(self, taskSignals, scope="prescript"):
        if scope not in ['prescript', 'taskscript', 'postscript']:
            raise ValueError("The signals scope should be one of the following options: 'prescript', 'taskscript' or 'postscript'")
        signalsScriptImplementation = """
        import com.google.common.base.Splitter;
        import org.ow2.proactive.scheduler.common.job.JobVariable;
        """
        for taskSignal in taskSignals:
            signalName = taskSignal
            signalVariables = taskSignals[signalName]
            signals = list(taskSignals.keys())
            signalsScriptImplementation += """
            // Define signal variables
            List<JobVariable> signalVariables{signalName} = new java.util.ArrayList<JobVariable>()
            """.format(signalName=signalName)
            for signalVariable in signalVariables:
                variableName = signalVariable['name']
                variableValue = signalVariable['value']
                variableModel = signalVariable['model']
                variableDescription = signalVariable['description']
                variableGroup = signalVariable['group']
                variableAdvanced = str(signalVariable['advanced']).lower()
                variableHidden = str(signalVariable['hidden']).lower()
                signalsScriptImplementation += """
                signalVariables{signalName}.add(new JobVariable("{variableName}", "{variableValue}", "{variableModel}", "{variableDescription}", "{variableGroup}", {variableAdvanced}, {variableHidden}))
                """.format(
                    signalName=signalName,
                    variableName=variableName,
                    variableValue=variableValue,
                    variableModel=variableModel,
                    variableDescription=variableDescription,
                    variableGroup=variableGroup,
                    variableAdvanced=variableAdvanced,
                    variableHidden=variableHidden
                )
            signalsScriptImplementation += """
                if (signalVariables{signalName}.isEmpty()) {{
                    signalapi.readyForSignal("{signalName}")
                }} else {{
                    signalapi.readyForSignal("{signalName}", signalVariables{signalName})
                }}
            """.format(signalName=signalName)
        signalsScriptImplementation += """
        signalsSet = {signals}.toSet()
        // Wait until one signal among those specified is received
        println("Waiting for any signal among " + signalsSet)
        receivedSignal = signalapi.waitForAny(signalsSet)
        // Remove ready signals
        signalapi.removeManySignals(new HashSet<>(signalsSet.collect {{ signal -> "ready_" + signal }}))
        // Display the received signal and add it to the job result
        println("Received signal: " + receivedSignal)
        println("Signal variables: ")
        def signalvariables = receivedSignal.getUpdatedVariables().each {{ k, v -> println "${{k}}:${{v}}" }}
        task_name = variables.get("PA_TASK_NAME")
        task_id = variables.get("PA_TASK_ID")
        receivedSignalObjId = "RECEIVED_SIGNAL_" + task_name + "_" + task_id
        def receivedSignalObj = [
            name: receivedSignal.toString(),
            variables: signalvariables
        ]
        variables.put(receivedSignalObjId, receivedSignalObj)
        """.format(signals=signals)
        if scope == 'prescript':
            taskPreScript = ProactivePreScript(ProactiveScriptLanguage().groovy())
            taskPreScript.setImplementation(signalsScriptImplementation)
            self.setPreScript(taskPreScript)
        if scope == 'taskscript':
            self.setScriptLanguage(ProactiveScriptLanguage().groovy())
            self.setTaskImplementation(signalsScriptImplementation)
        if scope == 'postscript':
            taskPostScript = ProactivePostScript(ProactiveScriptLanguage().groovy())
            taskPostScript.setImplementation(signalsScriptImplementation)
            self.setPostScript(taskPostScript)

class ProactivePythonTask(ProactiveTask):
    """
    Represents a proactive python task
    """

    def __init__(self, task_name='', default_python='python3'):
        """
        Initializes a ProactivePythonTask instance.
        
        Parameters:
        - task_name (str): Name of the task (default is an empty string).
        - default_python (str): Default Python interpreter to use (default is 'python3').
        """
        super(ProactivePythonTask, self).__init__(ProactiveScriptLanguage().python(), task_name)
        self.setDefaultPython(default_python)

    def setDefaultPython(self, default_python='python3'):
        """
        Sets the default Python interpreter for the task.
        
        Parameters:
        - default_python (str): The Python interpreter to use (default is 'python3').
        """
        self.default_python = default_python
        self.addGenericInformation("PYTHON_COMMAND", default_python)

    def setVirtualEnv(self, requirements=[], basepath="./", name="venv", verbosity=False, overwrite=False, install_requirements_if_exists=False):
        """
        Sets up a virtual environment for the task.
        
        Parameters:
        - requirements (list): List of Python packages to install in the virtual environment (default is an empty list).
        - basepath (str): Base path where the virtual environment will be created (default is current directory).
        - name (str): Name of the virtual environment directory (default is 'venv').
        - verbosity (bool): If True, enables verbose output (default is False).
        - overwrite (bool): If True, overwrites the existing virtual environment (default is False).
        - install_requirements_if_exists (bool): If True, installs requirements even if the virtual environment already exists (default is False).
        """
        if basepath is None:
            basepath = TemporaryDirectory().name
        venv_path = os.path.join(basepath, name)
        requirements_str = ' '.join(requirements)
        # Script to handle virtual environment creation
        fork_env_script = """
def envScript = localspace + "/createVirtualEnv.sh"
File file = new File(envScript)
file << "#!/bin/bash\\n"
file << "cd " + localspace + "\\n"
if (new File("{venv_path}").exists()) {{
    if ("{overwrite}" == "true") {{
        file << "echo [INFO] Overwriting existing virtualenv\\n"
        file << "rm -rf {venv_path}\\n"
        file << "{python} -m venv {venv_path}\\n"
        file << "source {venv_path}/bin/activate\\n"
        file << "pip install --upgrade pip\\n"
        file << "pip install py4j\\n"
        file << "echo [INFO] Installing requirements\\n"
        modules = "{requirements}".split("\\\\s+")
        for (String module : modules) {{
            file << "pip install " + module + "\\n"
        }}
    }} else {{
        file << "echo [INFO] Using existing virtualenv\\n"
        file << "source {venv_path}/bin/activate\\n"
        if ("{install_requirements_if_exists}" == "true") {{
            file << "echo [INFO] Installing requirements\\n"
            modules = "{requirements}".split("\\\\s+")
            for (String module : modules) {{
                file << "pip install " + module + "\\n"
            }}
        }}
    }}
}} else {{
    file << "echo [INFO] Creating a new virtualenv\\n"
    file << "{python} -m venv {venv_path}\\n"
    file << "source {venv_path}/bin/activate\\n"
    file << "pip install --upgrade pip\\n"
    file << "pip install py4j\\n"
    file << "echo [INFO] Installing requirements\\n"
    modules = "{requirements}".split("\\\\s+")
    for (String module : modules) {{
        file << "pip install " + module + "\\n"
    }}
}}
("chmod u+x " + envScript).execute().text
if ("{verbosity}" == "true") {{
    file << "pip -V && pip freeze\\n"
    println envScript + "\\n" + file.text
    println envScript.execute().text
}} else {{
    envScript.execute().waitFor()
}}
        """.format(
            venv_path=venv_path,
            python=self.default_python,
            overwrite=str(overwrite).lower(),
            requirements=requirements_str,
            verbosity=str(verbosity).lower(),
            install_requirements_if_exists=str(install_requirements_if_exists).lower()
        )
        fork_env = ProactiveForkEnv(ProactiveScriptLanguage().groovy())
        fork_env.setImplementation(fork_env_script)
        self.setForkEnvironment(fork_env)
        self.setDefaultPython(os.path.join(venv_path, 'bin', 'python'))

    def setVirtualEnvFromFile(self, requirements_file, basepath="./", name="venv", verbosity=False, overwrite=False, install_requirements_if_exists=False):
        """
        Sets up a virtual environment for the task using requirements from a file.
        
        Parameters:
        - requirements_file (str): Path to a text file containing Python packages to install.
        - basepath (str): Base path where the virtual environment will be created (default is current directory).
        - name (str): Name of the virtual environment directory (default is 'venv').
        - verbosity (bool): If True, enables verbose output (default is False).
        - overwrite (bool): If True, overwrites the existing virtual environment (default is False).
        - install_requirements_if_exists (bool): If True, installs requirements even if the virtual environment already exists (default is False).
        """
        if not os.path.exists(requirements_file):
            raise FileNotFoundError("Requirements file not found: {}".format(requirements_file))

        with open(requirements_file, 'r') as file:
            requirements = [line.strip() for line in file if line.strip() and not line.startswith('#')]

        self.setVirtualEnv(
            requirements=requirements,
            basepath=basepath,
            name=name,
            verbosity=verbosity,
            overwrite=overwrite,
            install_requirements_if_exists=install_requirements_if_exists
        )

    def setTaskExecutionFromFile(self, task_file, parameters=[], displayTaskResultOnScheduler=True):
        """
        Sets the task implementation from a Python script file.
        
        Parameters:
        - task_file (str): Path to the Python script file.
        - parameters (list): List of parameters to pass to the script (default is an empty list).
        - displayTaskResultOnScheduler (bool): If True, displays the task result on the scheduler (default is True).
        """
        if os.path.exists(task_file):
            params_string = ' '.join(parameters)
            task_implementation = "import subprocess"
            task_implementation += "\n"
            task_implementation += "print('Running " + task_file + " with " + params_string + " as parameters...')"
            task_implementation += "\n"
            task_implementation += "result = subprocess.check_output('python " + task_file + " " + params_string + "', shell=True).strip()"
            task_implementation += "\n"
            if displayTaskResultOnScheduler:
                task_implementation += "print('-' * 10)"
                task_implementation += "\n"
                task_implementation += "print(result.decode('ascii'))"
                task_implementation += "\n"
                task_implementation += "print('-' * 10)"
                task_implementation += "\n"
            task_implementation += "print('Finished')"
            self.setTaskImplementation(task_implementation)
            self.addInputFile(task_file)

    def setTaskExecutionFromLambdaFunction(self, lambda_function):
        """
        Sets the task implementation from a lambda function.
        
        Parameters:
        - lambda_function (function): The lambda function to execute.
        """
        pickled_lambda = codecs.encode(cloudpickle.dumps(lambda_function), "base64")
        task_implementation = "import pickle"
        task_implementation += "\n"
        task_implementation += "import codecs"
        task_implementation += "\n"
        task_implementation += "result = pickle.loads(codecs.decode(%s, \"base64\"))()" % pickled_lambda
        task_implementation += "\n"
        task_implementation += "print('result: ', result)"
        self.setTaskImplementation(task_implementation)
