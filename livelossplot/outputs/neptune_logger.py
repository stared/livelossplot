from typing import Optional
from livelossplot.main_logger import MainLogger
from livelossplot.outputs.base_output import BaseOutput


class NeptuneLogger(BaseOutput):
    """See: https://github.com/neptune-ai/neptune-client
    YOUR_API_TOKEN and USERNAME/PROJECT_NAME
    """
    def __init__(self, api_token: Optional[str] = None, project_qualified_name: Optional[str] = None, **kwargs):
        """Set secrets and create experiment
        Args:
            api_token: your api token, you can create NEPTUNE_API_TOKEN environment variable instead
            project_qualified_name: <user>/<project>, you can create NEPTUNE_PROJECT environment variable instead
            **kwargs: keyword args, that will be passed to create_experiment function
        """
        import neptune

        self.neptune = neptune
        self.run = self.neptune.init_run(api_token=api_token, project=project_qualified_name, **kwargs)

    def close(self):
        """Close connection"""
        if hasattr(self, "run"):
            self.run.stop()

    def send(self, logger: MainLogger):
        """Send metrics collected in last step to neptune server"""
        for name, log_items in logger.log_history.items():
            last_log_item = log_items[-1]
            self.run[name].append(value=last_log_item.value, step=last_log_item.step)
