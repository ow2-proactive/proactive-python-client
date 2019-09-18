
class ProactiveFlowBlock:
    """
    Represents a proactive flow block

    blockType (string)

    """

    flow_block_types = {'NONE': 'none',
                        'START': 'start',
                        'END': 'end'}

    def none(self):
        return self.flow_block_types['NONE']

    def start(self):
        return self.flow_block_types['START']

    def end(self):
        return self.flow_block_types['END']
