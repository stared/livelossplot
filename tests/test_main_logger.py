import re

from livelossplot import MainLogger


def test_main_logger():
    """Test basic usage"""
    logger = MainLogger()
    logs = {'loss': 0.6}
    logger.update(logs)
    assert 'loss' in logger.log_history.keys()
    assert len(logger.log_history['loss']) == 1


def test_main_logger_with_groups():
    """Test groups"""
    groups = {'acccuracy': ['acc', 'val_acc'], 'log-loss': ['loss', 'val_loss']}
    logger = MainLogger(groups=groups)
    logger.update({'acc': 0.5, 'val_acc': 0.4, 'loss': 1.2, 'val_loss': 1.1})
    logger.update({'acc': 0.55, 'val_acc': 0.45, 'loss': 1.1, 'val_loss': 1.0})
    logger.update({'acc': 0.65, 'val_acc': 0.55, 'loss': 1.0, 'val_loss': 0.9})
    grouped_log_history = logger.grouped_log_history(raw_names=True, raw_group_names=True)
    assert len(grouped_log_history) == 2
    assert len(grouped_log_history['acccuracy']) == 2
    assert len(grouped_log_history['acccuracy']['val_acc']) == 3
    assert len(grouped_log_history['log-loss']['loss']) == 3
    grouped_log_history = logger.grouped_log_history()
    assert len(grouped_log_history) == 2
    assert len(grouped_log_history['acccuracy']) == 2
    assert len(grouped_log_history['acccuracy']['validation']) == 3
    assert len(grouped_log_history['log-loss']['training']) == 3


def test_main_logger_with_default_groups():
    """Test group patterns"""
    logger = MainLogger()
    logger.update({'acc': 0.5, 'val_acc': 0.4, 'loss': 1.2, 'val_loss': 1.1})
    logger.update({'acc': 0.55, 'val_acc': 0.45, 'loss': 1.1, 'val_loss': 1.0})
    logger.update({'acc': 0.65, 'val_acc': 0.55, 'loss': 1.0, 'val_loss': 0.9})
    grouped_log_history = logger.grouped_log_history(raw_names=True, raw_group_names=True)
    assert len(grouped_log_history) == 2
    assert len(grouped_log_history['acc']) == 2
    assert len(grouped_log_history['acc']['val_acc']) == 3
    grouped_log_history = logger.grouped_log_history()
    assert len(grouped_log_history) == 2
    assert len(grouped_log_history['Accuracy']) == 2
    assert len(grouped_log_history['Accuracy']['validation']) == 3


def test_main_logger_metric_to_name():
    """Test group patterns"""
    logger = MainLogger()
    logger.update({'acc': 0.5, 'val_acc': 0.4, 'loss': 1.2, 'val_loss': 1.1, 'lr': 0.01})
    logger.update({'acc': 0.55, 'val_acc': 0.45, 'loss': 1.1, 'val_loss': 1.0, 'lr': 0.001})
    logger.update({'acc': 0.65, 'val_acc': 0.55, 'loss': 1.0, 'val_loss': 0.9, 'lr': 0.0001})
    metric_to_name = logger.metric_to_name
    assert 'lr' not in metric_to_name
    target_metric_to_name = {
        'acc': 'training',
        'val_acc': 'validation',
        'loss': 'training',
        'val_loss': 'validation',
    }
    for metric, metric_name in metric_to_name.items():
        assert metric_name == target_metric_to_name.get(metric)


def test_main_logger_autogroups():
    """Test group patterns"""
    logger = MainLogger()
    logger.update({'acc': 0.5, 'val_acc': 0.4, 'loss': 1.2, 'val_loss': 1.1, 'lr': 0.01})
    logger.update({'acc': 0.55, 'val_acc': 0.45, 'loss': 1.1, 'val_loss': 1.0, 'lr': 0.001})
    logger.update({'acc': 0.65, 'val_acc': 0.55, 'loss': 1.0, 'val_loss': 0.9, 'lr': 0.0001})
    grouped_log_history = logger.grouped_log_history()
    target_groups = {'Accuracy': ('validation', 'training'), 'Loss': ('validation', 'training'), 'lr': ('lr', )}
    for target_group, target_metrics in target_groups.items():
        for m1, m2 in zip(sorted(grouped_log_history[target_group].keys()), sorted(target_metrics)):
            assert m1 == m2


def test_main_logger_step_names():
    step_names = 'iteration'
    logger = MainLogger(step_names=step_names)
    assert logger.step_names['Accuracy'] == 'iteration'
    step_names = {'Accuracy': 'evaluation', 'Loss': 'batch'}
    logger = MainLogger(step_names=step_names)
    assert logger.step_names['Accuracy'] == 'evaluation'
    assert logger.step_names['Loss'] == 'batch'
    assert logger.step_names['Epoch Time'] == 'epoch'
