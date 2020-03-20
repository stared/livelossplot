import torch
from ignite import engine
from torch import nn, optim
from torch.utils.data import TensorDataset, DataLoader

from livelossplot import MainLogger, PlotLossesIgnite


class CheckOutput:
    def send(self, logger: MainLogger):
        assert isinstance(logger, MainLogger)
        log_history = logger.log_history
        assert log_history.get('loss') is not None


class Model(nn.Sequential):
    def __init__(self):
        super().__init__(nn.Linear(12, 5))


def get_random_data():
    dataset_size, num_inputs, num_outputs = 100, 12, 5
    inputs = torch.rand(dataset_size, num_inputs)
    labels = torch.randint(num_outputs, (dataset_size, ))
    dataset = TensorDataset(inputs, labels)
    dataloader = DataLoader(dataset, batch_size=10)
    return dataloader


def test_ignite():
    callback = PlotLossesIgnite(outputs=(CheckOutput(), ))
    model = Model()
    optimizer = optim.Adam(params=model.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss()
    trainer = engine.create_supervised_trainer(
        model, optimizer, loss_fn, output_transform=lambda x, y, y_pred, loss: {'loss': loss.item()}
    )

    losses = []

    @trainer.on(engine.Events.ITERATION_COMPLETED)
    def _save_losses(engine):
        losses.append(engine.state.output['loss'])

    @trainer.on(engine.Events.EPOCH_COMPLETED)
    def _compute_epoch_loss(engine):
        engine.state.metrics = {'loss': sum(losses) / len(losses)}

    callback.attach(trainer)

    train_dataloader = get_random_data()
    trainer.run(train_dataloader, max_epochs=2)
