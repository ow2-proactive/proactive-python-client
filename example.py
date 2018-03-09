import time
import sys
from activeeon import Proactive

if __name__ == '__main__':

    if len(sys.argv) != 5:
        sys.exit("4 arguments expected, <URL> <username> <password> <job XML file>")

    base_url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    path_to_job_file = sys.argv[4]

    activeeon_cloud = Proactive(base_url)  
    
    session_id = activeeon_cloud.pa_connect(username, password)

    print("Logged in with session id %s" % session_id)
    job_id = activeeon_cloud.pa_submit_job(session_id, path_to_job_file)

    print("Job %s submitted" % job_id)

    job_status = ''
    while job_status != 'FINISHED' and job_status != 'KILLED' :
        job = activeeon_cloud.pa_get_job(session_id, job_id)
        job_status = job['jobInfo']['status']
        (running, total) = activeeon_cloud.pa_get_job_progress(job)

        print("Progress %s/%s" % (running, total))

        for task_id in list(job['tasks']):
            progress = activeeon_cloud.pa_get_task_progress(job, task_id)
            print("Task %s progression is: %s%%" % (job['tasks'][task_id]['name'], progress))

        if job_status != 'FINISHED':
            time.sleep(1)

    print('Job %s finished' % job_id)
