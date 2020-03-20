def PlotLossesKeras(**kwargs):
    """PlotLosses callback for Keras (as a standalone library).
    Requires keras to be installed.
    :param kwargs: key-arguments which are passed to PlotLosses
    """
    from .keras import PlotLossesCallback
    return PlotLossesCallback(**kwargs)


def PlotLossesKerasTF(**kwargs):
    """PlotLosses callback for Keras (as a module of TensorFlow).
    Requires tensorflow to be installed.
    :param kwargs: key-arguments which are passed to PlotLosses
    """
    from .tf_keras import PlotLossesCallback
    return PlotLossesCallback(**kwargs)


def PlotLossesPoutyne(**kwargs):
    """PlotLosses callback for Poutyne, a library for PyTorch.
    Requires poutyne to be installed, https://poutyne.org/.
    :param kwargs: key-arguments which are passed to PlotLosses
    """
    from .poutyne import PlotLossesCallback
    return PlotLossesCallback(**kwargs)


def PlotLossesIgnite(**kwargs):
    """PlotLosses callback for Poutyne, a library for PyTorch.
    Requires pytorch-ignite to be installed, https://github.com/pytorch/ignite.
    :param kwargs: key-arguments which are passed to PlotLosses
    """
    from .pytorch_ignite import PlotLossesCallback
    return PlotLossesCallback(**kwargs)
