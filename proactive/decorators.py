from functools import wraps
from proactive import getProActiveGateway

# Global list to store tasks defined by decorators
registered_tasks = []

def task(name=None, depends_on=None, language='Python'):
    """
    Decorator to define a ProActive task.

    :param name: Optional name for the task. If not provided, the function name will be used.
    :param depends_on: Optional list of task names that this task depends on.
    :param language: Language of the task (e.g., 'Python', 'Groovy', etc.). Default is 'Python'.
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
                'DependsOn': depends_on
            }
            registered_tasks.append(task_def)
            # Execute the function as normal
            return func(*args, **kwargs)
        return wrapper
    return decorator

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

            # Dictionary to store task objects for dependency management
            task_objects = {}

            # Add registered tasks to the job
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

                job.addTask(task)
                task_objects[task_def['Name']] = task

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