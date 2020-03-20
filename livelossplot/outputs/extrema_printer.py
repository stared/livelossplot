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
        :param massage_template: you can specify massage which use all or a few values (min, max, current)
        """
        self.massage_template = massage_template
        self.extrema_cache = {}

    def send(self, logger: MainLogger):
        """Create massages with log_history and massage template"""
        log_groups = logger.grouped_log_history()
        massages = self._create_massages(log_groups)
        print('\n'.join(massages))

    def _create_massages(self, log_groups: Dict[str, Dict[str, List[LogItem]]]) -> List[str]:
        """Update cache and create massages"""
        massages = []
        for group_name, group_logs in log_groups.items():
            massages.append(group_name)
            for metric_name, metric_values in group_logs.items():
                self.update_extrema(metric_name, group_name, metric_values)
                msg = self.massage_template.format(
                    metric_name=metric_name, **self.extrema_cache[group_name][metric_name]
                )
                massages.append(msg)
        return massages

    def update_extrema(self, metric_name: str, group_name: str, metric_values: List[LogItem]) -> None:
        """Write highest, lower and current value to cache (or initialize if no exist)"""
        current_val = metric_values[-1].value
        if not self.extrema_cache.get(group_name):
            self.extrema_cache[group_name] = {}
        cache = self.extrema_cache[group_name].get(metric_name)
        if not cache:
            min_val = min(metric_values, key=lambda i: i.value).value
            max_val = max(metric_values, key=lambda i: i.value).value
            current_val = metric_values[-1].value
            self.extrema_cache[group_name][metric_name] = {
                'min': min_val,
                'max': max_val,
                'current': current_val,
            }
        else:
            min_val = min(cache['min'], current_val)
            max_val = max(cache['max'], current_val)
            cache['min'] = min_val
            cache['max'] = max_val
            cache['current'] = current_val

    @property
    def extrema_cache(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        """Cache getter"""
        return self._extrema_cache

    @extrema_cache.setter
    def extrema_cache(self, value: Dict[str, Dict[str, Dict[str, float]]]) -> None:
        """Cache setter - can initialize cache only with empty dictionary"""
        if len(value) > 0:
            raise RuntimeError('Cannot overwrite cache with non empty dictionary')
        self._extrema_cache = value

    def close(self):
        """Clear cache"""
        self.extrema_cache = {}
