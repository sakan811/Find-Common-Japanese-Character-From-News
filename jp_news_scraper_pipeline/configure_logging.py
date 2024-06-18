import logging


def configure_logging(logger: logging.Logger = None, logger_name: str = 'root') -> None | logging.Logger:
    """
    Configure logging for the specified logger or get the root logger by default.
    :param logger: Logger to configure.
                    Default is None, which will get the root logger if 'logger_name' is not specified.
    :param logger_name: Specify logger name.
    :return: None or logger.
    """
    # Use the provided logger or get the logger by name
    if logger is None:
        logger = logging.getLogger(logger_name)

    # Clear existing handlers for this logger to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set the logging level
    logger.setLevel(logging.DEBUG)

    # Define a custom log format
    log_format = '%(asctime)s | %(filename)s | line:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s'

    # Create a StreamHandler (which outputs to the terminal)
    stream_handler = logging.StreamHandler()

    # Create a Formatter with the custom log format
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    # Set the Formatter for the StreamHandler
    stream_handler.setFormatter(formatter)

    # Add the StreamHandler to the root logger
    logger.addHandler(stream_handler)

    return logger


def configure_logging_with_file(
        log_file: str,
        logger: logging.Logger = None,
        logger_name: str = 'root',
        print_on_terminal: bool = True) -> None | logging.Logger:
    """
    Configure logging with a log file for the specified logger or get the root logger by default.
    :param log_file: Log file name.
    :param logger: Logger to configure.
                    Default is None, which will get the root logger if 'logger_name' is not specified.
    :param logger_name: Specify logger name.
    :param print_on_terminal: Whether to print logs on the terminal.
                            Default is True.
    :return: None or logger.
    """
    # Use the provided logger or get the logger by name
    if logger is None:
        logger = logging.getLogger(logger_name)

    # Clear existing handlers for this logger to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set the logging level
    logger.setLevel(logging.DEBUG)

    # Define a custom log format
    log_format = '%(asctime)s | %(filename)s | line:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s'

    # Create a FileHandler to write logs to the specified file in overwrite mode
    file_handler = logging.FileHandler(log_file, mode='w')  # 'w' for write mode (overwrite)

    # Create a Formatter with the custom log format
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    # Set the Formatter for the FileHandler
    file_handler.setFormatter(formatter)

    if print_on_terminal:
        # Define a StreamHandler (which outputs to the terminal)
        stream_handler = logging.StreamHandler()
        # Set the Formatter for the StreamHandler
        stream_handler.setFormatter(formatter)
        # Add the StreamHandler to the root logger
        logger.addHandler(stream_handler)

    # Add both the FileHandler to the logger
    logger.addHandler(file_handler)

    return logger
