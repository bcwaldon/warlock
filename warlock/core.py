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

from jsonschema.validators import validator_for

from . import model


def model_factory(schema, base_class=model.Model, name=None, resolver=None):
    """Generate a model class based on the provided JSON Schema

    :param schema: dict representing valid JSON schema
    :param name: A name to give the class, if `name` is not in `schema`
    """
    schema = copy.deepcopy(schema)
    resolver = resolver

    class Model(base_class):
        def _setnested(self, path: list[str], value, root=None):
            if root is None:
                root = self
            if len(path) > 1:
                head = path[0]
                if not head in root:
                    root[head] = {}
                self._setnested(path[1:], value, root=root[head])
            elif len(path) == 1:
                root[path[0]] = value

        def _pathexists(self, path: list[str], root=None):
            if root is None:
                root = self
            if len(path) == 1:
                return path[0] in root
            elif len(path) == 0:
                return False
            else:
                head = path[0]
                if head in root:
                    return self._pathexists(path[1:], root=root[head])
                else:
                    return False

        def _setdefaults(self, path: list[str], schema_props: dict):
            for name, prop in schema_props.items():
                if "type" in prop:
                    local_path = path.copy()
                    local_path.append(name)
                    if prop["type"] == "object":
                        if "properties" in prop:
                            self._setdefaults(local_path, prop["properties"])
                    elif "default" in prop and not name in self:
                        if not self._pathexists(local_path):
                            self._setnested(local_path, prop["default"])

        def __init__(self, *args, **kwargs):
            self.__dict__["schema"] = schema
            self.__dict__["resolver"] = resolver

            cls = validator_for(self.schema)
            if resolver is not None:
                self.__dict__["validator_instance"] = cls(schema, resolver=resolver)
            else:
                self.__dict__["validator_instance"] = cls(schema)

            base_class.__init__(self, *args, **kwargs)

            if "properties" in schema:
                self._setdefaults([], schema["properties"])

    if resolver is not None:
        Model.resolver = resolver

    if name is not None:
        Model.__name__ = name
    elif "name" in schema:
        Model.__name__ = str(schema["name"])
    return Model
