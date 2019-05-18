# Warlock — self-validating Python objects using JSON schema

[![PyPI](https://img.shields.io/pypi/v/warlock.svg)][warlock]
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/warlock.svg)][warlock]
[![PyPI - Downloads](https://img.shields.io/pypi/dw/warlock.svg)][pypistats]

[![Build Status](https://travis-ci.org/bcwaldon/warlock.svg?branch=master)][ci-builds]
[![Coverage Status](https://coveralls.io/repos/github/bcwaldon/warlock/badge.svg?branch=master)][coveralls]

## Installation

Warlock is [available on PyPI][warlock]:

```shell
pip install warlock
```

## Usage

1) Create your schema

    ```python
    >>> schema = {
        'name': 'Country',
        'properties': {
            'name': {'type': 'string'},
            'abbreviation': {'type': 'string'},
            'population': {'type': 'integer'},
        },
        'additionalProperties': False,
    }
    ```

2) Create a model

    ```python
    >>> import warlock
    >>> Country = warlock.model_factory(schema)
    ```

3) Create an object using your model

    ```python
    >>> sweden = Country(name='Sweden', abbreviation='SE')
    ```

4) Let the object validate itself

    ```python
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
    ```

5) Generate a [JSON Patch document](http://tools.ietf.org/html/draft-ietf-appsawg-json-patch) to track changes

    ```python
    >>> sweden.population=9453000
    >>> sweden.patch
    '[{"path": "/population", "value": 9453000, "op": "add"}]'
    ```

[warlock]: https://pypi.org/project/warlock/
[pip]: https://pip.pypa.io/en/stable/
[ci-builds]: https://travis-ci.org/bcwaldon/warlock
[coveralls]: https://coveralls.io/github/bcwaldon/warlock?branch=master
[pypistats]: https://pypistats.org/packages/warlock
