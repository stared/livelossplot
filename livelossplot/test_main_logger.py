from livelossplot.main_logger import MainLogger


def test_main_logger():
    logger = MainLogger()
    logs = {'loss': 0.6}
    logger.update(logs)
    assert 'loss' in logger.log_history.keys()
    assert len(logger.log_history['loss']) == 1
