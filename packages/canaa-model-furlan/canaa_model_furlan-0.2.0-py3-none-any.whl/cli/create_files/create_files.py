import os

from cli.logging import get_logger
from cli.model_creator import ModelCreator

from .create_init import create_init
from .process_files import process_files

log = get_logger()


def create_files(model: ModelCreator, destiny_folder: str, **kwargs):

    log.info('Creating model files for {0}'.format(model))

    destiny_folder = os.path.abspath(destiny_folder)

    namespace_promax = model.info.namespace_promax or ""
    # if not model.info.namespace_promax else model.info.namespace_promax
    namespace_ms = model.info.namespace_ms or ""
    # "" if not model.info.namespace_ms else model.info.namespace_ms

    promax_model_folder = os.path.join(
        destiny_folder, 'domain', 'models', 'promax', namespace_promax)
    promax_file = os.path.join(
        promax_model_folder, model.promax_model_file_name)

    ms_model_folder = os.path.join(
        destiny_folder, 'domain', 'models', 'microservice', namespace_ms)
    ms_file = os.path.join(ms_model_folder, model.ms_model_file_name)

    dto_folder = os.path.join(
        destiny_folder, 'domain', 'models', 'dtos', namespace_ms)
    dto_file = os.path.join(dto_folder, model.dto_file_name)
    old_canaa_base = 'old_canaa_base' in kwargs and kwargs['old_canaa_base']

    mock_folder = os.path.join(destiny_folder, 'domain', 'mocks', namespace_ms)

    try:
        folders = []
        for folder in [promax_model_folder,
                       ms_model_folder,
                       dto_folder,
                       mock_folder]:
            if not os.path.isdir(folder):
                os.makedirs(folder)
                create_init(folder)
                folders.append(folder+" [created]")
            else:
                folders.append(folder)
        for folder in folders:
            log.info("Folder: {0}".format(folder))

    except Exception as exc:
        log.error("Folder error: %s", str(exc))
        return False

    return process_files(model, promax_file, ms_file, dto_file, old_canaa_base, mock_folder)
