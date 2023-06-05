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

import copy
import json
import os
import unittest
import warnings

import warlock

fixture = {
    "name": "Country",
    "properties": {"name": {"type": "string"}, "population": {"type": "integer"}},
    "additionalProperties": False,
}


complex_fixture = {
    "name": "Mixmaster",
    "properties": {
        "sub": {"type": "object", "properties": {"foo": {"type": "string"}}}
    },
}

parent_fixture = {
    "name": "Parent",
    "properties": {
        "name": {"type": "string"},
        "children": {"type": "array", "items": {"type": "object"}},
    },
    "required": ["name", "children"],
}

child_fixture = {
    "name": "Child",
    "properties": {"age": {"type": "integer"}, "mother": {"type": "object"}},
    "required": ["age", "mother"],
}


nameless_fixture = {
    "properties": {"name": {"type": "string"}, "population": {"type": "integer"}},
    "additionalProperties": False,
}

default_values = {
    "properties": {
        "name": {"type": "string", "default": "Peter"},
        "lastname": {"type": "string"},
        "height": {
            "type": "object",
            "properties": {
                "value": {"type": "number"},
                "unit": {"type": "string", "default": "m"},
            },
        },
    }
}


class TestCore(unittest.TestCase):
    def test_create_invalid_object(self):
        Country = warlock.model_factory(fixture)
        self.assertRaises(ValueError, Country, name=1)

    def test_invalid_operations(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name="Sweden", population=9379116)

        # Ensure a valid object was created
        self.assertEqual(sweden.name, "Sweden")
        self.assertEqual(sweden.population, 9379116)

        # Specific exceptions should be raised for invalid operations
        self.assertRaises(AttributeError, getattr, sweden, "overlord")
        exc = warlock.InvalidOperation
        self.assertRaises(exc, setattr, sweden, "overlord", "Bears")
        self.assertRaises(exc, setattr, sweden, "name", 5)
        self.assertRaises(exc, setattr, sweden, "population", "N/A")

    def test_no_mask_arbitrary_properties(self):
        fixture_copy = copy.deepcopy(fixture)
        fixture_copy["additionalProperties"] = {"type": "string"}
        Country = warlock.model_factory(fixture_copy)

        # We should still depend on the schema for validation
        self.assertRaises(ValueError, Country, GDP=56956)

        # But arbitrary properties should be allowed if they check out
        sweden = Country(overlord="Waldon")
        sweden.abbreviation = "SE"
        exc = warlock.InvalidOperation
        self.assertRaises(exc, setattr, sweden, "abbreviation", 0)

    def test_items(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name="Sweden", population=9379116)
        self.assertEqual(
            set(list(sweden.items())),
            set([("name", "Sweden"), ("population", 9379116)]),
        )
        self.assertEqual(
            set(sweden.items()), set([("name", "Sweden"), ("population", 9379116)])
        )

    def test_update(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name="Sweden", population=9379116)
        exc = warlock.InvalidOperation
        self.assertRaises(exc, sweden.update, {"population": "N/A"})
        self.assertRaises(exc, sweden.update, {"overloard": "Bears"})

    def test_naming(self):
        Country = warlock.model_factory(fixture)
        self.assertEqual("Country", Country.__name__)

        Country2 = warlock.model_factory(fixture, name="Country2")
        self.assertEqual("Country2", Country2.__name__)

        nameless = warlock.model_factory(nameless_fixture)
        self.assertEqual("Model", nameless.__name__)

        nameless2 = warlock.model_factory(nameless_fixture, name="Country3")
        self.assertEqual("Country3", nameless2.__name__)

    def test_deepcopy(self):
        """Make sure we aren't leaking references."""
        Mixmaster = warlock.model_factory(complex_fixture)
        mike = Mixmaster(sub={"foo": "mike"})

        self.assertEqual("mike", mike.sub["foo"])

        mike_1 = mike.copy()
        mike_1["sub"]["foo"] = "james"
        self.assertEqual("mike", mike.sub["foo"])

        mike_2 = dict(mike.items())
        mike_2["sub"]["foo"] = "james"
        self.assertEqual("mike", mike.sub["foo"])

        mike_3_sub = list(mike.values())[0]
        mike_3_sub["foo"] = "james"
        self.assertEqual("mike", mike.sub["foo"])

    def test_forbidden_methods(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name="Sweden", population=9379116)
        exc = warlock.InvalidOperation
        self.assertRaises(exc, sweden.clear)
        self.assertRaises(exc, sweden.pop, 0)
        self.assertRaises(exc, sweden.popitem)

    def test_dict_syntax(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name="Sweden", population=9379116)

        sweden["name"] = "Finland"
        self.assertEqual("Finland", sweden["name"])

        del sweden["name"]
        self.assertRaises(AttributeError, getattr, sweden, "name")

    def test_attr_syntax(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name="Sweden", population=9379116)

        sweden.name = "Finland"
        self.assertEqual("Finland", sweden.name)

        delattr(sweden, "name")
        self.assertRaises(AttributeError, getattr, sweden, "name")

    def test_changes(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name="Sweden", population=9379116)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(sweden.changes, {})
            assert w[0].category == DeprecationWarning
        sweden["name"] = "Finland"
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(sweden.changes, {"name": "Finland"})
            assert w[0].category == DeprecationWarning
        sweden["name"] = "Norway"
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(sweden.changes, {"name": "Norway"})
            assert w[0].category == DeprecationWarning

    def test_patch_no_changes(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name="Sweden", population=9379116)
        self.assertEqual(sweden.patch, "[]")

    def test_patch_alter_value(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name="Sweden", population=9379116)
        sweden["name"] = "Finland"
        self.assertEqual(
            json.loads(sweden.patch),
            json.loads('[{"path": "/name", "value": "Finland", "op": "replace"}]'),
        )

    def test_patch_drop_attribute(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name="Sweden", population=9379116)
        del sweden["name"]
        self.assertEqual(
            json.loads(sweden.patch), json.loads('[{"path": "/name", "op": "remove"}]')
        )

    def test_patch_reduce_operations(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name="Sweden", population=9379116)

        sweden["name"] = "Finland"
        self.assertEqual(
            json.loads(sweden.patch),
            json.loads('[{"path": "/name", "value": "Finland", "op": "replace"}]'),
        )

        sweden["name"] = "Norway"
        self.assertEqual(
            json.loads(sweden.patch),
            json.loads('[{"path": "/name", "value": "Norway", "op": "replace"}]'),
        )

    def test_patch_multiple_operations(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name="Sweden", population=9379116)

        sweden["name"] = "Finland"
        sweden["population"] = 5387000

        self.assertEqual(len(json.loads(sweden.patch)), 2)

        patches = json.loads(
            '[{"path": "/name", "value": "Finland", "op": "replace"}, '
            '{"path": "/population", "value": 5387000, "op": "replace"}]'
        )

        for patch in json.loads(sweden.patch):
            self.assertTrue(patch in patches)

    def test_resolver(self):
        from jsonschema import RefResolver

        dirname = os.path.dirname(__file__)
        schemas_path = "file://" + os.path.join(dirname, "schemas/")
        resolver = RefResolver(schemas_path, None)

        country_schema_file = open(os.path.join(dirname, "schemas/") + "country.json")
        person_schema_file = open(os.path.join(dirname, "schemas/") + "person.json")

        country_schema = json.load(country_schema_file)
        person_schema = json.load(person_schema_file)
        Country = warlock.model_factory(country_schema, resolver=resolver)
        Person = warlock.model_factory(person_schema, resolver=resolver)

        england = Country(
            name="England",
            population=53865800,
            overlord=Person(title="Queen", firstname="Elizabeth", lastname="Windsor"),
        )
        expected = {
            "name": "England",
            "population": 53865800,
            "overlord": {
                "title": "Queen",
                "lastname": "Windsor",
                "firstname": "Elizabeth",
            },
        }
        self.assertEqual(england, expected)

    def test_recursive_models(self):
        Parent = warlock.model_factory(parent_fixture)
        Child = warlock.model_factory(child_fixture)

        mom = Parent(name="Abby", children=[])

        teenager = Child(age=15, mother=mom)
        toddler = Child(age=3, mother=mom)

        mom.children = [teenager, toddler]

        self.assertEqual(mom.children[0].age, 15)
        self.assertEqual(mom.children[1].age, 3)

    def test_default_values(self):
        Person = warlock.model_factory(default_values)

        default = Person()
        self.assertEqual(default.name, "Peter")
        self.assertEqual(default.height, {"unit": "m"})

        with_name = Person(name="Mary")
        self.assertEqual(with_name.name, "Mary")
        self.assertEqual(with_name.height, {"unit": "m"})

        with_empty_height = Person(height={})
        self.assertEqual(with_empty_height.name, "Peter")
        self.assertEqual(with_empty_height.height, {"unit": "m"})

        with_height_value = Person(height={"value": 1.2})
        self.assertEqual(with_height_value.name, "Peter")
        self.assertEqual(with_height_value.height, {"value": 1.2, "unit": "m"})

        with_height = Person(height={"value": 120.0, "unit": "cm"})
        self.assertEqual(with_height.name, "Peter")
        self.assertEqual(with_height.height, {"value": 120.0, "unit": "cm"})
