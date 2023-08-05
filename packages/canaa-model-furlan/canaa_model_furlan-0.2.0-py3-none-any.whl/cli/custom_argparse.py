import argparse
import sys as _sys
from cli.logging import get_logger


class CustomArgumentParser(argparse.ArgumentParser):

    _testing = False
    log = get_logger()

    def set_testing(self, value):        
        self.log.debug('CustomArgumentParser -> TESTING = %s', value)
        self._testing = True if value else False

    def exit(self, status=None, message=None):
        if message:
            self._print_message(message, _sys.stderr)
        if self._testing:
            self.log.warning('EXITING: %s', self._testing)
            raise Exception('Exiting with status {0}'.format(status))
        else:
            _sys.exit(status)
