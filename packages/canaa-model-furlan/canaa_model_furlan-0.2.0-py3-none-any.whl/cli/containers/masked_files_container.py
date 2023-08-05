import glob

from cli.interfaces.metadata_container_interface import (
    IMetadataContainer, MetadataContainerException)
from cli.model_creator import ModelCreator
from cli.utils import get_file_extension


class MaskedFilesContainer(IMetadataContainer):

    def validate_origin(self, origin):
        files = [file
                 for file in glob.glob(origin)
                 if get_file_extension(file) == '.csv']

        if len(files) > 0:
            self.origin = files
        else:
            raise MetadataContainerException(
                "No .csv files found in {0}".format(origin))

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
