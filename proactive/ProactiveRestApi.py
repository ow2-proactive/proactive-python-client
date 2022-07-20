import getpass
import requests

from .ProactiveUtils import convert_palist_to_list


class ProactiveRestApi:

    def __init__(self):
        self.base_url = None
        self.username = None
        self.password = None
        self.session_id = None

    def init(self, connectionInfo):
        """
        https://doc.activeeon.com/javadoc/latest/org/ow2/proactive/scheduler/smartproxy/common/AbstractSmartProxy.html#connectionInfo
        https://doc.activeeon.com/javadoc/latest/org/ow2/proactive/authentication/ConnectionInfo.html
        """
        base_url = connectionInfo.getUrl()
        username = connectionInfo.getLogin()
        password = connectionInfo.getPassword()
        return self.login(base_url, username, password)

    def login(self, base_url, username=None, password=None):
        """
        https://try.activeeon.com/doc/rest/
        https://try.activeeon.com/doc/rest/#1001654576
        https://try.activeeon.com/doc/rest/#-1881814800
        curl -X POST -d "username=$username&password=$password" https://try.activeeon.com:8443/rest/rm/login
        curl -X POST -d "username=$username&password=$password" https://try.activeeon.com:8443/rest/common/login
        """
        print("[INFO] Log in...")
        assert(base_url is not None)
        self.base_url = base_url
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
        response = requests.post(api_url, data=api_url_data)
        if response.status_code == 200:
            print("[INFO] Connected!")
            self.session_id = response.text
            return True
        else:
            print("[ERROR] Login error, please check your username and password!")
            self.session_id = None
            return False

    def reconnect(self):
        self.disconnect()
        self.connect()

    def connected(self):
        """
        https://try.activeeon.com/doc/rest/#-1702945797
        """
        if self.session_id is not None:
            # print("[INFO] Checking connection...")
            api_url = self.base_url + "/common/connected"
            api_url_headers = {"sessionid": self.session_id}
            response = requests.get(api_url, headers=api_url_headers)
            if response.status_code == 200 and response.text == "true":
                # print("[INFO] Connected!")
                return True
            else:
                # print("[INFO] Not connected!")
                return False
        else:
            return False

    def get_rm_model_hosts(self):
        """
        https://try.activeeon.com/doc/rest/#-279015793
        """
        hosts = []
        if self.connected():
            api_url = self.base_url + "/rm/model/hosts"
            response = requests.get(api_url)
            print(response.status_code, response.text)
            if response.status_code == 200:
                hosts = convert_palist_to_list(response.text)
        else:
            print("[ERROR] You are not connected!")
        return hosts

    def get_rm_model_nodesources(self):
        """
        https://try.activeeon.com/doc/rest/#-1865954534
        """
        nodesources = []
        if self.connected():
            api_url = self.base_url + "/rm/model/nodesources"
            response = requests.get(api_url)
            print(response.status_code, response.text)
            if response.status_code == 200:
                nodesources = convert_palist_to_list(response.text)
        else:
            print("[ERROR] You are not connected!")
        return nodesources

    def get_rm_model_tokens(self):
        """
        https://try.activeeon.com/doc/rest/#283742038
        """
        tokens = []
        if self.connected():
            api_url = self.base_url + "/rm/model/tokens"
            response = requests.get(api_url)
            print(response.status_code, response.text)
            if response.status_code == 200:
                tokens = convert_palist_to_list(response.text)
        else:
            print("[ERROR] You are not connected!")
        return tokens

    def logout(self):
        if self.connected():
            print("[INFO] Disconnecting...")
            api_url = self.base_url + "/common/logout"
            api_url_headers = {"sessionid": self.session_id}
            response = requests.put(api_url, headers=api_url_headers)
            if response.status_code == 204:
                print("[INFO] Done.")
                self.session_id = None
                return True
            else:
                print("[ERROR] Error while disconnecting.")
                return False
        else:
            print("[ERROR] You are not connected!")

    def disconnect(self):
        return self.logout()


if __name__ == '__main__':
    restapi = ProactiveRestApi()
    restapi.login("https://try.activeeon.com:8443/rest")
    print("connected:", restapi.connected())
    # ...
    print(restapi.get_rm_model_hosts())
    print(restapi.get_rm_model_nodesources())
    print(restapi.get_rm_model_tokens())
    # ...
    restapi.logout()
    print("connected:", restapi.connected())

"""
$ python3 ProactiveRestApi.py
[INFO] Log in...
[INFO] Connected!
connected: True
200 PA:LIST(,trydev2.activeeon.com)
['', 'trydev2.activeeon.com']
200 PA:LIST(,Default,OpenStack,local,VMware,AmazonAWS,IbmSoftlayer,GoogleCloudCompute,AmazonAWS-Spot,AzureK8Scluster,AzureDirectVMs,AzureScaleSet,GPU,LocalDynamic,Kubernetes)
['', 'Default', 'OpenStack', 'local', 'VMware', 'AmazonAWS', 'IbmSoftlayer', 'GoogleCloudCompute', 'AmazonAWS-Spot', 'AzureK8Scluster', 'AzureDirectVMs', 'AzureScaleSet', 'GPU', 'LocalDynamic', 'Kubernetes']
200 PA:REGEXP(^$)
[]
[INFO] Disconnecting...
[INFO] Done.
connected: False
"""
