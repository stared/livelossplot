from datetime import datetime
from os import path

from livelossplot.main_logger import MainLogger
from livelossplot.outputs.base_output import BaseOutput


class TensorboardLogger(BaseOutput):
    """
    Class write logs to TensorBoard (using pure TensorBoard, not one from TensorFlow).
    """
    def __init__(self, logdir="./tensorboard_logs/", run_id=None):
        """
        :param logdir: dir where TensorBoard events will be written
        :param run_id: name for log id, otherwise it usses datetime
        """
        from tensorboard import summary
        self.summary = summary
        time_str = datetime.now().isoformat()[:-7].replace("T", " ").replace(":", "_")
        self._path = path.join(logdir, time_str)
        self.writer = summary.create_file_writer(self._path)

    def close(self):
        """Close tensorboard writer"""
        self.writer.close()

    def log_scalar(self, name: str, value: int, global_step: float):
        """
        :param name: name of metric
        :param value: float value of metric
        :param global_step: current step of the training loop
        :return:
        """
        with self.writer.as_default():
            self.summary.scalar(name, value, step=global_step)
        self.writer.flush()

    def send(self, logger: MainLogger):
        """Take log history from logger and store it in tensorboard event"""
        for name, log_items in logger.log_history.items():
            last_log_item = log_items[-1]
            self.log_scalar(name, last_log_item.value, last_log_item.step)
