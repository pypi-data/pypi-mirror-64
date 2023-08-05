from cli.imports import Imports
from cli.model_creator import ModelCreator
from cli.model_field import ModelField
from cli.utils import camel_to_snake, created_by, snake_to_camel


def create_dto(model: ModelCreator, old_canaa_base: bool):
    linhas = [
        'class {0}DTO({0}Model):\n'.format(
            snake_to_camel(model.info.ms_model)), '\tdef __init__(self, arg: {0}Model):'.format(
            snake_to_camel(model.info.promax_model)), '\t\tsuper().__init__()'
    ]

    _imports = Imports()
    _imports.add('canaa_base', 'BaseModel')

    field: ModelField = None
    if len(model.pks) > 0:
        linhas.append('\t\tself.integration_fields = {')
        i = 0
        for field in model.pks:
            i += 1
            linhas.append('\t\t\t"{0}": {1},'.format(
                field.field_ms, i
            ))
        linhas.append('\t\t}\n')

    for field in model.fields:
        if field.primitive_type:
            linhas.append('\t\tself.{0} = arg.{1}'.format(
                field.field_ms,
                field.field_promax
            ))
        else:
            linhas.append('\t\tself.{0} = {1}(arg.{2}).to_dict()'.format(
                field.field_ms,
                snake_to_camel(field.type_ms)+"DTO",
                field.field_promax
            ))
            _imports.add("domain.models.dtos.{0}.{1}".format(
                model.info.namespace_ms,
                camel_to_snake(field.type_ms)+'_dto'
            ), snake_to_camel(field.type_ms)+"DTO")

    _imports.add('domain.models.microservice.{0}.{1}'.format(
        model.info.namespace_ms,
        model.info.ms_model+'_model'
    ), snake_to_camel(model.info.ms_model)+'Model')
    _imports.add('domain.models.promax.{0}.{1}'.format(
        model.info.namespace_promax,
        model.info.promax_model+'_model'
    ), snake_to_camel(model.info.promax_model)+'Model')

    linhas.insert(0, _imports.to_code())
    linhas.insert(0, created_by() + "\n")

    return "\n".join(linhas)
