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
    assert len(grouped_log_history['acccuracy']['validation ']) == 3
    assert len(grouped_log_history['log-loss']['training ']) == 3


def test_main_logger_with_group_patterns():
    """Test group patterns"""
    group_patterns = {'acccuracy': re.compile(r'.*acc$'), 'log-loss': re.compile(r'.*loss$')}
    logger = MainLogger(group_patterns=group_patterns)
    logger.update({'acc': 0.5, 'val_acc': 0.4, 'loss': 1.2, 'val_loss': 1.1})
    logger.update({'acc': 0.55, 'val_acc': 0.45, 'loss': 1.1, 'val_loss': 1.0})
    logger.update({'acc': 0.65, 'val_acc': 0.55, 'loss': 1.0, 'val_loss': 0.9})
    grouped_log_history = logger.grouped_log_history(raw_names=True, raw_group_names=True)
    assert len(grouped_log_history) == 2
    assert len(grouped_log_history['acccuracy']) == 2
    assert len(grouped_log_history['acccuracy']['val_acc']) == 3
    grouped_log_history = logger.grouped_log_history()
    assert len(grouped_log_history) == 2
    assert len(grouped_log_history['acccuracy']) == 2
    assert len(grouped_log_history['acccuracy']['validation ']) == 3