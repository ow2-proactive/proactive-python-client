import os

from .ProactiveScript import *


class ProactiveSelectionScript(ProactiveScript):
    """
    Represents a proactive selection script

    script_language (ProactiveScriptLanguage)
    implementation (string)
    is_dynamic (boolean
    """

    def __init__(self, script_language):
        super(ProactiveSelectionScript, self).__init__(script_language)
        self.is_dynamic = True

    def setIsDynamic(self, is_dynamic):
        self.is_dynamic = is_dynamic

    def isDynamic(self):
        return self.is_dynamic

