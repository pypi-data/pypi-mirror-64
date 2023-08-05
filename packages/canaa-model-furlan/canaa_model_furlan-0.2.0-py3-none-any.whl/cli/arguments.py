"""
Arguments:

*
"""
import argparse
import os
import glob
import sys

from cli import __description__, __version__, __tool_name__
from cli.logging import get_logger
from cli.help import print_help, get_help
from cli.custom_argparse import CustomArgumentParser
from cli.containers.get_creators import get_files_from_origin

SOURCE = 'source'
DESTINY = 'destiny'
IGNORE_FIELD_ERRORS = 'ignore_field_errors'
JUST_VALIDATE = 'just_validate'
EXAMPLE = 'example'
VERSION = 'version'
OLD_CANAA = 'old_canaa_base'
FIELDS = [SOURCE, DESTINY, IGNORE_FIELD_ERRORS,
          JUST_VALIDATE, EXAMPLE, VERSION, OLD_CANAA]


class Arguments:

    _TESTING_ARGS = None
    _INSTANCE = None

    def __init__(self, *args, **kwargs):
        self.log = get_logger()
        self._configs = {
            key: (kwargs[key] if key in kwargs else None)
            for key in FIELDS
        }
        self._parser: argparse.ArgumentParser = None

    def validate(self) -> int:
        """
        Validates arguments and returns:

        0 = OK
        1 = Error
        2 = Can process file
        """
        if self.version:
            return print_help("version")

        if self.example:
            return print_help("example")

        if not self.source:
            self._parser.print_help()
            return 1

        if not self.just_validate and not self.destiny:
            self._parser.print_help()
            return 1

        # check origins
        csv_files, xlsx_files = get_files_from_origin(self.source)
        if not (csv_files or xlsx_files):
            self._parser.error("Invalid source")
            return 1

        return 2

    @classmethod
    def clear(cls):
        cls._INSTANCE = None

    @classmethod
    def create(cls, *testing_args):
        if not cls._INSTANCE:
            if testing_args:
                if not isinstance(testing_args, list):
                    testing_args = list(testing_args)
                if 'testing' in testing_args:
                    cls._TESTING_ARGS = True
                    testing_args.remove('testing')
                if len(testing_args) > 0:
                    sys.argv = [__file__]+testing_args

            get_logger().debug('Arguments: %s', sys.argv)
            parser = cls.create_parser()
            args = parser.parse_args()

            cls._INSTANCE = cls(source=args.source,
                                destiny=args.destiny,
                                ignore_field_errors=args.ignore_field_errors,
                                just_validate=args.just_validate,
                                example=args.example,
                                version=args.version)
            cls._INSTANCE._parser = parser

        return cls._INSTANCE

    @property
    def parser(self) -> argparse.ArgumentParser:
        return self._parser

    @property
    def source(self):
        return self._configs[SOURCE]

    @property
    def destiny(self):
        return self._configs[DESTINY]

    @property
    def ignore_field_errors(self):
        return self._configs[IGNORE_FIELD_ERRORS]

    @property
    def just_validate(self):
        return self._configs[JUST_VALIDATE]

    @property
    def example(self):
        return self._configs[EXAMPLE]

    @property
    def version(self):
        return self._configs[VERSION]

    @property
    def old_canaa_base(self):
        return self._configs[OLD_CANAA]

    @classmethod
    def create_parser(cls) -> argparse.ArgumentParser:
        description = '{0} v{1}'.format(__tool_name__, __version__)
        parser = CustomArgumentParser(
            description=__description__,
            usage=get_help('usage'),
            epilog=description)
        parser.set_testing(cls._TESTING_ARGS is not None)

        parser.add_argument(
            '--source', '-s',
            dest='source',
            help='model metadata file (csv) or folder with csv files (you can use * and ? masks)',
            type=lambda x: source_exists(parser, x))
        parser.add_argument(
            '--destiny', '-d',
            dest='destiny',
            help='Path to create "model" folder and DTO, Promax and Microservice python files and JSON mocks (default = current directory)',
            required=(
                '--source' in sys.argv or '-s' in sys.argv) and not('--just-validate' in sys.argv),
            type=lambda x: is_valid_folder(parser, x))
        parser.add_argument(
            '--ignore-field-errors',
            dest='ignore_field_errors',
            action='store_true',
            help='Don´t stop process when detect error on field definition')
        parser.add_argument(
            '--just-validate',
            dest='just_validate',
            action='store_true',
            help='Just validate model metadata file')
        parser.add_argument(
            '--example', '-e',
            dest='example',
            action='store_true',
            help='print example of metadata file')
        parser.add_argument(
            '--version', '-v',
            dest='version',
            action='store_true')
        parser.add_argument(
            '--old-canaa',
            dest='old_canaa_base',
            action='store_true',
            help='Use field types for canaa_base older than 0.5.0')
        parser.add_argument(
            '--foo',
            action="store_true",
            help=argparse.SUPPRESS)
        parser.set_defaults(ignore_field_errors=False,
                            just_validate=False,
                            example=False,
                            old_canaa_base=False,
                            version=False,
                            destiny_folder='.')

        return parser


def is_valid_folder(parser, arg):
    if not os.path.isdir(arg):
        if Arguments._TESTING_ARGS:
            raise FileNotFoundError(arg)
        parser.error("Folder '{0}' does not exist!".format(arg))
    else:
        return os.path.abspath(arg)


def source_exists(parser, arg):
    if '?' in arg or '*' in arg:
        files = glob.glob(arg)
        if len(files) > 0:
            return os.path.abspath(arg)

    if os.path.isdir(arg) or os.path.isfile(arg):
        return os.path.abspath(arg)

    if Arguments._TESTING_ARGS:
        raise FileNotFoundError(arg)
    parser.error("Source '{0}' does not exist!".format(arg))


def exit(exit_code, exit_exception=None):
    if not Arguments._TESTING_ARGS:    # pragma: no cover
        sys.exit(exit_code)

    if exit_exception:
        raise exit_exception
