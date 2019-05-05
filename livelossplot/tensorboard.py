import tensorflow as tf
from datetime import datetime
from os import path

class TensorboardLogger:
    def __init__(self, logdir="./tensorboard_logs/"):
        time_str = datetime.now().isoformat()[:-7].replace("T", " ")
        self._path = path.join(logdir, time_str)
        self.writer = tf.summary.FileWriter(self._path)

    def close(self):
        self.writer.close()

    def log_scalar(self, tag, value, global_step):
        summary = tf.Summary()
        summary.value.add(tag=tag, simple_value=value)
        self.writer.add_summary(summary, global_step=global_step)
        self.writer.flush()

    def log_logs(self, logs, global_step):
        for k, v in logs.items():
            self.log_scalar(k, v, global_step)

