"""Core Warlock functionality"""

import copy

import jsonschema

import model
import exceptions


def model_factory(schema, base_class=model.Model):
    """Generate a model class based on the provided JSON Schema

    :param schema: dict representing valid JSON schema
    """
    schema = copy.deepcopy(schema)

    def validator(obj):
        """Apply a JSON schema to an object"""
        try:
            jsonschema.validate(obj, schema)
        except jsonschema.ValidationError as exc:
            raise exceptions.ValidationError(str(exc))

    class Model(base_class):
        def __init__(self, *args, **kwargs):
            kwargs.setdefault('validator', validator)
            base_class.__init__(self, *args, **kwargs)

    Model.__name__ = str(schema['name'])
    return Model
