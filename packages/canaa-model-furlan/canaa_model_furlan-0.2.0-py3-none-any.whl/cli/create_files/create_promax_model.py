from cli.imports import Imports
from cli.model_creator import ModelCreator
from cli.model_field import ModelField
from cli.utils import camel_to_snake, created_by, snake_to_camel


def create_promax_model(model: ModelCreator, old_canaa_base: bool):
    _imports = Imports()
    _imports.add("canaa_base", "BaseModel")

    linhas = []
    linhas.append('class {0}Model(BaseModel):\n'.format(
        snake_to_camel(model.info.promax_model)))

    linhas.append('\tdef __init__(self, arg: dict):')
    linhas.append('\t\tsuper().__init__(arg)\n')

    field: ModelField = None
    for field in model.fields:
        com = "\n\t\t# " + field.field_ms
        linhas.append(com)
        if field.primitive_type:
            campo = "\t\tself.{0}: {1} = \\\n\t\t\tself.get_value('{0}', field_type={1}, required={2})".format(
                field.field_promax,
                field.type_promax,
                field.required
            )
            for datetime_type in ['datetime', 'time', 'date']:
                if datetime_type in [field.type_promax, field.type_ms]:
                    _imports.add('datetime', datetime_type)
        else:
            campo = "\t\tself.{0}: {1}Model = \\\n\t\t\t{1}Model(\n\t\t\t\tself.get_value('{0}', field_type=dict, required={2}))".format(
                field.field_promax,
                snake_to_camel(field.type_promax),
                field.required
            )
            _imports.add('domain.models.promax.{0}.{1}'.format(
                model.info.namespace_promax,
                camel_to_snake(field.type_promax)+"_model"),
                snake_to_camel(field.type_promax)+"Model")

        linhas.append(campo)

    linhas.insert(0, _imports.to_code())

    linhas.insert(0, created_by())

    return "\n".join(linhas)
