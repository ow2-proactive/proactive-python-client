import os


class ProactiveScript(object):
    """
    Represents a generic proactive script

    script_language (ProactiveScriptLanguage)
    implementation (string)
    """

    def __init__(self, script_language):
        self.script_language = script_language
        self.implementation = ''

    def setScriptLanguage(self, script_language):
        self.script_language = script_language

    def getScriptLanguage(self):
        return self.script_language

    def setImplementation(self, implementation):
        self.implementation = implementation

    def getImplementation(self):
        return self.implementation

    def setImplementationFromFile(self, script_file):
        if os.path.exists(script_file):
            with open(script_file, 'r') as content_file:
                self.implementation = content_file.read()


class ProactivePreScript(ProactiveScript):
    """
      Represent a pre-script for a proactive task
    """

    def __init__(self, script_language):
        super(ProactivePreScript, self).__init__(script_language)


class ProactivePostScript(ProactiveScript):
    """
      Represent a post-script for a proactive task
    """

    def __init__(self, script_language):
        super(ProactivePostScript, self).__init__(script_language)

