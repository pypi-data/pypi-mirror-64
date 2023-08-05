from cli.model_creator import ModelCreator
from cli.model_field import ModelField
from cli.utils import camel_to_snake
from cli.cache import get_cache


def create_promax_json(model: ModelCreator, destiny_folder: str):
    cache = get_cache()
    result = {}
    field: ModelField = None
    for field in model.fields:
        if field.primitive_type:
            result[field.field_promax] = eval(field.default_value)
        else:
            result[field.field_promax] = cache.get_value(
                'promax', camel_to_snake(field.type_promax)+'_model.py')

    if cache.set_value('promax', model.promax_model_file_name, result):
        return cache.export_to_json('promax', model.promax_model_file_name, destiny_folder)
