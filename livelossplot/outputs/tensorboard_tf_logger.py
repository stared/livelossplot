from datetime import datetime
from os import path

from livelossplot.main_logger import MainLogger
from livelossplot.outputs.base_output import BaseOutput


class TensorboardTFLogger(BaseOutput):
    """
    Class write logs to TensorBoard (from TensorFlow).
    """
    def __init__(self, logdir="./tensorboard_logs/", run_id=None):
        """
        Args:
            logdir: dir where TensorBoard events will be written
            run_id: name for log id, otherwise it usses datetime
        """
        from tensorflow import summary
        self.summary = summary
        run_id = datetime.now().isoformat()[:-7].replace("T", " ").replace(":", "_") if run_id is None else run_id
        self._path = path.join(logdir, run_id)
        self.writer = summary.create_file_writer(self._path)

    def close(self):
        """Close tensorboard writer"""
        self.writer.close()

    def log_scalar(self, name: str, value: float, global_step: int):
        """
        Args:
            name: name of metric
            value: float value of metric
            global_step: current step of the training loop
        """
        with self.writer.as_default():
            self.summary.scalar(name, value, step=global_step)
        self.writer.flush()

    def send(self, logger: MainLogger):
        """Take log history from logger and store it in tensorboard event"""
        for name, log_items in logger.log_history.items():
            last_log_item = log_items[-1]
            self.log_scalar(name, last_log_item.value, last_log_item.step)
