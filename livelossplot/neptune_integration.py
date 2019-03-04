import neptune

ctx = neptune.Context()


def neptune_send_plot(logs):
    epoch_data = logs[-1]
    for metrics, value in epoch_data.items():
        ctx.channel_send(name=metrics, y=value)
