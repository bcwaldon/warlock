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

    class Model(dict):
        """Self-validating model for arbitrary objects"""

        def __init__(self, *args, **kwargs):
            d = dict(*args, **kwargs)

            # we overload setattr so set this manually
            self.__dict__['validator'] = validator
            try:
                self.validator(d)
            except ValidationError:
                raise ValueError()
            else:
                dict.__init__(self, d)

            self.__dict__['changes'] = {}

        def __getattr__(self, key):
            try:
                return self.__getitem__(key)
            except KeyError:
                raise AttributeError(key)

        def __setitem__(self, key, value):
            mutation = dict(self.items())
            mutation[key] = value
            try:
                self.validator(mutation)
            except ValidationError:
                raise InvalidOperation()

            dict.__setitem__(self, key, value)

            self.__dict__['changes'][key] = value

        def __setattr__(self, key, value):
            self.__setitem__(key, value)

        def clear(self):
            raise InvalidOperation()

        def pop(self, key, default=None):
            raise InvalidOperation()

        def popitem(self):
            raise InvalidOperation()

        def __delitem__(self, key):
            raise InvalidOperation()

        # NOTE(termie): This is kind of the opposite of what copy usually does
        def copy(self):
            return copy.deepcopy(dict(self))

        def update(self, other):
            mutation = dict(self.items())
            mutation.update(other)
            try:
                self.validator(mutation)
            except ValidationError:
                raise InvalidOperation()
            dict.update(self, other)

        def iteritems(self):
            return copy.deepcopy(dict(self)).iteritems()

        def items(self):
            return copy.deepcopy(dict(self)).items()

        def itervalues(self):
            return copy.deepcopy(dict(self)).itervalues()

        def values(self):
            return copy.deepcopy(dict(self)).values()

        @property
        def changes(self):
            return copy.deepcopy(self.__dict__['changes'])

    Model.__name__ = str(schema['name'])
    return Model
