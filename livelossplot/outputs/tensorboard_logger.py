from datetime import datetime, timezone
from pathlib import Path

from livelossplot.main_logger import MainLogger
from livelossplot.outputs.base_output import BaseOutput


class TensorboardLogger(BaseOutput):
    """Write logs to TensorBoard via the standalone `tensorboard` package."""

    def __init__(self, logdir: str | Path = "./tensorboard_logs/", run_id: str | None = None):
        """
        Args:
            logdir: dir where TensorBoard events will be written.
            run_id: name for the run; defaults to the current timestamp.
        """
        from tensorboard import summary
        self.summary = summary
        if run_id is None:
            run_id = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H_%M_%S')
        self._path = Path(logdir) / run_id
        self.writer = summary.create_file_writer(str(self._path))

    def close(self) -> None:
        self.writer.close()

    def log_scalar(self, name: str, value: float, global_step: float) -> None:
        with self.writer.as_default():
            self.summary.scalar(name, value, step=global_step)
        self.writer.flush()

    def send(self, logger: MainLogger) -> None:
        for name, log_items in logger.log_history.items():
            last = log_items[-1]
            self.log_scalar(name, last.value, last.step)
