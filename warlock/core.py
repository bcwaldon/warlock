"""Core Warlock functionality"""

import copy

import jsonschema


class InvalidOperation(RuntimeError):
    pass


class ValidationError(ValueError):
    pass


def model_factory(schema):
    """Generate a model class based on the provided JSON Schema

    :param schema: dict representing valid JSON schema
    """
    schema = copy.deepcopy(schema)

    def validator(obj):
        """Apply a JSON schema to an object"""
        try:
            jsonschema.validate(obj, schema)
        except jsonschema.ValidationError:
            raise ValidationError()

    class Model(object):
        """Self-validating model for arbitrary objects"""
        def __init__(self, **kwargs):
            self.__dict__['validator'] = validator
            try:
                self.__dict__['validator'](kwargs)
            except ValidationError:
                raise ValueError()
            else:
                self.__dict__['raw'] = kwargs

            self.__dict__['changes'] = {}

        def __getattr__(self, key):
            try:
                return self.__getitem__(key)
            except KeyError:
                raise AttributeError(key)

        def __getitem__(self, key):
            return self.__dict__['raw'][key]

        def __setitem__(self, key, value):
            mutation = copy.deepcopy(self.__dict__['raw'])
            mutation[key] = value
            try:
                self.__dict__['validator'](mutation)
            except ValidationError:
                raise InvalidOperation()
            self.__dict__['raw'] = mutation
            self.__dict__['changes'][key] = value

        def __setattr__(self, key, value):
            self.__setitem__(key, value)

        def iteritems(self):
            return copy.deepcopy(self.__dict__['raw']).iteritems()

        def items(self):
            return copy.deepcopy(self.__dict__['raw']).items()

        @property
        def changes(self):
            return copy.deepcopy(self.__dict__['changes'])

    Model.__name__ = str(schema['name'])
    return Model
