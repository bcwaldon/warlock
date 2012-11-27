"""Core Warlock functionality"""

import copy

import model

def model_factory(schema, base_class=model.Model):
    """Generate a model class based on the provided JSON Schema

    :param schema: dict representing valid JSON schema
    """
    schema = copy.deepcopy(schema)

    class Model(base_class):
        def __init__(self, *args, **kwargs):
            base_class.__init__(self, schema, *args, **kwargs)

    Model.__name__ = str(schema['name'])
    return Model
