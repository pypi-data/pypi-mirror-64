from cli import __description__, __version__, __tool_name__

_help = {
    "version": "{description} v{version}",
    "example": """
The file must be an CSV (separated by ; fields), UTF-8 without BOM encoding

The first line defines the model names:
    - Promax namespace
    - Promax model name
    - Microservice namespace
    - Microservice model name

The next lines defines the fields:
    - Promax field name
    - Promax field type (int, bool, string, date, datetime, time, float or classes)
    - Microservice field name
    - Microservice field type
    - Extra informations: 'pk' for Primary Key, 'required' for required field

promax_namespace.promax_model;microservice_namespace.microservice_model
codigo_modelo;int;model_id;int;pk
nome_pessoa;string;person_name;string;required
data_nascimento;date;birth_date;date;
ativo;bool;active;bool;
cadastro;datetime;register;datetime
taxa;float;rate;float
descricao;DescricaoModel;description;DescriptionModel
""",
    "usage": """

Gets an metadata model example:
    {tool_name} --example

Validates an metadata model
    {tool_name} --source metadata_model.csv --just-validate

Generates models from metadata model
    {tool_name} --source metadata_model.csv --destiny output_folder

    {tool_name} --source metadata_models_folder --destiny output_folder

    {tool_name} --source metadata_model.xlsx --destiny output_folder

"""}

for key in _help:
    _help[key] = _help[key].format(
        tool_name=__tool_name__,
        version=__version__,
        description=__description__)


def get_help(what):
    if what in _help:
        return _help[what]
    return "# ERROR: {0} ISN´T A SOURCE OF HELP"


def print_help(what):
    print(get_help(what))

    return 0
