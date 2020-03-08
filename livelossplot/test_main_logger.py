from livelossplot.main_logger import MainLogger


def test_main_logger_one():
    logger = MainLogger()
    logs = {'loss': 0.6}
    logger.update(logs)
    assert 'loss' in logger.log_history.keys()
    assert len(logger.log_history['loss']) == 1

def test_main_logger_more():
    logger = MainLogger()
    logger.groups = {'acccuracy': ['acc', 'val_acc'], 'log-loss': ['loss', 'val_loss']}
    logger.update({
        'acc': 0.5,
        'val_acc': 0.4,
        'loss': 1.2,
        'val_loss': 1.1
    })
    logger.update({
        'acc': 0.55,
        'val_acc': 0.45,
        'loss': 1.1,
        'val_loss': 1.0
    })
    logger.update({
        'acc': 0.65,
        'val_acc': 0.55,
        'loss': 1.0,
        'val_loss': 0.9
    })
    grouped_log_history = logger.grouped_log_history()
    assert len(grouped_log_history) == 2
    assert len(grouped_log_history['acccuracy']) == 2
    assert len(grouped_log_history['acccuracy']['val_acc']) == 3
