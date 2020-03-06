class BaseOutput:
    def __init__(self):
        pass

    def send(self, *args, **kwargs):
        raise NotImplementedError()
