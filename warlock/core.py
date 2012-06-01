"""Core Warlock functionality"""

#import jsonschema


def model_factory(schema):
    """Generate a model class based on the provided JSON Schema

    :param schema: dict representing valid JSON schema
    """
    class Model(object):
        """Self-validating model for arbitrary objects"""
        def __init__(self, **kwargs):
            self.__dict__['raw'] = kwargs

        def __getattr__(self, key):
            try:
                return self.__dict__['raw'][key]
            except KeyError:
                raise AttributeError(key)

        def __setattr__(self, key, value):
            if key in self.__dict__['raw']:
                self.__dict__['raw'][key] = value
            else:
                raise AttributeError(key)

    Model.__name__ = schema['name']
    return Model
