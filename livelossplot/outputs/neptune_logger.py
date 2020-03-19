from livelossplot.main_logger import MainLogger
from livelossplot.outputs.base_output import BaseOutput


class NeptuneLogger(BaseOutput):
    """See: https://github.com/neptune-ai/neptune-client
    YOUR_API_TOKEN and USERNAME/PROJECT_NAME
    """
    def __init__(self, api_token: str, project_qualified_name: str):
        """Set secrets and create experiment"""
        import neptune
        self.neptune = neptune
        self.neptune.init(api_token=api_token, project_qualified_name=project_qualified_name)
        self.neptune.create_experiment()

    def close(self):
        """Close connection"""
        self.neptune.stop()

    def send(self, logger: MainLogger):
        """Send collected metrics to neptune server"""
        for name, log_items in logger.log_history.items():
            last_log_item = log_items[-1]
            self.neptune.send_metric(name, x=last_log_item.step, y=last_log_item.value)
