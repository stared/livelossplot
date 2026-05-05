from abc import ABC, abstractmethod
from typing import Literal

from livelossplot.main_logger import MainLogger

OutputMode = Literal['notebook', 'script']


class BaseOutput(ABC):
    @abstractmethod
    def send(self, logger: MainLogger) -> None:
        """Handle logs for a plugin"""

    def close(self) -> None:  # noqa: B027 — optional override hook
        """Run at the end of training, if needed"""

    def set_output_mode(self, mode: OutputMode) -> None:  # noqa: B027 — optional override hook
        """Notify plugin whether we're in a notebook or script context"""
