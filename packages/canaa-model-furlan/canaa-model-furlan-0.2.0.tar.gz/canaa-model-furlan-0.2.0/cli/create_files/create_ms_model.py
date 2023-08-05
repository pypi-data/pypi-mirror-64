from datetime import datetime

from cli.imports import Imports
from cli.model_creator import ModelCreator
from cli.model_field import ModelField
from cli.utils import camel_to_snake, created_by, snake_to_camel


def create_ms_model(model: ModelCreator, old_canaa_base: bool):
    linhas = [
        'class {0}Model(BaseModel):\n'.format(
            snake_to_camel(model.info.ms_model)),
        '\tdef __init__(self):',
        '\t\tself.integration_fields: dict = {}'
    ]

    _imports = Imports()
    _imports.add('canaa_base', 'BaseModel')

    field: ModelField = None

    for field in model.fields:
        linhas.append('\t\t# {0}'.format(field.field_promax))
        if field.primitive_type:
            linhas.append('\t\tself.{0}: {1} = {2}'.format(
                field.field_ms,
                field.type_ms,
                field.default_value
            ))
        
            for datetime_type in ['datetime', 'time', 'date']:
                if datetime_type in [field.type_promax, field.type_ms]:
                    _imports.add('datetime', datetime_type)
        else:
            linhas.append('\t\tself.{0}: {1} = {2}'.format(
                field.field_ms,
                snake_to_camel(field.type_ms)+'Model',
                field.default_value
            ))
            _imports.add('domain.models.microservice.{0}.{1}_model'.format(
                model.info.namespace_ms,
                camel_to_snake(field.type_ms)),
                snake_to_camel(field.type_ms)+"Model")

    linhas.insert(0, _imports.to_code())
    linhas.insert(0, created_by())

    return "\n".join(linhas)
