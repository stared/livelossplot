class BaseOutput:
    def send(self, *args, **kwargs):
        raise NotImplementedError()

    def close(self):
        pass
