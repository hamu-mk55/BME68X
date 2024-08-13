import os
import time
import datetime
from logging import (getLogger, Logger, Formatter,
                     FileHandler, StreamHandler, handlers,
                     DEBUG, INFO, WARNING, ERROR, CRITICAL)


def _set_level(level: str)->int:
    if level.lower() == 'debug':
        return DEBUG
    elif level.lower() == 'info':
        return INFO
    elif level.lower() == 'warning':
        return WARNING
    elif level.lower() == 'error':
        return ERROR
    elif level.lower() == 'critical':
        return CRITICAL
    else:
        return WARNING


def _set_format(date_fmt=None, fmt=None)->Formatter:

    if date_fmt is None:
        date_fmt = '%m/%d,%H:%M:%S'

    if fmt is None:
        fmt = '%(asctime)s,%(msecs)03d,[%(levelname).4s][%(funcName)s][%(lineno)d], %(message)s'

    return Formatter(fmt, datefmt=date_fmt)


def make_logger(log_dir: str = './log',
                level: str = 'info',
                file_name: str = 'mylogger',
                console_out: bool = True,
                file_out: bool = True,
                use_time_rotate: bool = True,
                date_fmt:str = None,
                fmt:str = None,
                logger_id: str = 'MyLogger') -> Logger:
    # Set logger
    log_level = _set_level(level)
    log_formatter = _set_format(date_fmt=date_fmt, fmt=fmt)

    logger = getLogger(logger_id)
    logger.setLevel(log_level)

    # Set File-Output
    if file_out:
        os.makedirs(log_dir, exist_ok=True)

        log_file = f'{log_dir}/{file_name}.log'
        if use_time_rotate:
            fh = handlers.TimedRotatingFileHandler(
                log_file,
                when="MIDNIGHT"
            )
        else:
            fh = FileHandler(log_file)

        fh.setLevel(log_level)
        fh.setFormatter(log_formatter)
        logger.addHandler(fh)

    # Set Console-Output
    if console_out:
        sh = StreamHandler()
        sh.setLevel(log_level)
        sh.setFormatter(log_formatter)
        logger.addHandler(sh)

    return logger


def example():
    logger = make_logger()

    while True:
        logger.debug('test_debug')
        logger.info('test_info')
        logger.warning('test_warn')
        logger.error('test_err')
        logger.critical('test_crt')
        logger.log(INFO, 'test_log')

        time.sleep(30)


if __name__ == '__main__':
    example()
