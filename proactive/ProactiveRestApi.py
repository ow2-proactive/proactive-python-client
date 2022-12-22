import getpass
import requests
import json
import ssl
import warnings
import contextlib

from urllib3.exceptions import InsecureRequestWarning
from .ProactiveUtils import convert_palist_to_list


old_merge_environment_settings = requests.Session.merge_environment_settings
@contextlib.contextmanager
def no_ssl_verification():
    opened_adapters = set()
    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        # Verification happens only once per connection so we need to close
        # all the opened adapters once we're done. Otherwise, the effects of
        # verify=False persist beyond the end of this context manager.
        opened_adapters.add(self.get_adapter(url))
        settings = old_merge_environment_settings(self, url, proxies, stream, verify, cert)
        settings['verify'] = False
        return settings
    requests.Session.merge_environment_settings = merge_environment_settings
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', InsecureRequestWarning)
            yield
    finally:
        requests.Session.merge_environment_settings = old_merge_environment_settings
        for adapter in opened_adapters:
            try:
                adapter.close()
            except:
                pass


class ProactiveRestApi:

    def __init__(self):
        self.base_url = None
        self.username = None
        self.password = None
        self.session_id = None
        self.debug = False

    def init(self, connectionInfo):
        base_url = connectionInfo.getUrl()
        username = connectionInfo.getLogin()
        password = connectionInfo.getPassword()
        return self.login(base_url, username, password)

    def login(self, base_url, username=None, password=None):
        if self.debug: print("[INFO] Log in...")
        assert(base_url is not None)
        self.base_url = base_url
        if self.debug: print("base_url: ", self.base_url)
        if self.connected():
            self.logout()
        if username is None:
            username = input('Login: ')
        if password is None:
            password = getpass.getpass(prompt='Password: ')
        self.username = username
        self.password = password
        return self.connect()

    def connect(self):
        api_url = self.base_url + "/common/login"
        api_url_data = {"username": self.username, "password": self.password}
        with no_ssl_verification():
            response = requests.post(api_url, data=api_url_data)
            if response.status_code == 200:
                if self.debug: print("[INFO] Connected!")
                self.session_id = response.text
                return True
            else:
                if self.debug: print("[ERROR] Login error, please check your username and password!")
                self.session_id = None
                return False

    def reconnect(self):
        self.disconnect()
        self.connect()

    def connected(self):
        if self.session_id is not None:
            if self.debug: print("[INFO] Checking connection...")
            api_url = self.base_url + "/common/connected"
            api_url_headers = {"sessionid": self.session_id}
            with no_ssl_verification():
                response = requests.get(api_url, headers=api_url_headers)
                if response.status_code == 200 and response.text == "true":
                    if self.debug: print("[INFO] Connected!")
                    return True
                else:
                    if self.debug: print("[INFO] Not connected!")
                    return False
        else:
            return False

    def get_rm_model_hosts(self):
        hosts = []
        if self.connected():
            api_url = self.base_url + "/rm/model/hosts"
            with no_ssl_verification():
                response = requests.get(api_url)
                if self.debug: print(response.status_code, response.text)
                if response.status_code == 200:
                    hosts = convert_palist_to_list(response.text)
        else:
            if self.debug: print("[ERROR] You are not connected!")
        return hosts

    def get_rm_model_nodesources(self):
        nodesources = []
        if self.connected():
            api_url = self.base_url + "/rm/model/nodesources"
            with no_ssl_verification():
                response = requests.get(api_url)
                if self.debug: print(response.status_code, response.text)
                if response.status_code == 200:
                    nodesources = convert_palist_to_list(response.text)
        else:
            if self.debug: print("[ERROR] You are not connected!")
        return nodesources

    def get_rm_model_tokens(self):
        tokens = []
        if self.connected():
            api_url = self.base_url + "/rm/model/tokens"
            with no_ssl_verification():
                response = requests.get(api_url)
                if self.debug: print(response.status_code, response.text)
                if response.status_code == 200:
                    tokens = convert_palist_to_list(response.text)
        else:
            if self.debug: print("[ERROR] You are not connected!")
        return tokens

    def get_job_log_full(self, job_id):
        log = None
        if self.connected():
            api_url = self.base_url + "/scheduler/jobs/{}/log/full".format(job_id)
            api_url_headers = {"sessionid": self.session_id}
            with no_ssl_verification():
                response = requests.get(api_url, headers=api_url_headers)
                if self.debug: print(response.status_code, response.text)
                if response.status_code == 200:
                    log = response.text
        else:
            if self.debug: print("[ERROR] You are not connected!")
        return log
    
    def get_job_result(self, job_id):
        result = None
        if self.connected():
            api_url = self.base_url + "/scheduler/jobs/{}/result".format(job_id)
            api_url_headers = {"sessionid": self.session_id}
            with no_ssl_verification():
                response = requests.get(api_url, headers=api_url_headers)
                if self.debug: print(response.status_code, response.text)
                if response.status_code == 200:
                    result = json.loads(response.text)
        else:
            if self.debug: print("[ERROR] You are not connected!")
        return result

    def get_propagated_variable_from_job_result(self, job_id, task_name, variable_name):
        job_result = self.get_job_result(job_id)
        if job_result is not None:
            return job_result['allResults'][task_name]['propagatedVariables'][variable_name]
        else:
            return None

    def get_service_instances(self, filterBy=None):
        result = None
        if self.connected():
            api_url = self.base_url.replace("rest", "cloud-automation-service/serviceInstances")
            if self.debug: print("api_url: ", api_url)
            api_url_headers = {"sessionid": self.session_id}
            with no_ssl_verification():
                response = requests.get(api_url, headers=api_url_headers)
                if self.debug: print(response.status_code, response.text)
                if response.status_code == 200:
                    result = json.loads(response.text)
                    if filterBy is not None:
                        for key, value in filterBy.items():
                            result = [item for item in result if item[key] == value]
        else:
            if self.debug: print("[ERROR] You are not connected!")
        return result

    def get_active_service_instances(self, filterBy=None):
        result = None
        if self.connected():
            api_url = self.base_url.replace("rest", "cloud-automation-service/serviceInstances/active")
            if self.debug: print("api_url: ", api_url)
            api_url_headers = {"sessionid": self.session_id}
            with no_ssl_verification():
                response = requests.get(api_url, headers=api_url_headers)
                if self.debug: print(response.status_code, response.text)
                if response.status_code == 200:
                    result = json.loads(response.text)
                    if filterBy is not None:
                        for key, value in filterBy.items():
                            result = [item for item in result if item[key] == value]
        else:
            if self.debug: print("[ERROR] You are not connected!")
        return result

    def get_service_instance_by_id(self, instance_id):
        result = None
        if self.connected():
            api_url = self.base_url.replace("rest", "cloud-automation-service/serviceInstances/{}".format(instance_id))
            if self.debug: print("api_url: ", api_url)
            api_url_headers = {"sessionid": self.session_id}
            with no_ssl_verification():
                response = requests.get(api_url, headers=api_url_headers)
                if self.debug: print(response.status_code, response.text)
                if response.status_code == 200:
                    result = json.loads(response.text)
        else:
            if self.debug: print("[ERROR] You are not connected!")
        return result

    def get_service_deployment_endpoint_url(self, instance_id, deployment=0):
        result = self.get_service_instance_by_id(instance_id)
        service_endpoint_url = None
        if result is not None:
            service_endpoint = result['deployments'][deployment]['endpoint']
            if service_endpoint['proxyfied']:
                service_endpoint_url = service_endpoint['proxyfiedUrl']
            else:
                service_endpoint_url = service_endpoint['url']
        return service_endpoint_url

    def logout(self):
        if self.connected():
            if self.debug: print("[INFO] Disconnecting...")
            api_url = self.base_url + "/common/logout"
            api_url_headers = {"sessionid": self.session_id}
            with no_ssl_verification():
                response = requests.put(api_url, headers=api_url_headers)
                if response.status_code == 204:
                    if self.debug: print("[INFO] Done.")
                    self.session_id = None
                    return True
                else:
                    if self.debug: print("[ERROR] Error while disconnecting.")
                    return False
        else:
            if self.debug: print("[ERROR] You are not connected!")

    def set_enable_debug(self, debug_mode=True):
        self.debug = debug_mode

    def disconnect(self):
        return self.logout()
