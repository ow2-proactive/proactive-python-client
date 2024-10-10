from functools import wraps
from proactive import getProActiveGateway

# List to store tasks defined by decorators
registered_tasks = []

# Decorator to define a task
def task(name=None, depends_on=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Store the function, args, and kwargs for later execution
            task_def = {
                'Name': name if name else func.__name__,
                'Language': 'Python',
                'Func': func,
                'Args': args,
                'Kwargs': kwargs,
                'DependsOn': depends_on
            }
            registered_tasks.append(task_def)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Decorator to define a job
def job(name, print_job_output=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            gateway = getProActiveGateway()

            job = gateway.createJob()
            job.setJobName(name)

            # Execute the function to register tasks
            func(*args, **kwargs)

            # Add the registered tasks to the job
            task_objects = {}
            for task_def in registered_tasks:
                task = gateway.createPythonTask(task_name=task_def['Name'])

                # Execute the stored function with args and kwargs to get the script content
                task_func = task_def['Func']
                args = task_def['Args']
                kwargs = task_def['Kwargs']
                script_content = task_func(*args, **kwargs)

                # Set the script implementation for the task
                task.setTaskImplementation(script_content)
                job.addTask(task)
                task_objects[task_def['Name']] = task

            # Set task dependencies based on the 'DependsOn' parameter
            for task_def in registered_tasks:
                if task_def['DependsOn']:
                    current_task = task_objects[task_def['Name']]
                    for dependency_name in task_def['DependsOn']:
                        if dependency_name in task_objects:
                            dependency_task = task_objects[dependency_name]
                            current_task.addDependency(dependency_task)

            # Submit the job
            job_id = gateway.submitJob(job)
            print(f"Job submitted with ID: {job_id}")

            if print_job_output:
                print("Getting job output...")
                job_output = gateway.getJobOutput(job_id)
                print(f"Job output:\n{job_output}")

            # Clear the registered tasks list for the next job
            registered_tasks.clear()

            # Cleanup
            gateway.close()
            print("Disconnected and finished.")

        return wrapper
    return decorator