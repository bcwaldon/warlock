#import jsonschema


def Class(schema):
    class schema_class(object):
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

    return schema_class
