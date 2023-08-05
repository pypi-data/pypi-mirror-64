import os
import shutil

import autopep8
from cli.logging import get_logger

LOG = get_logger()


def write_file(filename, content) -> bool:
    success = False
    try:
        content = autopep8.fix_code(content, options={
            'aggressive': 1
        })

        backup = ""
        if os.path.isfile(filename):
            mt = os.path.getmtime(filename)
            backup = filename+'.'+str(mt)
            shutil.move(filename, backup)

        with open(filename, 'w') as f:
            f.write(content)

        if os.path.isfile(filename) and os.path.isfile(backup):
            os.unlink(backup)

        success = os.path.isfile(filename)

        LOG.debug('FILE OUTPUT (%s) -> %s', filename, success)

    except Exception as exc:
        LOG.error('FILE OUTPUT (%s) %s', filename, str(exc))

    return success
