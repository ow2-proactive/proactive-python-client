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
        self.target = None
        self.targetElse = None
        self.targetContinuation = None

    def setActionType(self, action_type):
        self.proactive_action_type = action_type

    def getActionType(self):
        return self.proactive_action_type

    def setActionTarget(self, target):
        self.target = target

    def getActionTarget(self):
        return self.target

    def setActionTargetElse(self, target):
        self.targetElse = target

    def getActionTargetElse(self):
        return self.targetElse

    def setActionTargetContinuation(self, target):
        self.targetContinuation = target

    def getActionTargetContinuation(self):
        return self.targetContinuation

    def isReplicateFlowScript(self):
        return True if self.getActionType() == ProactiveFlowActionType().replicate() else False

    def isLoopFlowScript(self):
        return True if self.getActionType() == ProactiveFlowActionType().loop() else False

    def isBranchFlowScript(self):
        return True if self.getActionType() == ProactiveFlowActionType().branch() else False
