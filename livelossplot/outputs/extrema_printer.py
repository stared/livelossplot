from typing import Dict, List

from livelossplot.main_logger import LogItem
from livelossplot.main_logger import MainLogger
from .base_output import BaseOutput


class ExtremaPrinter(BaseOutput):
    def __init__(
        self,
        massage_template: str = '\t{metric_name:16} \t (min: {min:8.3f},'
        ' max: {max:8.3f}, cur: {current:8.3f})'
    ):
        """
        Args:
            massage_template: you can specify massage which use all or a few values (min, max, current)
        """
        self.massage_template = massage_template
        self.last_message = ""

    def send(self, logger: MainLogger):
        """Create massages with log_history and massage template"""
        log_groups = logger.grouped_log_history()
        self.last_message = '\n'.join(self._create_massages(log_groups))
        print(self.last_message)

    def _create_massages(self, log_groups: Dict[str, Dict[str, List[LogItem]]]) -> List[str]:
        """Create massages"""
        massages = []
        for group_name, group_logs in log_groups.items():
            massages.append(group_name)
            for metric_name, log_items in group_logs.items():
                if len(log_items) == 0:
                    msg = '\t{metric_name:16} \t (no values!)'.format(metric_name=metric_name)
                else:
                    values = [log_item.value for log_item in log_items]
                    min_val = min(values)
                    max_val = max(values)
                    current_val = values[-1]
                    msg = self.massage_template.format(
                        metric_name=metric_name, min=min_val, max=max_val, current=current_val
                    )
                massages.append(msg)
        return massages
