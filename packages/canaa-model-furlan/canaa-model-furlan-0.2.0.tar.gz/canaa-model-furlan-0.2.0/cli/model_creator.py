import os

from .imports import Imports
from .logging import get_logger
from .model_field import ModelField
from .model_info import ModelInfo
from .utils import camel_to_snake, get_file_extension


class ModelCreator:

    def __init__(self, origin, ignore_field_errors, just_validate):
        self.log = get_logger()
        self.fields = []
        self.info: ModelInfo = None
        self.pks = []
        self._imports = Imports()
        self._ok = False
        self._ignore_field_errors = ignore_field_errors
        self._just_validate = just_validate
        self._has_non_primitive_fields = False
        self._submodels = {}
        if isinstance(origin, list):
            self._ok = self.load_from_list(origin)
        elif isinstance(origin, str):
            if not os.path.exists(origin):
                raise FileNotFoundError(origin)
            ext = get_file_extension(origin).lower()
            if ext:

                self.log.info('ModelCreator: %s', origin)
                if ext == '.csv':
                    self._ok = self.load_from_csv(origin)

            else:
                raise ValueError('Invalid file type: {0}'.format(origin))

    def __str__(self):
        if not self._ok:
            return "ModelCreator data is not loaded"

        return " - ".join([
            str(self.info),
            "{0} fields".format(len(self.fields))])

    def __repr__(self):
        return str(self)

    def __eq__(self, value):
        return isinstance(value, ModelCreator) and \
            str(self.info) == str(value.info)

    @property
    def is_ok(self):
        return self._ok

    @property
    def has_non_primitive_fields(self):
        return self._has_non_primitive_fields

    @property
    def promax_model_file_name(self):
        if self.info:
            return camel_to_snake(self.info.promax_model)+"_model.py"
        return "undefined_promax_model.py"

    @property
    def ms_model_file_name(self):
        if self.info:
            return camel_to_snake(self.info.ms_model)+'_model.py'
        return "undefined_ms_model.py"

    @property
    def dto_file_name(self):
        if self.info:
            return camel_to_snake(self.info.ms_model)+'_dto.py'
        return "undefined_dto_model.py"

    @property
    def submodels(self) -> dict:
        """
        Returns submodels as dict

        {"model_name":[("field1","type"),("field2","type")]}
        """
        return self._submodels

    def load_from_list(self, records: list):
        if not isinstance(records, list) or len(records) < 2:
            return False

        has_head = False

        line_no = 0
        for linha in records:
            linha = linha.strip()
            if linha.startswith('#'):
                continue
            line_no += 1
            if not has_head:
                self.info = ModelInfo(linha)
                has_head = True
            else:
                if not self._add_field(linha, line_no):
                    return False

        return True

    def load_from_csv(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            return self.load_from_list(f.readlines())

    def _add_field(self, field_data, line_no: int = 0):
        if isinstance(field_data, str) and not field_data:
            return True

        try:
            field = ModelField(field_data)
            self._has_non_primitive_fields |= not field.primitive_type
            self._submodels.update(field.submodels)
        except Exception as exc:
            exc_msg = "".join([
                "" if line_no < 1 else "line #{0}: ".format(line_no),
                str(exc)])
            if self._ignore_field_errors:
                self.log.warning(exc_msg)
                return True
            else:
                self.log.error(exc_msg)
                return self._just_validate

        self.log.info(str(field))

        self.fields.append(field)
        if field.is_pk:
            self.pks.append(field)

        for datetime_type in ['datetime', 'time', 'date']:
            if datetime_type in [field.type_promax, field.type_ms]:
                self._imports.add('datetime', datetime_type)

        if not field.primitive_type:
            self._imports.add(self.info.namespace_ms, field.type_ms+'DTO')

        return True

    def imports(self):
        return self._imports.to_code().splitlines()

    @staticmethod
    def sorted_creators_list(creators_list: list):
        # Create unique list
        cd = {str(creator.info): creator for creator in creators_list}
        cl = sorted(
            [cd[n] for n in cd.keys() if cd[n].is_ok],
            key=lambda x: '1' if x.has_non_primitive_fields else '0')

        return cl
