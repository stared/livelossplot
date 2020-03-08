class BaseOutput:
    def send(self, *args, **kwargs):
        raise NotImplementedError()
