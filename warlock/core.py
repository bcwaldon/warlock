# Copyright 2012 Brian Waldon
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Core Warlock functionality"""

import copy

from . import model


def model_factory(schema, resolver=None, base_class=model.Model, name=None):
    """Generate a model class based on the provided JSON Schema

    :param schema: dict representing valid JSON schema
    :param name: A name to give the class, if `name` is not in `schema`
    """
    schema = copy.deepcopy(schema)
    resolver = resolver

    class Model(base_class):
        def __init__(self, *args, **kwargs):
            self.__dict__['schema'] = schema
            self.__dict__['resolver'] = resolver
            base_class.__init__(self, *args, **kwargs)

    if resolver is not None:
        Model.resolver = resolver

    if name is not None:
        Model.__name__ = name
    elif 'name' in schema:
        Model.__name__ = str(schema['name'])
    return Model
