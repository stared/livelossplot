from livelossplot.main_logger import LogItem, MainLogger

from .base_output import BaseOutput


class ExtremaPrinter(BaseOutput):
    def __init__(
        self,
        message_template: str = '\t{metric_name:16} \t (min: {min:8.3f},'
        ' max: {max:8.3f}, cur: {current:8.3f})'
    ):
        """
        Args:
            message_template: format string with min, max, current placeholders
        """
        self.message_template = message_template
        self.last_message = ""

    def send(self, logger: MainLogger):
        """Print min/max/current per metric to stdout"""
        log_groups = logger.grouped_log_history()
        self.last_message = '\n'.join(self._create_messages(log_groups))
        print(self.last_message)

    def _create_messages(self, log_groups: dict[str, dict[str, list[LogItem]]]) -> list[str]:
        messages = []
        for group_name, group_logs in log_groups.items():
            messages.append(group_name)
            for metric_name, log_items in group_logs.items():
                if len(log_items) == 0:
                    msg = f'\t{metric_name:16} \t (no values!)'
                else:
                    values = [log_item.value for log_item in log_items]
                    msg = self.message_template.format(
                        metric_name=metric_name,
                        min=min(values),
                        max=max(values),
                        current=values[-1],
                    )
                messages.append(msg)
        return messages
