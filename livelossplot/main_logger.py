import re
from collections import defaultdict
from collections.abc import Iterable
from re import Pattern
from typing import NamedTuple


class LogItem(NamedTuple):
    step: int
    value: float


COMMON_NAME_SHORTCUTS = {
    'acc': 'Accuracy',
    'nll': 'Log Loss (cost function)',
    'mse': 'Mean Squared Error',
    'loss': 'Loss',
}


class MainLogger:
    """Stores per-step training metrics and groups them for plotting."""

    def __init__(
        self,
        groups: dict[str, list[str]] | None = None,
        metric_to_name: dict[str, str] | None = None,
        from_step: int = 0,
        current_step: int = -1,
        auto_generate_groups_if_not_available: bool = True,
        auto_generate_metric_to_name: bool = True,
        group_patterns: Iterable[tuple[str | Pattern, str]] = (
            (r'^(?!val(_|-))(.*)', 'training'),
            (r'^(val(_|-))(.*)', 'validation'),
        ),
        step_names: str | dict[str, str] = 'epoch',
    ):
        """
        Args:
            groups: pre-defined metric groups, e.g. {'accuracy': ['acc', 'val_acc']}.
            metric_to_name: short-name to display-name overrides, e.g. {'acc': 'Accuracy'}.
            from_step: positive = show steps from this one; negative = show only this many last steps.
            current_step: current step of the train loop.
            auto_generate_groups_if_not_available: derive groups from `group_patterns` if `groups` is empty.
            auto_generate_metric_to_name: derive display names from `group_patterns` and `COMMON_NAME_SHORTCUTS`.
            group_patterns: regex patterns mapping metric names to group labels (training/validation).
            step_names: x-axis label, either a single string or per-group mapping.
        """
        self.log_history: dict[str, list[LogItem]] = {}
        self.groups: dict[str, list[str]] = groups if groups is not None else {}
        self.metric_to_name: dict[str, str] = metric_to_name or {}
        self.from_step = from_step
        self.current_step = current_step
        self.auto_generate_groups = not groups and auto_generate_groups_if_not_available
        self.auto_generate_metric_to_name = auto_generate_metric_to_name
        self.group_patterns = tuple((re.compile(pattern), replace_with) for pattern, replace_with in group_patterns)
        if isinstance(step_names, str):
            self.step_names: dict[str, str] = defaultdict(lambda: step_names)
        else:
            self.step_names = defaultdict(lambda: 'epoch', step_names)

    def update(self, logs: dict[str, float], current_step: int | None = None) -> None:
        """Append a new step of metric values."""
        if current_step is None:
            self.current_step += 1
            current_step = self.current_step
        else:
            self.current_step = current_step
        for k, v in logs.items():
            if k not in self.log_history:
                self._add_new_metric(k)
            self.log_history[k].append(LogItem(step=current_step, value=v))

    def reset(self) -> None:
        """Clear all logs, groups, and reset the step counter."""
        self.log_history = {}
        self.groups = {}
        self.current_step = -1

    def grouped_log_history(
        self,
        raw_names: bool = False,
        raw_group_names: bool = False,
    ) -> dict[str, dict[str, list[LogItem]]]:
        """Return logs grouped by metric group, sorted alphabetically.

        Args:
            raw_names: keep original metric names instead of `metric_to_name` mapping.
            raw_group_names: keep original group names instead of `COMMON_NAME_SHORTCUTS` mapping.
        """
        if self.auto_generate_groups:
            self.groups = self._auto_generate_groups()
        result: dict[str, dict[str, list[LogItem]]] = {}
        for group_name, names in sorted(self.groups.items()):
            display_group = group_name if raw_group_names else COMMON_NAME_SHORTCUTS.get(group_name, group_name)
            result[display_group] = {
                name if raw_names else self.metric_to_name.get(name, name): self.history_shorter(name)
                for name in names
            }
        return result

    def history_shorter(self, name: str, full: bool = False) -> list[LogItem]:
        """Return the log history for one metric, trimmed by `from_step` unless `full=True`."""
        if name not in self.log_history:
            return []
        log_metrics = self.log_history[name]
        if full or self.from_step == 0:
            return log_metrics
        if self.from_step > 0:
            return [x for x in log_metrics if x.step >= self.from_step]
        threshold = self.current_step + self.from_step
        return [x for x in log_metrics if x.step >= threshold]

    def _add_new_metric(self, metric_name: str) -> None:
        self.log_history[metric_name] = []
        if not self.metric_to_name.get(metric_name):
            self._auto_generate_metrics_to_name(metric_name)

    def _auto_generate_metrics_to_name(self, metric_name: str) -> None:
        suffix = self._find_suffix_with_group_patterns(metric_name)
        similar_metric_names = [m for m in self.log_history if m.endswith(suffix)]
        if len(similar_metric_names) == 1:
            return
        for name in similar_metric_names:
            new_name = name
            for pattern, replace_with in self.group_patterns:
                new_name = re.sub(pattern, replace_with, new_name)
            if suffix in COMMON_NAME_SHORTCUTS:
                new_name = new_name.replace(suffix, COMMON_NAME_SHORTCUTS[suffix])
            self.metric_to_name[name] = new_name

    def _auto_generate_groups(self) -> dict[str, list[str]]:
        groups: dict[str, list[str]] = {}
        for key in self.log_history:
            abs_key = self._find_suffix_with_group_patterns(key)
            groups.setdefault(abs_key, []).append(key)
        return groups

    def _find_suffix_with_group_patterns(self, metric_name: str) -> str:
        suffix = metric_name
        for pattern, _ in self.group_patterns:
            match = re.match(pattern, metric_name)
            if match:
                suffix = match.groups()[-1]
        return suffix
