from __future__ import division
import warnings

import matplotlib
import matplotlib.pyplot as plt
from IPython.display import clear_output


def not_inline_warning():
    backend = matplotlib.get_backend()
    if "backend_inline" not in backend:
        warnings.warn("livelossplot requires inline plots.\nYour current backend is: {}\nRun in a Jupyter environment and execute '%matplotlib inline'.".format(backend))

# TODO
# * object-oriented API
# * only integer ticks




def draw_plot(logs, metrics, figsize=None, max_epoch=None,
              max_cols=2,
              validation_fmt="val_{}",
              metric2title={},
              extrema=None,
              fig_path=None,
              samples_per_update=None,
              training_size=None,
              batch_size=None):

    extrema_logs = []

    epoch_logs = logs["epoch"]
    batch_logs = logs["batch"]

    if samples_per_update:
        training_log_step = samples_per_update // batch_size
        if len(logs["batch"])%training_log_step != 0:
            return
        else:
            training_logs = batch_logs[training_log_step-1::training_log_step]
            val_logs = epoch_logs
            training_data_x_axis = [x*samples_per_update for x in range(1,len(training_logs)+1)]
            val_data_x_axis = [x*training_size for x in range(1,len(val_logs)+1)]
            xlabel='number of datasets seen'
    else:
        if len(epoch_logs)==0:
            return
        training_logs = epoch_logs
        val_logs = epoch_logs
        training_data_x_axis = range(1, len(training_logs)+1)
        val_data_x_axis = training_data_x_axis
        xlabel='epoch'


    clear_output(wait=True)
    plt.figure(figsize=figsize)
    plot_rows = (len(metrics) + 1) // max_cols +1


    for metric_id, metric in enumerate(metrics):
        axe = plt.subplot2grid((plot_rows, max_cols),(metric_id//max_cols, metric_id%max_cols))
        if max_epoch is not None:

            if samples_per_update is None:
                axe.set_xlim(1,max_epoch)
            else:
                axe.set_xlim(1,training_size*max_epoch)


        metric_logs = [log[metric] for log in training_logs]


        axe.plot(training_data_x_axis,
                 metric_logs,
                 label="training")

        values_fmt = 'min: {min:8.3f}, max: {max:8.3f}, cur: {cur:8.3f}'
        training_log_fmt = '{metric}:\ntraining   ({values_fmt})'.format(
            metric=metric2title.get(metric, metric),
            values_fmt=values_fmt
        )


        if extrema:
            extrema_logs.append(
                training_log_fmt.format(
                    min=extrema[metric].get('min', float('inf')),
                    max=extrema[metric].get('max', -float('inf')),
                    cur=metric_logs[-1]
                )
            )
        validation_log_fmt = '\nvalidation ({})'.format(values_fmt)
        if len(val_logs):
            val_metric_name = validation_fmt.format(metric)
            val_metric_logs = [log[val_metric_name] for log in val_logs]
            axe.plot(val_data_x_axis,
                     val_metric_logs,
                     label="validation")
            if extrema:
                extrema_logs[-1] += validation_log_fmt.format(
                    min=extrema[val_metric_name].get('min', float('inf')),
                    max=extrema[val_metric_name].get('max', -float('inf')),
                    cur=val_metric_logs[-1]
                )


        axe.set(
            title=metric2title.get(metric, metric),
            xlabel=xlabel,
            )

        axe.legend(loc='center right')
    plt.tight_layout()
    plt.show()
    print('\n\n'.join(extrema_logs))





def draw_plot1(logs, metrics, figsize=None, max_epoch=None,
              max_cols=2,
              validation_fmt="val_{}",
              metric2title={},
              extrema=None,
              fig_path=None):
    clear_output(wait=True)
    plt.figure(figsize=figsize)
    logs = logs["epoch"]

    extrema_logs = []
    for metric_id, metric in enumerate(metrics):
        plt.subplot((len(metrics) + 1) // max_cols + 1, max_cols, metric_id + 1)
        #row col ind
        if max_epoch is not None:
            plt.xlim(1, max_epoch)
        print(logs)
        metric_logs = [log[metric] for log in logs]
        print(metric_logs)
        plt.plot(range(1, len(logs) + 1),
                 metric_logs,
                 label="training")


        # metric_logs = [log[metric] for log in epoch_logs]
        # print(metric_logs)
        # axe.plot(range(1, len(logs)+1),
        #          metric_logs,
        #          label="training")

        values_fmt = 'min: {min:8.3f}, max: {max:8.3f}, cur: {cur:8.3f}'
        training_log_fmt = '{metric}:\ntraining   ({values_fmt})'.format(
            metric=metric2title.get(metric, metric),
            values_fmt=values_fmt
        )
        validation_log_fmt = '\nvalidation ({})'.format(values_fmt)

        if extrema:
            extrema_logs.append(
                training_log_fmt.format(
                    min=extrema[metric].get('min', float('inf')),
                    max=extrema[metric].get('max', -float('inf')),
                    cur=metric_logs[-1]
                )
            )

        if validation_fmt.format(metric) in logs[0]:
            val_metric_name = validation_fmt.format(metric)
            val_metric_logs = [log[val_metric_name] for log in logs]
            plt.plot(range(1, len(logs) + 1),
                     val_metric_logs,
                     label="validation")
            if extrema:
                extrema_logs[-1] += validation_log_fmt.format(
                    min=extrema[val_metric_name].get('min', float('inf')),
                    max=extrema[val_metric_name].get('max', -float('inf')),
                    cur=val_metric_logs[-1]
                )

        plt.title(metric2title.get(metric, metric))
        plt.xlabel('epoch')
        plt.legend(loc='center right')

    plt.tight_layout()
    if fig_path is not None:
        plt.savefig(fig_path)
    plt.show()
    print('\n\n'.join(extrema_logs))
