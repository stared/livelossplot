from livelossplot.main_logger import MainLogger


class BaseOutput:
    def send(self, logger: MainLogger):
        """Abstract method - handle logs for a plugin"""
        raise NotImplementedError()

    def close(self):
        """Overwrite it with last steps"""
        pass
