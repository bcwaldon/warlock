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
import unittest

import six

import warlock


fixture = {
    'name': 'Country',
    'properties': {
        'name': {'type': 'string'},
        'population': {'type': 'integer'},
    },
    'additionalProperties': False,
}


complex_fixture = {
    'name': 'Mixmaster',
    'properties': {
        'sub': {'type': 'object',
                'properties': {'foo': {'type': 'string'}}}
    },
}


class TestCore(unittest.TestCase):
    def test_create_invalid_object(self):
        Country = warlock.model_factory(fixture)
        self.assertRaises(ValueError, Country, name=1)

    def test_class_name_from_unicode_schema_name(self):
        fixture_copy = copy.deepcopy(fixture)
        fixture_copy['name'] = six.text_type(fixture_copy['name'])
        # Can't set class.__name__ to a unicode object, ensure warlock
        # does some magic to make it possible
        warlock.model_factory(fixture_copy)

    def test_invalid_operations(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name='Sweden', population=9379116)

        # Ensure a valid object was created
        self.assertEqual(sweden.name, 'Sweden')
        self.assertEqual(sweden.population, 9379116)

        # Specific exceptions should be raised for invalid operations
        self.assertRaises(AttributeError, getattr, sweden, 'overlord')
        exc = warlock.InvalidOperation
        self.assertRaises(exc, setattr, sweden, 'overlord', 'Bears')
        self.assertRaises(exc, setattr, sweden, 'name', 5)
        self.assertRaises(exc, setattr, sweden, 'population', 'N/A')

    def test_no_mask_arbitrary_properties(self):
        fixture_copy = copy.deepcopy(fixture)
        fixture_copy['additionalProperties'] = {'type': 'string'}
        Country = warlock.model_factory(fixture_copy)

        # We should still depend on the schema for validation
        self.assertRaises(ValueError, Country, GDP=56956)

        # But arbitrary properties should be allowed if they check out
        sweden = Country(overlord='Waldon')
        sweden.abbreviation = 'SE'
        exc = warlock.InvalidOperation
        self.assertRaises(exc, setattr, sweden, 'abbreviation', 0)

    def test_items(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name='Sweden', population=9379116)
        self.assertEqual(set(list(six.iteritems(sweden))),
                         set([('name', 'Sweden'), ('population', 9379116)]))
        self.assertEqual(set(sweden.items()),
                         set([('name', 'Sweden'), ('population', 9379116)]))

    def test_update(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name='Sweden', population=9379116)
        exc = warlock.InvalidOperation
        self.assertRaises(exc, sweden.update, {'population': 'N/A'})
        self.assertRaises(exc, sweden.update, {'overloard': 'Bears'})

    def test_deepcopy(self):
        """Make sure we aren't leaking references."""
        Mixmaster = warlock.model_factory(complex_fixture)
        mike = Mixmaster(sub={'foo': 'mike'})

        self.assertEquals(mike.sub['foo'], 'mike')

        mike_1 = mike.copy()
        mike_1['sub']['foo'] = 'james'
        self.assertEquals(mike.sub['foo'], 'mike')

        mike_2 = dict(six.iteritems(mike))
        mike_2['sub']['foo'] = 'james'
        self.assertEquals(mike.sub['foo'], 'mike')

        mike_2 = dict(mike.items())
        mike_2['sub']['foo'] = 'james'
        self.assertEquals(mike.sub['foo'], 'mike')

        mike_3_sub = list(six.itervalues(mike))[0]
        mike_3_sub['foo'] = 'james'
        self.assertEquals(mike.sub['foo'], 'mike')

        mike_3_sub = list(mike.values())[0]
        mike_3_sub['foo'] = 'james'
        self.assertEquals(mike.sub['foo'], 'mike')

    def test_forbidden_methods(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name='Sweden', population=9379116)
        exc = warlock.InvalidOperation
        self.assertRaises(exc, sweden.clear)
        self.assertRaises(exc, sweden.pop, 0)
        self.assertRaises(exc, sweden.popitem)

    def test_dict_syntax(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name='Sweden', population=9379116)

        sweden['name'] = 'Finland'
        self.assertEqual(sweden['name'], 'Finland')

        del sweden['name']
        self.assertRaises(AttributeError, getattr, sweden, 'name')

    def test_attr_syntax(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name='Sweden', population=9379116)

        sweden.name = 'Finland'
        self.assertEqual(sweden.name, 'Finland')

        delattr(sweden, 'name')
        self.assertRaises(AttributeError, getattr, sweden, 'name')

    def test_changes(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name='Sweden', population=9379116)
        self.assertEqual(sweden.changes, {})
        sweden['name'] = 'Finland'
        self.assertEqual(sweden.changes, {'name': 'Finland'})
        sweden['name'] = 'Norway'
        self.assertEqual(sweden.changes, {'name': 'Norway'})

    def test_patch_no_changes(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name='Sweden', population=9379116)
        self.assertEqual(sweden.patch, '[]')

    def test_patch_alter_value(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name='Sweden', population=9379116)
        sweden['name'] = 'Finland'
        self.assertEqual(
            sweden.patch,
            '[{"path": "/name", "value": "Finland", "op": "replace"}]')

    def test_patch_drop_attribute(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name='Sweden', population=9379116)
        del sweden['name']
        self.assertEqual(sweden.patch, '[{"path": "/name", "op": "remove"}]')

    def test_patch_reduce_operations(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name='Sweden', population=9379116)

        sweden['name'] = 'Finland'
        self.assertEqual(
            sweden.patch,
            '[{"path": "/name", "value": "Finland", "op": "replace"}]')

        sweden['name'] = 'Norway'
        self.assertEqual(
            sweden.patch,
            '[{"path": "/name", "value": "Norway", "op": "replace"}]')

    def test_patch_multiple_operations(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name='Sweden', population=9379116)

        sweden['name'] = 'Finland'
        sweden['population'] = 5387000
        self.assertEqual(
            sweden.patch,
            '[{"path": "/name", "value": "Finland", "op": "replace"}, '
            '{"path": "/population", "value": 5387000, "op": "replace"}]')
