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

"""Self-validating model for arbitrary objects"""

import copy

import jsonpatch
import jsonschema

from . import exceptions


class Model(dict):
    def __init__(self, *args, **kwargs):
        # we overload setattr so set this manually
        d = dict(*args, **kwargs)

        try:
            self.validate(d)
        except exceptions.ValidationError as exc:
            raise ValueError(str(exc))
        else:
            dict.__init__(self, d)

        self.__dict__["__original__"] = copy.deepcopy(d)

    def __setitem__(self, key, value):
        mutation = dict(self.items())
        mutation[key] = value
        try:
            self.validate(mutation)
        except exceptions.ValidationError as exc:
            msg = "Unable to set '%s' to %r. Reason: %s" % (key, value, exc)
            raise exceptions.InvalidOperation(msg)

        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        mutation = dict(self.items())
        del mutation[key]
        try:
            self.validate(mutation)
        except exceptions.ValidationError as exc:
            msg = "Unable to delete attribute '%s'. Reason: %s" % (key, exc)
            raise exceptions.InvalidOperation(msg) from exc

        dict.__delitem__(self, key)

    def __getattr__(self, key):
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __delattr__(self, key):
        self.__delitem__(key)

    # BEGIN dict compatibility methods

    def clear(self):
        mutation = dict(self.items())
        keys = list(mutation.keys())
        for key in keys:
            del mutation[key]
            try:
                self.validate(mutation)
            except exceptions.ValidationError as exc:
                msg = "Unable to clear data. Reason: %s" % (exc,)
                raise exceptions.InvalidOperation(msg)
        for key in keys:
            del self[key]

    def pop(self, key, *args):
        try:
            value = self.__getitem__(key)
            self.__delitem__(key)
        except KeyError:
            if args:
                return args[0]
            raise
        except exceptions.InvalidOperation as exc:
            msg = "Unable to pop '%s'. Reason: %s" % (key, exc.__context__)
            raise exceptions.InvalidOperation(msg)
        return value

    def popitem(self):
        item = next(iter(self.items()))
        key = item[0]
        try:
            self.__delitem__(key)
        except exceptions.InvalidOperation as exc:
            msg = "Unable to pop next item '%s'. Reason: %s" % (item, exc.__context__)
            raise exceptions.InvalidOperation(msg)
        return item

    def copy(self):
        return copy.deepcopy(dict(self))

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        return copy.deepcopy(dict(self), memo)

    def update(self, other):
        mutation = dict(self.items())
        mutation.update(other)
        try:
            self.validate(mutation)
        except exceptions.ValidationError as exc:
            raise exceptions.InvalidOperation(str(exc))
        dict.update(self, other)

    def items(self):
        return copy.deepcopy(dict(self)).items()

    def values(self):
        return copy.deepcopy(dict(self)).values()

    # END dict compatibility methods

    @property
    def patch(self):
        """Return a jsonpatch object representing the delta"""
        original = self.__dict__["__original__"]
        return jsonpatch.make_patch(original, dict(self)).to_string()

    def validate(self, obj=None):
        """Apply a JSON schema to an object"""
        if obj is None:
            obj = self
        try:
            if self.resolver is not None:
                jsonschema.validate(obj, self.schema, resolver=self.resolver)
            else:
                jsonschema.validate(obj, self.schema)
        except jsonschema.ValidationError as exc:
            raise exceptions.ValidationError(str(exc))
