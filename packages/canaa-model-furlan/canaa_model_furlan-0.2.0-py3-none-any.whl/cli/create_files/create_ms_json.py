from cli.cache import get_cache
from cli.model_creator import ModelCreator
from cli.model_field import ModelField
from cli.utils import camel_to_snake


def create_ms_json(model: ModelCreator, destiny_folder: str):
    cache = get_cache()

    result = {}
    field: ModelField = None
    for field in model.fields:
        if field.primitive_type:
            result[field.field_ms] = eval(field.default_value)
        else:
            result[field.field_ms] = cache.get_value(
                'ms', camel_to_snake(field.type_ms)+'_model.py')

    if cache.set_value('ms', model.ms_model_file_name, result):
        return cache.export_to_json('ms', model.ms_model_file_name, destiny_folder)
