# Warlock

Build self-validating python objects using JSON schemas.

1) Create your schema

    >>> schema = {
        'name': 'Country',
        'properties': {
            'name': {'type': 'string'},
            'abbreviation': {'type': 'string'},
            'population': {'type': 'integer'},
        },
        'additionalProperties': False,
    }

2) Create a model

    >>> import warlock
    >>> Country = warlock.model_factory(schema)

3) Create an object using your model

    >>> sweden = Country(name='Sweden', abbreviation='SE')

4) Let the object validate itself

    >>> sweden.name = 5
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "warlock/core.py", line 53, in __setattr__
        raise InvalidOperation(msg)
    warlock.core.InvalidOperation: Unable to set 'name' to '5'

    >>> sweden.overlord = 'Bears'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "warlock/core.py", line 53, in __setattr__
        raise InvalidOperation(msg)
    warlock.core.InvalidOperation: Unable to set 'overlord' to 'Bears'

5) Generate a [JSON Patch document](http://tools.ietf.org/html/draft-ietf-appsawg-json-patch) to track changes

    >>> sweden.population=9453000
    >>> sweden.patch
    '[{"path": "/population", "value": 9453000, "op": "add"}]'
