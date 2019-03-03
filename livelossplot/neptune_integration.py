import neptune

ctx = neptune.Context()


def neptune_send_plot(logs):
    epoch_data = logs[-1]
    for key in epoch_data:
        ctx.channel_send(name=key, y=epoch_data[key])
