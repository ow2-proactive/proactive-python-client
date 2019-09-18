class ProactiveFlowActionType:
    """
    Represents a proactive flow block

    blockType (string)

    """

    flow_action_types = {'CONTINUE': 'continue',
                         'IF': 'if',
                         'REPLICATE': 'replicate',
                         'LOOP': 'loop'}

    def replicate(self):
        return self.flow_action_types['REPLICATE']

