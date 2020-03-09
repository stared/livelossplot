import re
from typing import NamedTuple, Dict, List, Pattern

# Value of metrics - for value later, we want to support numpy arrays etc
LogItem = NamedTuple('LogItem', [('step', int), ('value', float)])


class MainLogger:
    """Main logger"""

    def __init__(self, groups: Dict[str, List[str]] or None = None,
                 log_history: Dict[str, List[LogItem]] or None = None,
                 group_patterns: Dict[str, Pattern] or None = None,
                 current_step: int = -1):
        self.log_history = {} if log_history is None else log_history
        self.groups = {} if groups is None else groups
        self.group_patterns = {} if group_patterns is None else group_patterns
        self.current_step = current_step

    def update(self, logs: dict, i: int or None = None) -> None:
        """Update logs"""
        if i == None:
            self.current_step += 1
            i = self.current_step
        else:
            self.current_step = i

        for k, v in logs.items():
            if k not in self.log_history:
                self.log_history[k] = []
            self.log_history[k].append(LogItem(step=i, value=v))

    def _generate_groups_with_patterns(self) -> Dict[str, List[str]]:
        groups = {pattern: [] for pattern in self.group_patterns}
        for name, pattern in self.group_patterns.items():
            for key in self.log_history.keys():
                if re.match(pattern, key):
                    groups[name].append(key)
        return groups

    def grouped_log_history(self) -> Dict[str, Dict[str, List[LogItem]]]:
        if self.group_patterns:
            self.groups = self._generate_groups_with_patterns()
        return {group_name: {name: self.log_history[name] for name in names}
                for group_name, names in self.groups.items()}

    def reset(self) -> None:
        self.log_history = {}
        self.groups = {}
        self.current_step = -1
