import re
from collections import OrderedDict, defaultdict
from typing import NamedTuple, Dict, Iterable, List, Pattern, Tuple, Optional, Union

# Value of metrics - for value later, we want to support numpy arrays etc
LogItem = NamedTuple('LogItem', [('step', int), ('value', float)])
COMMON_NAME_SHORTCUTS = {
    'acc': 'Accuracy',
    'nll': 'Log Loss (cost function)',
    'mse': 'Mean Squared Error',
    'loss': 'Loss'
}


class MainLogger:
    """
    Main logger - the aim of this class is to store every log from training
    Log is a float value with corresponding training engine step
    """
    def __init__(
        self,
        groups: Optional[Dict[str, List[str]]] = None,
        metric_to_name: Optional[Dict[str, str]] = None,
        from_step: int = 0,
        current_step: int = -1,
        auto_generate_groups_if_not_available: bool = True,
        auto_generate_metric_to_name: bool = True,
        group_patterns: Iterable[Tuple[Pattern, str]] = (
            (r'^(?!val(_|-))(.*)', 'training'),
            (r'^(val(_|-))(.*)', 'validation'),
        ),
        step_names: Union[str, Dict[str, str]] = 'epoch'
    ):
        """
        Args:
            groups: dictionary with grouped metrics for example the group 'accuracy' can contains different stages
                for example 'validation_accuracy', 'training_accuracy' etc.
            metric_to_name: transformation of metric name which can be used to display name
                we can have short name in the code (acc), but full name on charts (Accuracy)
            from_step: step to show in plots (positive: show steps from this one, negative: show only this many last steps)
            current_step: current step of the train loop
            auto_generate_groups_if_not_available: flag, that enable auto-creation of metric groups
                base on group patterns
            auto_generate_metric_to_name: flag, that enable auto-creation of metric long names
                base on common shortcuts
            group_patterns: you can put there regular expressions to match a few metric names with group
                and replace its name using second value
            step_names: dictionary with a name of x axis for each metrics group or one name for all metrics
        """
        self.log_history = {}
        self.groups = groups if groups is not None else {}
        self.metric_to_name = metric_to_name if metric_to_name else {}
        self.from_step = from_step
        self.current_step = current_step
        self.auto_generate_groups = all((not groups, auto_generate_groups_if_not_available))
        self.auto_generate_metric_to_name = auto_generate_metric_to_name
        self.group_patterns = tuple((re.compile(pattern), replace_with) for pattern, replace_with in group_patterns)
        if isinstance(step_names, str):
            self.step_names = defaultdict(lambda: step_names)
        else:
            self.step_names = defaultdict(lambda: 'epoch', step_names)

    def update(self, logs: Dict[str, float], current_step: Optional[int] = None) -> None:
        """
        Args:
            logs: dictionary with metric names and values
            current_step: current step of the training loop

        Notes:
            Loop step can be controlled outside or inside main logger with autoincrement of self.current_step
        """
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
        """Add empty list for a new metric and extend metric name transformations
        Args:
            metric_name: name of metric that will be added to log_history as empty list
        """
        self.log_history[metric_name] = []
        if not self.metric_to_name.get(metric_name):
            self._auto_generate_metrics_to_name(metric_name)

    def _auto_generate_metrics_to_name(self, metric_name: str):
        """The function generate transforms for metric names base on patterns
        Args:
            metric_name: name of new appended metric

        Example:
            It can create transformation from val_acc to Validation Accuracy
        """
        suffix = self._find_suffix_with_group_patterns(metric_name)
        if suffix is None and suffix != metric_name:
            return
        similar_metric_names = [m for m in self.log_history.keys() if m.endswith(suffix)]
        if len(similar_metric_names) == 1:
            return
        for name in similar_metric_names:
            new_name = name
            for pattern_to_replace, replace_with in self.group_patterns:
                new_name = re.sub(pattern_to_replace, replace_with, new_name)
            if suffix in COMMON_NAME_SHORTCUTS.keys():
                new_name = new_name.replace(suffix, COMMON_NAME_SHORTCUTS[suffix])
            self.metric_to_name[name] = new_name

    def grouped_log_history(self, raw_names: bool = False,
                            raw_group_names: bool = False) -> Dict[str, Dict[str, List[LogItem]]]:
        """
        Args:
            raw_names: flag, return raw names instead of transformed by metric to name (as in update() input dictionary)
            raw_group_names: flag, return group names without transforming them with COMMON_NAME_SHORTCUTS

        Returns:
            logs grouped by metric groups - groups are passed in the class constructor

        Notes:
            method use group patterns instead of groups if they are available
        """
        if self.auto_generate_groups:
            self.groups = self._auto_generate_groups()
        ret = {}
        sorted_groups = OrderedDict(sorted(self.groups.items(), key=lambda t: t[0]))
        for group_name, names in sorted_groups.items():
            group_name = group_name if raw_group_names else COMMON_NAME_SHORTCUTS.get(group_name, group_name)
            ret[group_name] = {
                name if raw_names else self.metric_to_name.get(name, name): self.history_shorter(name)
                for name in names
            }
        return ret

    def history_shorter(self, name: str, full: bool = False) -> List[LogItem]:
        """
        Args:
            name: metrics name, e.g. 'val_acc' or 'loss'
            full: flag, if True return all, otherwise as specified by the from_step parameter

        Returns:
            a list of log items
        """
        log_metrics = self.log_history[name]
        if full or self.from_step == 0:
            return log_metrics
        elif self.from_step > 0:
            return [x for x in log_metrics if x.step >= self.from_step]
        else:
            current_from_step = self.current_step + self.from_step
            return [x for x in log_metrics if x.step >= current_from_step]

    def _auto_generate_groups(self) -> Dict[str, List[str]]:
        """
        Returns:
            groups generated with group patterns

        Notes:
            Auto create groups base on val_ prefix - this step is skipped if groups are set
                or if group patterns are available
        """
        groups = {}
        for key in self.log_history.keys():
            abs_key = self._find_suffix_with_group_patterns(key)
            if not groups.get(abs_key):
                groups[abs_key] = []
            groups[abs_key].append(key)
        return groups

    def _find_suffix_with_group_patterns(self, metric_name: str) -> str:
        suffix = metric_name
        for pattern, _ in self.group_patterns:
            match = re.match(pattern, metric_name)
            if match:
                suffix = match.groups()[-1]
        return suffix

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
