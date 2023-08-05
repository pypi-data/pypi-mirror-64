import logging
import os

_logger = None


def get_logger() -> logging.Logger:
    global _logger
    if not _logger:
        FORMAT = '%(levelname)-8s: %(message)s'
        level = logging.DEBUG if os.getenv('DEBUG', None) else logging.INFO
        logging.basicConfig(level=level,
                            format=FORMAT)

        _logger = logging.getLogger(__name__)

    return _logger
