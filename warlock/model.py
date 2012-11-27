"""Self-validating model for arbitrary objects"""

import copy

import jsonschema
import jsonpatch

from errors import *

class Model(dict):
    def __init__(self, schema, *args, **kwargs):
        # Load the validator from the kwargs
        self.__dict__['schema'] = schema

        # we overload setattr so set this manually
        d = dict(*args, **kwargs)

        try:
            self.validator(d)
        except ValidationError as exc:
            raise ValueError(str(exc))
        else:
            dict.__init__(self, d)

        self.__dict__['changes'] = {}
        self.__dict__['__original__'] = copy.deepcopy(d)

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
            msg = "Unable to set '%s' to '%s'" % (key, value)
            raise InvalidOperation(msg)

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
        mutation = dict(self.items())
        del mutation[key]
        try:
            self.validator(mutation)
        except ValidationError:
            msg = "Unable to delete attribute '%s'" % (key)
            raise InvalidOperation(msg)

        dict.__delitem__(self, key)

    def __delattr__(self, key):
        self.__delitem__(key)

    # NOTE(termie): This is kind of the opposite of what copy usually does
    def copy(self):
        return copy.deepcopy(dict(self))

    def update(self, other):
        mutation = dict(self.items())
        mutation.update(other)
        try:
            self.validator(mutation)
        except ValidationError as exc:
            raise InvalidOperation(str(exc))
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

    @property
    def patch(self):
        original = self.__dict__['__original__']
        return jsonpatch.make_patch(original, dict(self)).to_string()

    def validator(self, obj):
        """Apply a JSON schema to an object"""
        try:
            jsonschema.validate(obj, self.schema)
        except jsonschema.ValidationError as exc:
            raise ValidationError(str(exc))
