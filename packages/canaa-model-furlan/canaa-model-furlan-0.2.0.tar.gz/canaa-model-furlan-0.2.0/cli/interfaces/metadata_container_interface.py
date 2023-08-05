import glob
import os
from abc import ABCMeta, abstractmethod


class IMetadataContainer:
    __metaclass__ = ABCMeta

    def __init__(self, origin, ignore_field_errors: bool, just_validate: bool):
        """Metadata container

        :param origin: .csv, .xlsx or folder with .csv files
        :param ignore_field_errors
        :param just_validate
        """
        if not isinstance(origin, str):
            raise TypeError(
                "Invalid type '{0}' for origin".format(type(origin)))
        self.origin = []
        self._model_creators = None
        self._validated = False
        self.ignore_field_errors = ignore_field_errors
        self.just_validate = just_validate

        self.validate_origin(origin)
        if '*' in origin or '?' in origin:
            files = glob.glob(origin)
            if len(files) > 0:
                self.origin = files
        elif os.path.isfile(origin):
            self.origin = [origin]
        elif os.path.isdir(origin):
            # Find csv and xlsx files
            files = [file for file in glob.glob(os.path.join(origin, '*.csv')) +
                     glob.glob(os.path.join(origin, '*.xlsx'))
                     if not os.path.basename(file).startswith('~')]
            if len(files) > 0:
                self.origin = files

        if len(self.origin) == 0:
            raise FileNotFoundError("Not found: {0}".format(origin))

    def get_metadata_files(self):
        return self.origin

    @abstractmethod
    def validate_origin(self, origin):
        """Must validates origin of data

        :param origin: file or folder name

        Must raise exception in case of invalid data
        """
        raise NotImplementedError

    @abstractmethod
    def get_model_creators(self):
        raise NotImplementedError


class MetadataContainerException(Exception):
    pass
