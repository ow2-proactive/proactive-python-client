import time
import sys
from scheduler import Scheduler

if __name__ == '__main__':

    if len(sys.argv) != 5:
        sys.exit("4 arguments expected, <URL> <username> <password> <job XML file>")

    base_url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    path_to_job_file = sys.argv[4]

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
