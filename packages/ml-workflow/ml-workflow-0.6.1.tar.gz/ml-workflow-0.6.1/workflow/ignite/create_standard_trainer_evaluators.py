import ignite
from ignite.engine import Events
from ignite.contrib.handlers.tensorboard_logger import (
    TensorboardLogger, OutputHandler, OptimizerParamsHandler, global_step_from_engine
)

from workflow.ignite.handlers.epoch_logger import EpochLogger
from workflow.ignite.handlers.metrics_logger import MetricsLogger
from workflow.ignite.handlers.progress_bar import ProgressBar


def create_standard_trainer_evaluators(
    train_batch,
    evaluate_batch,
    evaluate_data_loaders,
    trainer_metrics,
    evaluator_metrics,
    optimizers,
    config,
):

    trainer = ignite.engine.Engine(train_batch)

    for name, metric in trainer_metrics.items():
        metric.attach(trainer, name)

    evaluators = {
        evaluator_name: ignite.engine.Engine(evaluate_batch)
        for evaluator_name in evaluate_data_loaders.keys()
    }

    for evaluator_name, evaluator in evaluators.items():
        for metric_name, metric in evaluator_metrics[evaluator_name].items():
            metric.attach(evaluator, metric_name)

    tensorboard_logger = TensorboardLogger(log_dir='tb')

    EpochLogger().attach(trainer)

    # Order of attaching progress bars is important for vscode / atom
    training_desc = 'train'
    train_metric_names = list(trainer_metrics.keys())
    ProgressBar(desc=training_desc).attach(
        trainer, metric_names=train_metric_names
    )
    MetricsLogger(training_desc).attach(trainer, train_metric_names)

    tensorboard_logger.attach(
        trainer,
        OutputHandler(
            tag=training_desc,
            metric_names=train_metric_names,
        ),
        Events.ITERATION_COMPLETED,
    )


    def run_evaluator(evaluator_desc):
        return lambda engine: evaluators[evaluator_desc].run(
            evaluate_data_loaders[evaluator_desc]
        )


    for evaluator_desc, evaluator in evaluators.items():
        evaluator_metric_names = list(evaluator_metrics[evaluator_desc].keys())

        trainer.add_event_handler(
            Events.EPOCH_COMPLETED, run_evaluator(evaluator_desc),
        )

        ProgressBar(desc=evaluator_desc).attach(evaluator)
        MetricsLogger(evaluator_desc).attach(evaluator, evaluator_metric_names)
        tensorboard_logger.attach(
            evaluator,
            OutputHandler(
                tag=evaluator_desc,
                metric_names=evaluator_metric_names,
                global_step_transform=global_step_from_engine(trainer),
            ),
            Events.EPOCH_COMPLETED,
        )

    if type(optimizers) is not dict:
        optimizers = dict(optimizer=optimizers)

    for name, optimizer in optimizers.items():
        tensorboard_logger.attach(
            trainer,
            log_handler=OptimizerParamsHandler(
                tag=f'{training_desc}/{name}',
                param_name='lr',
                optimizer=optimizer,
            ),
            event_name=Events.ITERATION_COMPLETED,
        )

    trainer.add_event_handler(
        Events.ITERATION_COMPLETED, ignite.handlers.TerminateOnNan(),
    )

    return trainer, evaluators, tensorboard_logger
