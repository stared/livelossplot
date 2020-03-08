from datetime import datetime
from os import path

import tensorflow as tf

from livelossplot.main_logger import MainLogger
from livelossplot.output_plugins.base_output import BaseOutput


class TensorboardLogger(BaseOutput):
    """TODO: Make a class also for TensorboardX."""

    def __init__(self, logdir="./tensorboard_logs/"):
        time_str = datetime.now().isoformat()[:-7].replace("T", " ").replace(":", "_")
        self._path = path.join(logdir, time_str)
        self.writer = tf.summary.create_file_writer(self._path)

    def close(self):
        self.writer.close()

    def log_scalar(self, name: str, value: int, global_step: float):
        with self.writer.as_default():
            tf.summary.scalar(name, value, step=global_step)
        self.writer.flush()

    def send(self, logger: MainLogger):
        for name, log_items in logger.log_history.items():
            last_log_item = log_items[-1]
            self.log_scalar(name, last_log_item.value, last_log_item.step)
