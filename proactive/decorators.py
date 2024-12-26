from functools import wraps
from proactive import getProActiveGateway, ProactiveScriptLanguage, ProactiveFlowBlock

# Global list to store tasks defined by decorators
registered_tasks = []

class TaskDecorator:
    def __init__(self, language):
        self.language = language

    def __call__(self, name=None, depends_on=None, runtime_env=None, virtual_env=None, input_files=None, output_files=None, prescript=None, postscript=None):
        def decorator(func):
            return task(name=name, depends_on=depends_on, language=self.language, runtime_env=runtime_env, virtual_env=virtual_env, input_files=input_files, output_files=output_files, prescript=prescript, postscript=postscript)(func)
        return decorator

class LoopDecorator:
    @staticmethod
    def start():
        def decorator(func):
            func._is_loop_start = True
            return func
        return decorator

    @staticmethod
    def end(loop_criteria):
        def decorator(func):
            func._is_loop_end = True
            func._loop_criteria = loop_criteria
            return func
        return decorator

loop = LoopDecorator()

class ReplicateDecorator:
    @staticmethod
    def start(replicate_criteria):
        def decorator(func):
            func._is_replicate_start = True
            func._replicate_criteria = replicate_criteria
            return func
        return decorator

    @staticmethod
    def end():
        def decorator(func):
            func._is_replicate_end = True
            return func
        return decorator

replicate = ReplicateDecorator()

class BranchDecorator:
    @staticmethod
    def condition():
        def decorator(func):
            func._is_condition_task = True
            return func
        return decorator

    @staticmethod
    def on_if():
        def decorator(func):
            func._is_if_branch = True
            return func
        return decorator

    @staticmethod
    def on_else():
        def decorator(func):
            func._is_else_branch = True
            return func
        return decorator

    @staticmethod
    def continuation():
        def decorator(func):
            func._is_continuation_task = True
            return func
        return decorator

branch = BranchDecorator()

class ScriptDecorator:
    def __init__(self):
        self.languages = [
            'python', 'groovy', 'bash', 'shell', 'r', 'powershell', 'perl', 'ruby',
            'windows_cmd', 'javascript', 'scalaw', 'docker_compose', 'dockerfile',
            'kubernetes', 'php', 'vbscript', 'jython'
        ]
        for lang in self.languages:
            setattr(self, lang, self.create_decorator(lang))

    def create_decorator(self, language):
        def decorator(func):
            @wraps(func)
            def wrapper():
                return func()
            wrapper.language = language
            return wrapper
        return decorator

