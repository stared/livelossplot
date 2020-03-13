import re
from typing import NamedTuple, Dict, List, Pattern

# Value of metrics - for value later, we want to support numpy arrays etc
LogItem = NamedTuple('LogItem', [('step', int), ('value', float)])


class MainLogger:
    """
    Main logger - the aim of this class is to store every log from training
    Log is a float value with corresponding training engine step
    """

    def __init__(self, groups: Dict[str, List[str]] or None = None,
                 group_patterns: Dict[str, Pattern] or None = None,
                 current_step: int = -1):
        self.log_history = {}
        self.groups = groups
        self.group_patterns = group_patterns
        self.current_step = current_step

    def update(self, logs: dict, current_step: int or None = None) -> None:
        """Update logs - loop step can be controlled outside or inside main logger"""
        if current_step is None:
            self.current_step += 1
            current_step = self.current_step
        else:
            self.current_step = current_step

        for k, v in logs.items():
            if k not in self.log_history:
                self.log_history[k] = []
            self.log_history[k].append(LogItem(step=current_step, value=v))

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

    def grouped_log_history(self) -> Dict[str, Dict[str, List[LogItem]]]:
        """
        :return: logs grouped by metric groups - groups are passed in the class constructor
        method use group patterns instead of groups if they are available
        """
        if self.group_patterns:
            self.groups = self._generate_groups_with_patterns()
        return {group_name: {name: self.log_history[name] for name in names}
                for group_name, names in self.groups.items()}

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
