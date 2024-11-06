import os
import logging
import colorlog
from tools.ansi_configs import colors as COLORS

LOG_DIRECTORY = 'logs'
os.makedirs(LOG_DIRECTORY, exist_ok=True)

class CustomColoredFormatter(colorlog.ColoredFormatter):
    def __init__(self):
        log_format = (
            '%(levelname_log_color)s%(levelname)s%(reset)s : '
            '%(asctime_log_color)s%(asctime)s%(reset)s - '
            '%(name_log_color)s%(name)s%(reset)s : '
            '%(message_log_color)s%(message)s%(reset)s'
        )
        super().__init__(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    def format(self, record):
        record.levelname_log_color = COLORS.get(record.levelname, '\033[0m')
        record.asctime_log_color = '\033[34m'
        record.name_log_color = '\033[36m'
        record.message_log_color = '\033[37m'
        record.reset = '\033[0m'
        return super().format(record)

class LoggerSetup:
    @staticmethod
    def create_file_handler(filename: str, level: int, formatter: logging.Formatter):
        handler = logging.FileHandler(filename)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        return handler

    @staticmethod
    def create_console_handler(level: int, formatter: logging.Formatter):
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        return handler

    @staticmethod
    def configure_logging():
        standard_formatter = logging.Formatter('%(levelname)s : %(asctime)s - %(name)s : %(message)s')

        console_handler = LoggerSetup.create_console_handler(logging.DEBUG, CustomColoredFormatter())
        general_file_handler = LoggerSetup.create_file_handler(os.path.join(LOG_DIRECTORY, 'app.log'), logging.DEBUG, standard_formatter)
        error_file_handler = LoggerSetup.create_file_handler(os.path.join(LOG_DIRECTORY, 'error.log'), logging.ERROR, standard_formatter)

        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'console': console_handler,
                'file_general': general_file_handler,
                'file_error': error_file_handler,
            },
            'loggers': {
                'FATHER': {
                    'handlers': ['console', 'file_general', 'file_error'],
                    'level': logging.DEBUG,
                    'propagate': False,
                },
                'prisma': {
                    'handlers': ['console', 'file_general', 'file_error'],
                    'level': logging.WARNING,
                    'propagate': False,
                },
            },
        }
        logging.config.dictConfig(logging_config)

LoggerSetup.configure_logging()

def get_logger(name: str):
    return logging.getLogger(name)

logger = get_logger("FATHER")
