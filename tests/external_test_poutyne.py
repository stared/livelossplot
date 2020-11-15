import torch
from torch import nn, optim
from torch.utils.data import TensorDataset, DataLoader
from poutyne import Model

from livelossplot import MainLogger, PlotLossesPoutyne
from livelossplot.outputs import BaseOutput


class CheckOutput(BaseOutput):
    def send(self, logger: MainLogger):
        assert isinstance(logger, MainLogger)
        log_history = logger.log_history
        assert log_history.get('loss') is not None


class Network(nn.Sequential):
    def __init__(self):
        super().__init__(nn.Linear(12, 5))


def get_random_data():
    dataset_size, num_inputs, num_outputs = 100, 12, 5
    inputs = torch.rand(dataset_size, num_inputs)
    labels = torch.randint(num_outputs, (dataset_size, ))
    dataset = TensorDataset(inputs, labels)
    dataloader = DataLoader(dataset, batch_size=10)
    return dataloader


def test_poutyne():
    callback = PlotLossesPoutyne(outputs=(CheckOutput(), ))
    network = Network()
    optimizer = optim.Adam(params=network.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss()

    train_dataloader = get_random_data()

    model = Model(network, optimizer, loss_fn)
    model.fit_generator(train_dataloader, epochs=2, callbacks=[callback])
