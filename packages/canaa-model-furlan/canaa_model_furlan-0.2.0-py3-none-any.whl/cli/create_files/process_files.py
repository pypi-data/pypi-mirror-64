import os

from cli.create_files.create_dto import create_dto
from cli.create_files.create_init import create_init
from cli.create_files.create_ms_json import create_ms_json
from cli.create_files.create_ms_model import create_ms_model
from cli.create_files.create_promax_json import create_promax_json
from cli.create_files.create_promax_model import create_promax_model
from cli.logging import get_logger
from cli.create_files.file_output import write_file
log = get_logger()


def process_files(model, promax_file, ms_file, dto_file,
                  old_canaa_base, mock_folder):
    processes = {
        "PROMAX": {
            "file": promax_file,
            "method": create_promax_model,
            "json": create_promax_json
        },
        "MICROSERVICE": {
            "file": ms_file,
            "method": create_ms_model,
            "json": create_ms_json
        },
        "DTO": {
            "file": dto_file,
            "method": create_dto,
            "json": lambda x, y: True
        }
    }
    try:
        for process in processes:
            filename = processes[process]['file']
            method = processes[process]['method']
            create_json = processes[process]['json']

            content = method(model, old_canaa_base)
            if os.path.isfile(filename):
                os.remove(filename)

            write_file(filename, content)

            if os.path.isfile(filename):
                log.info('Created %s: %s', process, filename)
            else:
                raise Exception(
                    "File not found after generation: {0}".format(filename))

            create_init(filename)
            create_json(model, mock_folder)

        log.info('Files created successfully!')
        return True

    except Exception as exc:
        log.error('Error on creating %s: %s - %s',
                  process,
                  filename,
                  str(exc))

    return False
