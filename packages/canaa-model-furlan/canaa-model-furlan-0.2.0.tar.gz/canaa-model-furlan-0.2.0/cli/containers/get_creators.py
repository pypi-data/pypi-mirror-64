import glob
import os

from cli.containers.masked_files_container import MaskedFilesContainer
from cli.containers.metadata_folder_container import FolderContainer
from cli.containers.metadata_xlsx_container import XLSXContainer
from cli.containers.unique_file_container import UniqueFileContainer
from cli.interfaces.metadata_container_interface import \
    MetadataContainerException
from cli.model_creator import ModelCreator
from cli.utils import get_file_extension
from cli.model_candidate import ModelCandidate
CSV = '.csv'
XLSX = '.xlsx'
EXTS = [CSV, XLSX]


def get_container_from_origin(origin: str,
                              ignore_field_errors: bool,
                              just_validate: bool):
    if not isinstance(origin, str) or not origin:
        raise MetadataContainerException('Invalid origin "{0}"'.format(origin))

    if '*' in origin or '?' in origin:
        container = MaskedFilesContainer(
            origin, ignore_field_errors, just_validate)
    elif get_file_extension(origin) == '.xlsx':
        container = XLSXContainer(origin, ignore_field_errors, just_validate)
    elif get_file_extension(origin):
        container = UniqueFileContainer(
            origin, ignore_field_errors, just_validate
        )
    elif not get_file_extension(origin):
        container = FolderContainer(origin, ignore_field_errors, just_validate)
    else:
        raise MetadataContainerException('Invalid origin: "{0}'.format(origin))

    return container


def get_creators(origin: str,
                 ignore_field_errors: bool,
                 just_validate: bool) -> list:
    csv_files, xlsx_files = get_files_from_origin(origin)
    return _get_model_creators(csv_files, xlsx_files,
                               ignore_field_errors, just_validate)


def get_files_from_origin(origin: str):
    if not isinstance(origin, str) or not origin:
        raise MetadataContainerException('Invalid origin "{0}"'.format(origin))

    files = []
    error = None
    if '*' in origin or '?' in origin:
        files, error = _get_masked_files(origin)

    else:
        if os.path.isfile(origin):
            files, error = _get_unique_file(origin)

        elif os.path.isdir(origin):
            files, error = _get_files_from_path(origin)

        else:
            error = 'Origin not found in {0}'.format(origin)

    if error:
        raise MetadataContainerException(error)

    csv_files = [file for file in files
                 if get_file_extension(file) == CSV]
    xlsx_files = [file for file in files
                  if get_file_extension(file) == XLSX]

    return csv_files, xlsx_files


def _get_masked_files(origin):
    """
    Gets csv files from mask
    """

    files = [file
             for file in glob.glob(origin)
             if get_file_extension(file) == CSV]
    error = None if len(
        files) > 0 else 'No valid (.csv) files in {0}'.format(origin)

    return files, error


def _get_unique_file(origin):
    """
    Gets unique file csv or xlsx
    """

    files = []
    error = None
    if get_file_extension(origin) in EXTS:
        if os.path.isfile(origin):
            files = [origin]
        else:
            error = 'File not found {0}'.format(origin)

    else:
        error = 'No valid file (.csv or .xlsx) in {0}'.format(origin)

    return files, error


def _get_files_from_path(origin):
    """
    Gets all csv and xlsx files on folder
    """
    files = [file for file in glob.glob(os.path.join(origin, '*.csv')) +
             glob.glob(os.path.join(origin, '*.xlsx'))
             if not os.path.basename(file).startswith('~')]
    error = None if len(
        files) > 0 else 'No valid (.csv or .xlsx) files in {0}'.format(origin)

    return files, error


def _get_model_creators(csv_files,
                        xlsx_files,
                        ignore_field_errors,
                        just_validate):
    model_creators = []
    for csv_file in csv_files:
        mc = ModelCreator(csv_file, ignore_field_errors, just_validate)
        if mc.is_ok:
            model_creators.append(mc)

    for xlsx_file in xlsx_files:
        cnt = XLSXContainer(xlsx_file, ignore_field_errors, just_validate)
        for mc in cnt.get_model_creators():
            model_creators.append(mc)

    submodel_creators = {}

    for mc in model_creators:
        for submodel in mc.submodels:
            model_candidate: ModelCandidate = mc.submodels[submodel]
            if str(model_candidate) in submodel_creators:
                continue

            model_candidate.set_namespaces(
                mc.info.namespace_promax, mc.info.namespace_ms)

            submodel = ModelCreator(
                model_candidate.generate_model_definition(),
                ignore_field_errors,
                just_validate)

            submodel_creators[str(model_candidate)] = submodel

    if len(submodel_creators) > 0:
        model_creators.extend(submodel_creators.values())

    model_creators = ModelCreator.sorted_creators_list(model_creators)

    return model_creators
