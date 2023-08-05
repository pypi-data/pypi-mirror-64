class ModelCandidate:

    def __init__(self,
                 promax_namespace: str,
                 promax_name: str,
                 promax_fields: list,
                 ms_namespace: str,
                 ms_name: str,
                 ms_fields: list):
        self._validate_args(promax_namespace, promax_name, promax_fields,
                            ms_namespace, ms_name, ms_fields)
        self._promax_ns = promax_namespace
        self._promax_name = promax_name
        self._promax_fields = promax_fields
        self._ms_ns = ms_namespace
        self._ms_name = ms_name
        self._ms_fields = ms_fields

    def set_namespaces(self, promax_namespace, ms_namespace):
        if not(isinstance(promax_namespace, str) and promax_namespace and
               isinstance(ms_namespace, str) and ms_namespace):
            raise TypeError(
                "Invalid namespaces: {0}".format(
                    [promax_namespace, ms_namespace]
                ))
        self._promax_ns = promax_namespace
        self._ms_ns = ms_namespace

    def _validate_args(self,
                       promax_namespace, promax_name, promax_fields,
                       ms_namespace, ms_name,  ms_fields):
        if not(isinstance(promax_namespace, str) and promax_namespace and
               isinstance(promax_name, str) and promax_name and
               isinstance(ms_namespace, str) and ms_namespace and
               isinstance(ms_name, str) and ms_name and
               isinstance(promax_fields, list) and
               isinstance(ms_fields, list)):
            raise TypeError(
                "Invalid arguments: {0}".format(
                    [promax_namespace, promax_name, promax_fields,
                     ms_namespace, ms_name,  ms_fields]
                ))

        if len(promax_fields) != len(ms_fields) or \
                len(promax_fields) == 0:
            raise ModelCandidateException(
                "Not matching fields: {0} - {1}".format(
                    promax_fields,
                    ms_fields))

        for fields in [promax_fields, ms_fields]:
            for field in fields:
                if not isinstance(field, tuple) or len(field) != 2:
                    raise ModelCandidateException(
                        "Expected tuple ('field_name','field_type'): {0}".format(field))

    def generate_model_definition(self) -> list:
        """
        Used to create a model, in ModelCreator.load_from_list
        """
        md = []
        # Header
        md.append("{0}.{1};{2}.{3}".format(
            self._promax_ns,
            self._promax_name,
            self._ms_ns,
            self._ms_name
        ))
        for i in range(len(self._promax_fields)):
            promax_field, promax_type = self._promax_fields[i]
            ms_field, ms_type = self._ms_fields[i]
            md.append("{0};{1};{2};{3};".format(
                promax_field,
                promax_type,
                ms_field,
                ms_type
            ))

        return md

    def __str__(self):
        return "{0}:{1}".format(self._promax_name, self._ms_name)


class ModelCandidateException(Exception):
    pass
