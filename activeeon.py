import requests


class Proactive:
    """
    Simple client for the ProActive scheduler REST API
    See also https://try.activeeon.com/rest/doc/jaxrsdocs/overview-summary.html
    """

    def __init__(self, base_url):
        """
        :param base_url: REST API base URL including host and port, for instance http://localhost:8080
        """
        self.base_url = base_url

    def pa_connect(self, username, password):
        payload = {'username': username, 'password': password}
        r = requests.post("%s/rest/scheduler/login" % self.base_url, data=payload)

        if r.status_code != requests.codes.ok:
            raise Exception("Failed to login: %s" % r.text)

        return r.text


    def pa_submit_job(self, session_id, path_to_job_file):
        headers = {'sessionid': session_id}
        files = {'file': ('job.xml', open('%s' % path_to_job_file, 'rb'), 'application/xml')}
        r = requests.post("%s/rest/scheduler/submit" % self.base_url, headers=headers, files=files)

        if r.status_code != requests.codes.ok:
            raise Exception("Failed to submit job: %s" % r.text)

        return r.json()['id']


    def pa_get_job(self, session_id, job_id):
        headers = {'sessionid': session_id}
        r = requests.get("%s/rest/scheduler/jobs/%s" % (self.base_url, job_id), headers=headers)

        if r.status_code != requests.codes.ok:
            raise Exception("Failed to retrieve job state: %s" % r.text)

        return r.json()


    @staticmethod
    def pa_get_job_progress(job):
        return (job['jobInfo']['numberOfFinishedTasks'], job['jobInfo']['totalNumberOfTasks'])

    @staticmethod
    def pa_get_task_progress(job, task_id):
        return job['tasks'][task_id]['taskInfo']['progress']

