# logging_config.py
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Log to stdout
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'app.log',  # Log to a file
            'mode': 'a', # Append to the log file
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'openai-git-agent': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
