from .data_type.complex_types import parse_json_model
from .data_type.primitive_types import (get_default_primitive_type_as_str,
                                        get_type_from_str, is_primitive_type)
from .utils import get_words, padr, snake_to_camel
from .model_candidate import ModelCandidate


class ModelField:

    _COL_W = [0, 25, 10, 25, 10, 10]

    def __init__(self, line: str):
        '''
        Obtém um campo da model
        campo_promax;tipo_promax;campo_ms;tipo_ms;extra_info
        utiliza_robin_hood;boolean;uses_robin_hood
        ind_est_vendas;DescricaoModel;sales_state;DescriptionModel
        '''

        self._field_promax: str = None
        self._field_ms: str = None
        self._type_promax: str = None
        self._type_ms: str = None
        self._required: bool = False
        self._pk: bool = False
        self._submodels: dict = {}

        if isinstance(line, str):
            self.load_from_str(line)
        else:
            raise ValueError('line argument must be str')

        self._type_promax, sm_promax_fields = self._validate_type(
            tp=self._type_promax,
            name=self._field_promax)
        self._type_ms, sm_ms_fields = self._validate_type(
            tp=self._type_ms,
            name=self._field_ms)

        if sm_promax_fields:
            if not sm_ms_fields:
                raise ModelFieldException(
                    "Missing submodel for MS in field [%s/%s]",
                    self._field_promax,
                    self._field_ms)
            mc = ModelCandidate(promax_namespace='promax_ns',
                                promax_name=self._field_promax,
                                promax_fields=sm_promax_fields,
                                ms_namespace='ms_ns',
                                ms_name=self._field_ms,
                                ms_fields=sm_ms_fields)
            self._submodels[str(mc)] = mc

        if not self._type_ms:
            self._type_ms = self._type_promax
            if self._type_promax in self._submodels and \
                    self._type_ms not in self._submodels:
                self._submodels[self._type_ms] = self._submodels[self._type_promax]

        if self._type_promax in self._submodels and \
                not self._validate_submodels(self._type_promax, self._type_ms):
            raise ModelFieldException(
                "Invalid submodel definition for field [%s/%s]",
                self._field_promax, self._field_ms)

        if not self.is_ok:
            missing_fields = [field_name for field_name in [
                'field_promax', 'type_promax', 'field_ms']
                if not getattr(self, field_name, None)]
            raise ModelFieldException(
                "Missing {0} : {1}".format(missing_fields, line.strip()))

        if not isinstance(self._pk, bool):
            self._pk = False

        if not isinstance(self._required, bool):
            self._required = False

        self._required |= self._pk

    def __repr__(self):
        return " - ".join([
            "OK" if self.is_ok else "!!",
            self.field_promax+":" + self.type_promax,
            self.field_ms +
            ":"+self.type_ms,
            self.extra,
            self.default_value
        ])

    def __str__(self):
        for index, value in enumerate([self.field_promax,
                                       self.type_promax,
                                       self.field_ms,
                                       self.type_ms,
                                       self.extra,
                                       self.default_value]):
            self._COL_W[index] = max(
                self._COL_W[index], len(value))

        return " - ".join([
            "OK" if self.is_ok else "!!",
            padr(self.field_promax, self._COL_W[0])+":"+padr(
                self.type_promax, self._COL_W[1]),
            padr(self.field_ms, self._COL_W[2]) +
            ":"+padr(self.type_ms, self._COL_W[3]),
            padr(self.extra, self._COL_W[4]),
            padr(self.default_value, self._COL_W[5])
        ])

    def load_from_str(self, line):
        (self._field_promax,
         self._type_promax,
         self._field_ms,
         self._type_ms,
         extra) = get_words(line, 5)
        self._required = extra and extra.lower() == 'required'
        self._pk = extra and extra.lower() == 'pk'

    def _validate_submodels(self, type_promax, type_ms):
        """ Returns True if both submodels have same length """
        return type_promax in self._submodels and \
            type_ms in self._submodels and \
            len(self._submodels[type_promax]) > 0 and \
            len(self._submodels[type_promax]) == len(self._submodels[type_ms])

    @property
    def field_promax(self):
        return self._field_promax

    @property
    def type_promax(self):
        return self._type_promax

    @property
    def field_ms(self):
        return self._field_ms

    @property
    def type_ms(self):
        return self._type_ms

    @property
    def required(self):
        return self._required

    @property
    def extra(self):
        if self._pk:
            return 'pk'
        elif self._required:
            return 'required'
        return ''

    @property
    def is_pk(self) -> bool:
        return self._pk

    @property
    def is_ok(self):
        return self._field_promax and \
            self._type_promax and \
            self.field_ms and \
            self.is_valid_field_name(self._field_promax) and \
            self.is_valid_field_name(self._field_ms)

    @property
    def primitive_type(self):
        return is_primitive_type(self._type_promax)

    @property
    def default_value(self) -> str:
        if not self.primitive_type:
            return snake_to_camel(self.type_ms)+'Model()'
        return get_default_primitive_type_as_str(self.type_ms)

    @property
    def submodels(self) -> dict:
        """
        Returns a dict {"ModelCandidate":ModelCandidate()}
        """
        return self._submodels

    def _validate_type(self, tp: str, name: str = None):
        """
        Validates type, returning ("normalized_type", submodel_fields)
        """
        if tp is None:
            return None, None

        fields = None
        if tp.startswith('{'):
            # Submodel defined in JSON
            fields = parse_json_model(tp, modelname=name)
            if not fields:
                return None, None
            return snake_to_camel(name), fields

        normal_type = get_type_from_str(tp)
        if normal_type != "None":
            tp = normal_type

        return tp, fields

    @classmethod
    def is_valid_field_name(cls, field_name) -> bool:
        if isinstance(field_name, str) and \
                len(field_name) > 0 and \
                (field_name[0] == '_' or field_name[0].isalpha()):
            for c in field_name:
                if not (c == '_' or c.isalpha() or c.isdigit()):
                    return False
            return True

        return False


class ModelFieldException(Exception):
    pass
