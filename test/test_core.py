import copy
import unittest

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
        fixture_copy['name'] = unicode(fixture_copy['name'])
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
        self.assertEqual(set(list(sweden.iteritems())),
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

        mike_2 = dict(mike.iteritems())
        mike_2['sub']['foo'] = 'james'
        self.assertEquals(mike.sub['foo'], 'mike')

        mike_2 = dict(mike.items())
        mike_2['sub']['foo'] = 'james'
        self.assertEquals(mike.sub['foo'], 'mike')

        mike_3_sub = list(mike.itervalues())[0]
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
        self.assertRaises(exc, sweden.__delitem__, 'name')

    def test_dict_syntax(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name='Sweden', population=9379116)
        self.assertEqual(sweden['name'], 'Sweden')
        sweden['name'] = 'Finland'
        self.assertEqual(sweden['name'], 'Finland')

    def test_changes(self):
        Country = warlock.model_factory(fixture)
        sweden = Country(name='Sweden', population=9379116)
        self.assertEqual(sweden.changes, {})
        sweden['name'] = 'Finland'
        self.assertEqual(sweden.changes, {'name': 'Finland'})
        sweden['name'] = 'Norway'
        self.assertEqual(sweden.changes, {'name': 'Norway'})
