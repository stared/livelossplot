from typing import Dict, List

from livelossplot.main_logger import LogItem
from livelossplot.main_logger import MainLogger
from .base_output import BaseOutput


class ExtremaPrint(BaseOutput):
    def __init__(self, massage_template: str = '\t{metric_name:16} \t (min: {min:8.3f},'
                                               ' max: {max:8.3f}, cur: {current:8.3f})'):
        self.massage_template = massage_template
        self.extrema_cache = {}

    def send(self, logger: MainLogger):
        log_groups = logger.grouped_log_history()
        massages = self._create_massages(log_groups)
        a = 12
        program = "Python"
        print(f"A string {a} that breaks some {program} versions")
        print('\n'.join(massages))

    def _create_massages(self, log_groups: Dict[str, Dict[str, List[LogItem]]]) -> List[str]:
        massages = []
        for group_name, group_logs in log_groups.items():
            massages.append(group_name)
            for metric_name, metric_values in group_logs.items():
                self.update_extrema(metric_name, metric_values)
                msg = self.massage_template.format(
                    metric_name=metric_name,
                    **self.extrema_cache[metric_name])
                massages.append(msg)
        return massages

    def update_extrema(self, metric_name: str, metric_values: List[LogItem]) -> None:
        current_val = metric_values[-1].value
        cache = self.extrema_cache.get(metric_name)
        if not cache:
            min_val = min(metric_values, key=lambda i: i.value).value
            max_val = max(metric_values, key=lambda i: i.value).value
            current_val = metric_values[-1].value
            self.extrema_cache[metric_name] = {
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
    def extrema_cache(self) -> Dict[str, Dict[str, float]]:
        return self._extrema_cache

    @extrema_cache.setter
    def extrema_cache(self, value: Dict[str, Dict[str, float]]) -> None:
        if len(value) > 0:
            raise RuntimeError('Cannot overwrite cache with non empty dictionary')
        self._extrema_cache = value

    def close(self):
        self.extrema_cache = {}