def task(name=None, depends_on=None, language='Python', runtime_env=None, virtual_env=None, input_files=None, output_files=None, prescript=None, postscript=None):
    """
    Decorator to define a ProActive task.

    :param name: Optional name for the task. If not provided, the function name will be used.
    :param depends_on: Optional list of task names that this task depends on.
    :param language: Language of the task (e.g., 'Python', 'Groovy', etc.). Default is 'Python'.
    :param runtime_env: Optional dictionary defining the runtime environment settings for the task.
    :param virtual_env: Optional dictionary defining the virtual environment settings for the task.
        - requirements (list): List of Python packages to install in the virtual environment.
        - basepath (str): Base path where the virtual environment will be created.
        - name (str): Name of the virtual environment directory.
        - verbosity (bool): If True, enables verbose output.
        - overwrite (bool): If True, overwrites the existing virtual environment.
        - install_requirements_if_exists (bool): If True, installs requirements even if the virtual environment already exists.
        - requirements_file (str): File containing the list of requirements.
    :param input_files: Optional list of files to transfer to the task environment.
    :param output_files: Optional list of output files to be retrieved after task execution.
    :param prescript: Optional pre-script function to execute before the task.
    :param postscript: Optional post-script function to execute after the task.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Store the task definition for later use when building the job
            task_def = {
                'Name': name if name else func.__name__,
                'Language': language,
                'Func': func,
                'Args': args,
                'Kwargs': kwargs,
                'DependsOn': depends_on,
                'RuntimeEnv': runtime_env,
                'VirtualEnv': virtual_env,
                'InputFiles': input_files,
                'OutputFiles': output_files,
                'Prescript': prescript,
                'Postscript': postscript,
                'IsLoopStart': getattr(func, '_is_loop_start', False),
                'IsLoopEnd': getattr(func, '_is_loop_end', False),
                'LoopCriteria': getattr(func, '_loop_criteria', None),
                'IsReplicateStart': getattr(func, '_is_replicate_start', False),
                'IsReplicateEnd': getattr(func, '_is_replicate_end', False),
                'ReplicateCriteria': getattr(func, '_replicate_criteria', None),
                'IsConditionTask': getattr(func, '_is_condition_task', False),
                'IsIfBranch': getattr(func, '_is_if_branch', False),
                'IsElseBranch': getattr(func, '_is_else_branch', False),
                'IsContinuationTask': getattr(func, '_is_continuation_task', False),
            }
            registered_tasks.append(task_def)
            # Execute the function as normal
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Adding specific language decorators dynamically to the TaskDecorator class
task.python = TaskDecorator(language=ProactiveScriptLanguage().python())
task.groovy = TaskDecorator(language=ProactiveScriptLanguage().groovy())
task.bash = TaskDecorator(language=ProactiveScriptLanguage().bash())
task.shell = TaskDecorator(language=ProactiveScriptLanguage().shell())
task.r = TaskDecorator(language=ProactiveScriptLanguage().r())
task.powershell = TaskDecorator(language=ProactiveScriptLanguage().powershell())
task.perl = TaskDecorator(language=ProactiveScriptLanguage().perl())
task.ruby = TaskDecorator(language=ProactiveScriptLanguage().ruby())
task.cmd = TaskDecorator(language=ProactiveScriptLanguage().windows_cmd())
task.javascript = TaskDecorator(language=ProactiveScriptLanguage().javascript())
task.scalaw = TaskDecorator(language=ProactiveScriptLanguage().scalaw())
task.docker_compose = TaskDecorator(language=ProactiveScriptLanguage().docker_compose())
task.dockerfile = TaskDecorator(language=ProactiveScriptLanguage().dockerfile())
task.kubernetes = TaskDecorator(language=ProactiveScriptLanguage().kubernetes())
task.php = TaskDecorator(language=ProactiveScriptLanguage().php())
task.vbscript = TaskDecorator(language=ProactiveScriptLanguage().vbscript())
task.jython = TaskDecorator(language=ProactiveScriptLanguage().jython())

# Define pre-script and post-script as part of the task module
task.prescript = ScriptDecorator()
task.postscript = ScriptDecorator()

def job(name, print_job_output=True):
    """
    Decorator to define a ProActive job.

    :param name: Name of the job.
    :param print_job_output: Boolean to determine if job output should be printed.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Initialize ProActive gateway
            gateway = getProActiveGateway()

            # Create a new job
            job = gateway.createJob(job_name=name)

            # Execute the decorated function to register tasks
            func(*args, **kwargs)

            # Dictionary to store task objects for dependency and loop setup
            task_objects = {}

            # Add registered tasks to the job
            start_task = None
            end_task = None
            replicate_start_task = None
            replicate_end_task = None
            condition_task = None
            if_task = None
            else_task = None
            continuation_task = None

            for task_def in registered_tasks:
                # Create the task according to the specified language
                if task_def['Language'].lower() == 'python':
                    task = gateway.createPythonTask(task_name=task_def['Name'])
                else:
                    task = gateway.createTask(language=task_def['Language'], task_name=task_def['Name'])

                # Check if the task was created successfully
                if task is None:
                    print(f"Error: Failed to create task '{task_def['Name']}' with language '{task_def['Language']}'.")
                    continue

                # Execute the task function to get the script content
                script_content = task_def['Func'](*task_def['Args'], **task_def['Kwargs'])

                # Set the script implementation for the task
                try:
                    task.setTaskImplementation(script_content)
                except AttributeError as e:
                    print(f"Error: Failed to set implementation for task '{task_def['Name']}'. Task is None or the method failed.")
                    print(f"Exception details: {e}")
                    continue

                 # Set the runtime environment if provided
                # Parameters:
                # - type (str): Specifies the type of container technology to use for running the task. 
                # Options include "docker", "podman", "singularity", or any other value to indicate a non-containerized execution.
                # - image (str): The container image to use for running the task. Ensure that the 'py4j' Python package is available in the specified image.
                # - nvidia_gpu (bool): Whether to enable NVIDIA GPU support within the container. Automatically set to False if no NVIDIA GPUs are present.
                # - mount_host_path (str): The host machine path to mount into the container, providing the container access to specific directories or files from the host.
                # - mount_container_path (str): The path inside the container where the host's file system (or a part of it) specified by `mount_host_path` will be accessible.
                # - rootless (bool): Enables or disables rootless mode for the container execution, applicable to all container types (default False).
                # - isolation (bool): Enables or disables isolation mode specifically for Singularity containers (default False). This parameter is only applicable if 'type' is set to "singularity".
                # - no_home (bool): When set to True, the user's home directory is not mounted inside the container if the home directory is not the current working directory. Only applicable to Singularity containers (default False).
                # - host_network (bool): Configures the container to use the host's network stack directly, bypassing the default or custom network namespaces (default False).
                # - verbose (bool): Enables verbose output for the container runtime environment setup process (default False).
                if task_def['RuntimeEnv']:
                    task.setRuntimeEnvironment(
                        type=task_def['RuntimeEnv'].get('type'),
                        image=task_def['RuntimeEnv'].get('image'),
                        nvidia_gpu=task_def['RuntimeEnv'].get('nvidia_gpu'),
                        mount_host_path=task_def['RuntimeEnv'].get('mount_host_path'),
                        mount_container_path=task_def['RuntimeEnv'].get('mount_container_path'),
                        rootless=task_def['RuntimeEnv'].get('rootless'),
                        isolation=task_def['RuntimeEnv'].get('isolation'),
                        no_home=task_def['RuntimeEnv'].get('no_home'),
                        host_network=task_def['RuntimeEnv'].get('host_network'),
                        verbose=str(task_def['RuntimeEnv'].get('verbose')).lower() if task_def['RuntimeEnv'].get('verbose') is not None else None
                    )

                # Set the virtual environment if provided
                if task_def['VirtualEnv']:
                    ve = task_def['VirtualEnv']
                    if 'requirements' in ve:
                        task.setVirtualEnv(
                            requirements=ve.get('requirements', []),
                            basepath=ve.get('basepath', "./"),
                            name=ve.get('name', "venv"),
                            verbosity=ve.get('verbosity', False),
                            overwrite=ve.get('overwrite', False),
                            install_requirements_if_exists=ve.get('install_requirements_if_exists', False)
                        )
                    if 'requirements_file' in ve:
                        task.setVirtualEnvFromFile(
                            requirements_file=ve.get('requirements_file'),
                            basepath=ve.get('basepath', "./"),
                            name=ve.get('name', "venv"),
                            verbosity=ve.get('verbosity', False),
                            overwrite=ve.get('overwrite', False),
                            install_requirements_if_exists=ve.get('install_requirements_if_exists', False)
                        )

                # Set input files if provided
                if task_def['InputFiles']:
                    for file in task_def['InputFiles']:
                        task.addInputFile(file)

                # Set output files if provided
                if task_def['OutputFiles']:
                    for file in task_def['OutputFiles']:
                        task.addOutputFile(file)

                # Set pre-script if provided
                if task_def['Prescript']:
                    pre_script = gateway.createPreScript(getattr(ProactiveScriptLanguage(), task_def['Prescript'].language)())
                    pre_script.setImplementation(task_def['Prescript']())
                    task.setPreScript(pre_script)

                # Set post-script if provided
                if task_def['Postscript']:
                    post_script = gateway.createPostScript(getattr(ProactiveScriptLanguage(), task_def['Postscript'].language)())
                    post_script.setImplementation(task_def['Postscript']())
                    task.setPostScript(post_script)

                job.addTask(task)
                task_objects[task_def['Name']] = task

                # Set loop start and end blocks
                if task_def.get('IsLoopStart'):
                    start_task = task
                    start_task.setFlowBlock(ProactiveFlowBlock().start())
                if task_def.get('IsLoopEnd'):
                    end_task = task
                    end_task.setFlowBlock(ProactiveFlowBlock().end())
                    if task_def['LoopCriteria']:
                        loop_script = gateway.createLoopFlowScript(
                            task_def['LoopCriteria'],
                            start_task.getTaskName(),
                            script_language=ProactiveScriptLanguage().python()
                        )
                        end_task.setFlowScript(loop_script)

                # Set replicate start and end blocks
                if task_def.get('IsReplicateStart'):
                    replicate_start_task = task
                    replicate_start_task.setFlowBlock(ProactiveFlowBlock().start())
                    replicate_script = gateway.createReplicateFlowScript(
                        task_def['ReplicateCriteria'],
                        script_language=ProactiveScriptLanguage().python()
                    )
                    replicate_start_task.setFlowScript(replicate_script)

                if task_def.get('IsReplicateEnd'):
                    replicate_end_task = task
                    replicate_end_task.setFlowBlock(ProactiveFlowBlock().end())

                # Set condition, branch, and continuation tasks
                if task_def.get('IsConditionTask'):
                    condition_task = task
                    # Set the branch script directly from the function's script content
                    branch_script = script_content
                elif task_def.get('IsIfBranch'):
                    if_task = task
                elif task_def.get('IsElseBranch'):
                    else_task = task
                elif task_def.get('IsContinuationTask'):
                    continuation_task = task

            # Add branch flow if all necessary tasks are present
            if condition_task and if_task and else_task and continuation_task:
                if not branch_script:
                    raise ValueError("Branch script must be defined for the condition task to determine the flow.")

                flow_script = gateway.createBranchFlowScript(
                    branch_script,
                    if_task.getTaskName(),
                    else_task.getTaskName(),
                    continuation_task.getTaskName(),
                    script_language=ProactiveScriptLanguage().python()
                )
                condition_task.setFlowScript(flow_script)

            # Set task dependencies
            for task_def in registered_tasks:
                if task_def['DependsOn']:
                    current_task = task_objects.get(task_def['Name'])
                    if current_task:
                        for dependency_name in task_def['DependsOn']:
                            dependency_task = task_objects.get(dependency_name)
                            if dependency_task:
                                current_task.addDependency(dependency_task)

            # Submit the job and get the job ID
            if any(task_def['InputFiles'] or task_def['OutputFiles'] for task_def in registered_tasks):
                job_id = gateway.submitJobWithInputsAndOutputsPaths(job)
            else:
                job_id = gateway.submitJob(job)
            print(f"Job submitted with ID: {job_id}")

            # Print job output if requested
            if print_job_output:
                print("Getting job output...")
                job_output = gateway.getJobOutput(job_id)
                print(f"Job output:\n{job_output}")

            # Clear the registered tasks list for the next job
            registered_tasks.clear()

            # Close the gateway connection
            gateway.close()
            print("Disconnected and finished.")
        return wrapper
    return decorator