class PipelineRuntimeError(RuntimeError):

    def __init__(self, msg):
        self.msg = msg