import requests


class Scheduler:
    def __init__(self, base_url):
        self.base_url = base_url

    def login(self, username, password):
        payload = {'username': username, 'password': password}
        r = requests.post("%s/rest/scheduler/login" % self.base_url, data=payload)

        if r.status_code != requests.codes.ok:
            raise Exception("Failed to login: %s" % r.text)

        return r.text


    def submit_job(self, session_id, path_to_job_file):
        headers = {'sessionid': session_id}
        files = {'file': ('job.xml', open('%s' % path_to_job_file, 'rb'), 'application/xml')}
        r = requests.post("%s/rest/scheduler/submit" % self.base_url, headers=headers, files=files)

        if r.status_code != requests.codes.ok:
            raise Exception("Failed to submit job: %s" % r.text)

        return r.json()['id']


    def get_job(self, session_id, job_id):
        headers = {'sessionid': session_id}
        r = requests.get("%s/rest/scheduler/jobs/%s" % (self.base_url, job_id), headers=headers)

        if r.status_code != requests.codes.ok:
            raise Exception("Failed to retrieve job state: %s" % r.text)

        return r.json()


    @staticmethod
    def get_job_progress(job):
        return (job['jobInfo']['numberOfFinishedTasks'], job['jobInfo']['totalNumberOfTasks'])

