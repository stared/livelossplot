import re
from typing import NamedTuple, Dict, List, Pattern, Tuple

# Value of metrics - for value later, we want to support numpy arrays etc
LogItem = NamedTuple('LogItem', [('step', int), ('value', float)])
COMMON_NAME_SHORTCUTS = {'acc': 'Accuracy', 'nll': 'Log Loss', 'mse': 'Mean Squared Error', 'loss': 'Loss'}


class MainLogger:
    """
    Main logger - the aim of this class is to store every log from training
    Log is a float value with corresponding training engine step
    """
    def __init__(
        self,
        groups: Dict[str, List[str]] or None = None,
        group_patterns: Dict[str, Pattern] or None = None,
        metric_to_name: Dict[str, str] or None = None,
        current_step: int = -1,
        auto_generate_groups_if_not_available: bool = True,
        auto_generate_metric_to_name: bool = True
    ):
        self.log_history = {}
        self.groups = groups
        self.group_patterns = group_patterns
        self.metric_to_name = metric_to_name if metric_to_name else {}
        self.current_step = current_step
        self.auto_generate_groups = all((not groups, not group_patterns, auto_generate_groups_if_not_available))
        self.auto_generate_metric_to_name = auto_generate_metric_to_name

    def update(self, logs: dict, current_step: int or None = None) -> None:
        """Update logs - loop step can be controlled outside or inside main logger"""
        if current_step is None:
            self.current_step += 1
            current_step = self.current_step
        else:
            self.current_step = current_step
        for k, v in logs.items():
            if k not in self.log_history:
                self._add_new_metric(k)
            self.log_history[k].append(LogItem(step=current_step, value=v))

    def _add_new_metric(self, metric_name: str):
        self.log_history[metric_name] = []
        if not self.metric_to_name.get(metric_name):
            self._auto_generate_metrics_to_name(metric_name)

    def _auto_generate_metrics_to_name(
        self,
        metric_name: str,
        patterns: Tuple[Tuple[str, str]] = (
            (r'^(?!val_)', 'Training '),
            (r'^val_', 'Validation '),
        )
    ):
        suffix = '_'.join(metric_name.split('_')[1:]) if '_' in metric_name else metric_name
        similar_metric_names = [m for m in self.log_history.keys() if m.endswith(suffix)]
        for name in similar_metric_names:
            new_name = name
            for pattern_to_replace, replace_with in patterns:
                new_name = re.sub(pattern_to_replace, replace_with, new_name)
            if suffix in COMMON_NAME_SHORTCUTS.keys():
                new_name = new_name.replace(suffix, COMMON_NAME_SHORTCUTS[suffix])
            self.metric_to_name[name] = new_name

    def grouped_log_history(self, raw_names: bool = False) -> Dict[str, Dict[str, List[LogItem]]]:
        """
        :return: logs grouped by metric groups - groups are passed in the class constructor
        method use group patterns instead of groups if they are available
        """
        if self.group_patterns:
            self.groups = self._generate_groups_with_patterns()
        elif self.auto_generate_groups:
            self.groups = self._auto_generate_groups()
        ret = {}
        for group_name, names in self.groups.items():
            group_name = group_name if raw_names else COMMON_NAME_SHORTCUTS.get(group_name, group_name)
            ret[group_name] = {
                name if raw_names else self.metric_to_name.get(name, name): self.log_history[name]
                for name in names
            }
        return ret

    def _generate_groups_with_patterns(self) -> Dict[str, List[str]]:
        """
        :return: grouped metric names
        """
        groups = {pattern: [] for pattern in self._group_patterns}
        for name, pattern in self._group_patterns.items():
            for key in self.log_history.keys():
                if re.match(pattern, key):
                    groups[name].append(key)
        return groups

    def _auto_generate_groups(self) -> Dict[str, List[str]]:
        groups = {}
        for key in self.log_history.keys():
            abs_key = key.replace('val_', '')
            if not groups.get(abs_key):
                groups[abs_key] = []
            groups[abs_key].append(key)
        return groups

    def reset(self) -> None:
        """Method clears logs, groups and reset step counter"""
        self.log_history = {}
        self.groups = {}
        self.current_step = -1

    @property
    def groups(self) -> Dict[str, List[str]]:
        """groups getter"""
        return self._groups

    @groups.setter
    def groups(self, value: Dict[str, List[str]]) -> None:
        """groups setter - groups should be dictionary"""
        if value is None:
            self._groups = {}
        self._groups = value

    @property
    def log_history(self) -> Dict[str, List[LogItem]]:
        """logs getter"""
        return self._log_history

    @log_history.setter
    def log_history(self, value: Dict[str, List[LogItem]]) -> None:
        """logs setter - logs can not be overwritten - you can only reset it to empty state"""
        if len(value) > 0:
            raise RuntimeError('Cannot overwrite log history with non empty dictionary')
        self._log_history = value

    @property
    def group_patterns(self) -> Dict[str, Pattern]:
        """group patterns getter"""
        return self._group_patterns

    @group_patterns.setter
    def group_patterns(self, value: Dict[str, Pattern]) -> None:
        """group patterns setter - patterns should be dictionary"""
        if value is None:
            self._group_patterns = {}
        self._group_patterns = value
