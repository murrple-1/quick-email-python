import os
import sys
import logging

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

_logger = None
def logger():
    global _logger

    if _logger is None:
        _logger = logging.getLogger(__name__)
        _logger.setLevel(logging.getLevelName(LOG_LEVEL))

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(
            logging.Formatter(
                fmt='%(asctime)s (%(levelname)s): %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'))
        _logger.addHandler(stream_handler)

    return _logger
