"""
Parses model definition by JSON

Example:
{
    "id":"int",
    "name":"str",
    "active":true,
    "number":10,
    "number2":"int"
}

All the key and values from JSON must be string or primitive type
"""
import collections
import json

from cli.logging import get_logger

from .primitive_types import get_type_from_str

LOG = get_logger()


def parse_json_model(model: str, modelname: str) -> list:
    """
    Parse JSON defined model, returning list of tuples (fieldname, fieldtype)
    """
    LOG.info('Parsing JSON submodel %s', modelname)
    try:
        model_data = json.loads(
            model, object_pairs_hook=collections.OrderedDict,)
    except json.JSONDecodeError as exc:
        LOG.critical('INVALID JSON: %s (%s)', model, str(exc))
        return None
    except Exception as exc:
        LOG.error('UNEXPECTED ERROR (%s) ON JSON LOADING: %s', str(exc), model)
        return None

    fields = []
    for key in model_data:
        value = model_data[key]
        value_type = parse_value_type(value)
        if not value_type:
            LOG.critical('INVALID TYPE FOR FIELD %s: %s - COMPLETE MODEL: %s',
                         key, value, model_data)
            return None
        fields.append((key, value_type))

    if len(fields) > 0:
        LOG.info('  FIELDS: %s', fields)
        return fields

    LOG.critical('  NO FIELDS IN SUBMODEL %s', modelname)
    return None


def parse_value_type(value):
    if isinstance(value, str):
        value_type = get_type_from_str(value)
    elif isinstance(value, int):
        value_type = 'int'
    elif isinstance(value, float):
        value_type = 'float'
    elif isinstance(value, bool):
        value_type = 'bool'
    else:
        # data type error
        value_type = ''

    return value_type
