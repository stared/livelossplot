from abc import ABC, abstractmethod

from livelossplot.main_logger import MainLogger


class BaseOutput(ABC):
    @abstractmethod
    def send(self, logger: MainLogger):
        """Abstract method - handle logs for a plugin"""
        ...

    def close(self):
        """Overwrite it with last steps"""
        ...

    def set_output_mode(self, mode: str):
        """Some of output plugins needs to know target format"""
        assert mode in ('notebook', 'script')
        self._set_output_mode(mode)

    def _set_output_mode(self, mode: str):
        ...
