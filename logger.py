import logging


def get_logger(name="auto-labeler", level=logging.INFO):
    """
    Returns a logger with the specified name and logging level.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s [%(filename)s]')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


logger = get_logger()
