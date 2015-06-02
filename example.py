import time
from scheduler import Scheduler

if __name__ == '__main__':
    base_url = "http://localhost:8080"
    username = 'admin'
    password = 'admin'
    path_to_job_file = 'job.xml'

    scheduler = Scheduler(base_url)
    session_id = scheduler.login(username, password)

    print("Logged in with session id %s" % session_id)
    job_id = scheduler.submit_job(session_id, path_to_job_file)

    print("Job %s submitted" % job_id)

    job_status = ''
    while job_status != 'FINISHED':
        job = scheduler.get_job(session_id, job_id)
        job_status = job['jobInfo']['status']
        (running, total) = scheduler.get_job_progress(job)

        print("Progress %s/%s" % (running, total))

        if job_status != 'FINISHED':
            time.sleep(1)

    print('Job %s finished' % job_id)
