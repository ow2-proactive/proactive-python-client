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
