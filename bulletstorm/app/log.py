# log_config.py
import logging


def setup_logging(name=None):
    if not logging.root.handlers:
        logging.basicConfig(
            level=logging.ERROR,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    if name is not None:
        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG)
        return log
