"""Log module."""

# python
import logging as _logging

DEFAULT_FORMAT = '%(asctime)s %(levelname)-8s | %(name)-12s | ' \
                 '%(filename)22s:%(lineno)04d %(funcName)24s | %(message)s'
"""The default format for log messages."""
DEFAULT_DATEFMT = '%Y-%m-%d %H:%M:%S'

# by default use INFO level
_logging.basicConfig(format=DEFAULT_FORMAT, datefmt=DEFAULT_DATEFMT, level=_logging.DEBUG)

# set level according to SPIN_LOGLEVEL
_root_logger = _logging.getLogger()
_root_logger.setLevel(_logging.DEBUG)
_console_log_level = _logging.INFO

# rebind basic log functions
exception = _logging.exception
critical = _logging.critical
error = _logging.error
warn = _logging.warn
warning = _logging.warning
info = _logging.info
debug = _logging.debug
