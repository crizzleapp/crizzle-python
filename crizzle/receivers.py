from . import signals
import logging

logger = logging.getLogger('Crizzle')


@signals.receiver(signals.pre_run)
def log_pre_run(instance=None, **kwargs):
    logger.info(f"Starting App '{instance.name}' in mode {instance.mode}")


@signals.receiver(signals.ready)
def log_ready(instance=None, **kwargs):
    logger.debug(f"Crizzle app '{instance.name}' is ready to run.")
