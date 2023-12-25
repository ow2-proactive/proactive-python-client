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
        self.implementation_url = None

    def setScriptLanguage(self, script_language):
        self.script_language = script_language

    def getScriptLanguage(self):
        return self.script_language

    def setImplementation(self, implementation):
        self.implementation = implementation
        self.implementation_url = None

    def getImplementation(self):
        return self.implementation

    def setImplementationFromFile(self, script_file):
        if os.path.exists(script_file):
            with open(script_file, 'r') as content_file:
                self.setImplementation(content_file.read())

    def setImplementationFromURL(self, implementation_url):
        self.implementation_url = implementation_url
        self.implementation = ''

    def getImplementationFromURL(self):
        return self.implementation_url


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

