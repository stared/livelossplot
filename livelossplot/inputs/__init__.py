def PlotLossesKeras(**kwargs):
    """PlotLosses callback for Keras (as a standalone library, not a TensorFlow module).
    Args:
        **kwargs: key-arguments which are passed to PlotLosses

    Notes:
        Requires keras to be installed.
    """
    from .keras import PlotLossesCallback
    return PlotLossesCallback(**kwargs)


def PlotLossesKerasTF(**kwargs):
    """PlotLosses callback for Keras (as a module of TensorFlow).
    Args:
        **kwargs: key-arguments which are passed to PlotLosses

    Notes:
        Requires tensorflow to be installed.
    """
    from .tf_keras import PlotLossesCallback
    return PlotLossesCallback(**kwargs)


def PlotLossesPoutyne(**kwargs):
    """PlotLosses callback for Poutyne, a library for PyTorch.
    Args:
        **kwargs: key-arguments which are passed to PlotLosses

    Notes:
        Requires poutyne to be installed, <https://poutyne.org/>.
    """
    from .poutyne import PlotLossesCallback
    return PlotLossesCallback(**kwargs)


def PlotLossesIgnite(**kwargs):
    """PlotLosses callback for PyTorch-Ignite, a library for PyTorch.
    Args:
        **kwargs: key-arguments which are passed to PlotLosses

    Notes:
        Requires pytorch-ignite to be installed, <https://github.com/pytorch/ignite>.
    """
    from .pytorch_ignite import PlotLossesCallback
    return PlotLossesCallback(**kwargs)
