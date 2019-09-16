from .ProactiveFlowActionType import *
from .ProactiveScript import *


class ProactiveFlowScript(ProactiveScript):
    """
    Represents a proactive flow script

    script_language (ProactiveScriptLanguage)
    implementation (string)
    """

    def __init__(self, script_language):
        super(ProactiveFlowScript, self).__init__(script_language)
        self.proactive_action_type = None

    def setActionType(self, action_type):
        self.proactive_action_type = action_type

    def getActionType(self):
        return self.proactive_action_type

    def isReplicateFlowScript(self):
        return True if self.getActionType() == ProactiveFlowActionType().replicate() else False
