class BaseOutput:
    def send(self, *args, **kwargs):
        """Abstract method - handle logs for a plugin"""
        raise NotImplementedError()

    def close(self):
        """Overwrite it with last steps"""
        pass
