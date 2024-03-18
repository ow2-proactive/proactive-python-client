from .ProactiveGateway import *
from .ProactiveRestApi import *
from .ProactiveUtils import *
from .ProactiveFactory import *
from .ProactiveBuilder import *

from .model.ProactiveScript import *
from .model.ProactiveForkEnv import *
from .model.ProactiveSelectionScript import *
from .model.ProactiveScriptLanguage import *
from .model.ProactiveTask import *
from .model.ProactiveJob import *

import os
version_file = os.path.join(os.path.dirname(__file__), '..', 'VERSION')

with open(version_file) as vf:
    __version__ = vf.read().strip()

from dotenv import load_dotenv
load_dotenv()

import getpass

def getProActiveGateway():
    """
    Gateway Helper for Proactive
    Automatically loads a local .env file looking for the PROACTIVE_URL, PROACTIVE_USERNAME and PROACTIVE_PASSWORD.
    If the .env file does not exists, ask the user to enter the Proactive server URL (using try.activeeon.com by default) as well as the user name and password.
    """
    print("Logging on proactive-server...")
    proactive_url = os.getenv("PROACTIVE_URL")
    if not proactive_url:
        proactive_url = input("Server (default: https://try.activeeon.com:8443): ")
    if proactive_url == "":
        proactive_url  = "https://try.activeeon.com:8443"
    if not proactive_url.startswith("http"):
        proactive_url  = "https://"+proactive_url+".activeeon.com:8443"
    print("Connecting on: " + proactive_url)
    gateway = ProActiveGateway(base_url=proactive_url)
    username = os.getenv("PROACTIVE_USERNAME")
    password = os.getenv("PROACTIVE_PASSWORD")
    if not (username and password):
        username = input("Login: ")
        password = getpass.getpass(prompt="Password: ")
    gateway.connect(username, password)
    assert gateway.isConnected(), "Failed to connect to the ProActive server!"
    print("Connected")
    return gateway
