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
