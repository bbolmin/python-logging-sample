import sys
from loguru import logger

CONFIG_INFO = {
    'format': '<m>[{time:YYYY-MM-DD HH:mm:ss}]</m> |<g>{level}</g>| {message}',
    'save_path': './log/info.txt',
    'rotation': '1days'
}

CONFIG_DEBUG = {
    'format': '<m>[{time:YYYY-MM-DD HH:mm:ss}]</m> |<c>{level}</c>| {file} ({line} line) | {message}',
    'save_path': './log/debug.txt',
    'rotation': '1days'
}

CONFIG_ERROR = {
    'format': '<m>[{time:YYYY-MM-DD HH:mm:ss}]</m> |<r>{level}</r>| {file} ({line} line) | {message}',
    'save_path': './log/error.txt',
    'rotation': '1days'
}


class LoggerBase(object):
    def __init__(self, level, config):
        self.level = level.upper()
        self.config = config
        self.set_handler()

    def set_handler(self):
        logger.add(sys.stdout, format=self.config['format'], filter=self.__base_filter)
        if 'save_path' in self.config:
            if 'rotation' in self.config:
                logger.add(self.config['save_path'], format=self.config['format'], filter=self.__file_filter,
                           rotation=self.config['rotation'])
            else:
                logger.add(self.config['save_path'], format=self.config['format'], filter=self.__file_filter)

    def __exception_check(self, record):
        if record['exception'] is None:
            return False
        return True

    def __base_filter(self, record):
        return record["level"].name == self.level

    def __file_filter(self, record):
        if record["level"].name != self.level:
            return False
        return ('save' in record['extra'] and record['extra']['save']) or self.__exception_check(record)


def initialize_logger():
    logger.remove()

    LoggerBase('INFO', CONFIG_INFO)
    LoggerBase('DEBUG', CONFIG_DEBUG)
    LoggerBase('ERROR', CONFIG_ERROR)


initialize_logger()

if __name__ == "__main__":
    logger.info('info level print test')
    logger.debug('debug level print test')
    logger.error('error level print test')
    logger.info('file test', save=True)
    try:
        raise ValueError("test Exception")
    except Exception as e:
        logger.exception(e)


'''
# Level 	Severity 	   method
# TRACE 		5		logger.trace()
# DEBUG 		10		logger.debug()
# INFO  		20		logger.info()
# SUCCESS		25		logger.success()
# WARNING		30		logger.warning()
# ERROR 		40		logger.error()
# CRITICAL		50		logger.critical()

 
@logger.catch
def my_function(x, y, z):
    # An error? It's caught anyway!
    return 1 / (x + y + z)
'''
