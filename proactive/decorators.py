from functools import wraps
from proactive import getProActiveGateway

# Global list to store tasks defined by decorators
registered_tasks = []

def task(name=None, depends_on=None):
    """
    Decorator to define a ProActive task.
    
    :param name: Optional name for the task. If not provided, the function name will be used.
    :param depends_on: Optional list of task names that this task depends on.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Store the task definition for later use when building the job
            task_def = {
                'Name': name if name else func.__name__,
                'Language': 'Python',
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
                task = gateway.createPythonTask(task_name=task_def['Name'])
                
                # Execute the task function to get the script content
                script_content = task_def['Func'](*task_def['Args'], **task_def['Kwargs'])
                
                # Set the script implementation for the task
                task.setTaskImplementation(script_content)
                job.addTask(task)
                task_objects[task_def['Name']] = task
            
            # Set task dependencies
            for task_def in registered_tasks:
                if task_def['DependsOn']:
                    current_task = task_objects[task_def['Name']]
                    for dependency_name in task_def['DependsOn']:
                        if dependency_name in task_objects:
                            dependency_task = task_objects[dependency_name]
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