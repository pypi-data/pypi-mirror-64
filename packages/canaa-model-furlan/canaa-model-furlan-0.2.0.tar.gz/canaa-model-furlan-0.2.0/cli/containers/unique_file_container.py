import os

from cli.interfaces.metadata_container_interface import (
    IMetadataContainer, MetadataContainerException)
from cli.model_creator import ModelCreator
from cli.utils import get_file_extension


class UniqueFileContainer(IMetadataContainer):

    def validate_origin(self, origin):
        if not get_file_extension(origin) in ['.csv', '.xlsx']:
            raise MetadataContainerException(
                'Invalid file type for origin: {0} - Expected .csv or .xlsx file'
                .format(origin))

        if not os.path.isfile(origin):
            raise FileNotFoundError(origin)

        self.origin = [origin]

    def get_model_creators(self):
        if not self._model_creators:
            self._model_creators = []
            for file in self.origin:
                mc = ModelCreator(
                    origin=file,
                    ignore_field_errors=self.ignore_field_errors,
                    just_validate=self.just_validate)
                if mc.is_ok:
                    self._model_creators.append(mc)

        return self._model_creators
