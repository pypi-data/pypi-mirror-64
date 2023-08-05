from .containers.get_creators import get_creators
from .create_files import create_files
from .logging import get_logger

log = get_logger()


def process_files(origin: str,
                  destiny_folder: str,
                  just_validate: bool,
                  ignore_field_errors: bool,
                  old_canaa_base: bool):
    success = False
    try:
        creators = get_creators(origin, ignore_field_errors, just_validate)

        if len(creators) > 0:
            success = True
            for mc in creators:
                if mc.is_ok and not just_validate:
                    success &= create_files(mc, destiny_folder,
                                            old_canaa_base=old_canaa_base)

    except Exception as exc:
        log.exception('EXCEPTION: %s', exc)
        success = False

    return success
