from .ProactiveScript import *


class ProactiveForkEnv(ProactiveScript):
    """
    Represents a generic proactive fork env script

    script_language (ProactiveScriptLanguage)
    implementation (string)
    java_home (string)
    """

    def __init__(self, script_language):
        super(ProactiveForkEnv, self).__init__(script_language)
        self.java_home = '/usr'

    def setJavaHome(self, java_home):
        self.java_home = java_home

    def getJavaHome(self):
        return self.java_home

