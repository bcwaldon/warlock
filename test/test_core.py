import unittest

import warlock


class TestCore(unittest.TestCase):
    def test_core(self):
        schema = {
            'name': 'Country',
            'properties': {
                'name': {'type': 'string'},
                'abbreviation': {'type': 'string'},
            },
        }

        Country = warlock.model_factory(schema)

        sweden = Country(name='Sweden', abbreviation='SE')

        self.assertEqual(sweden.name, 'Sweden')
        self.assertEqual(sweden.abbreviation, 'SE')
        self.assertRaises(AttributeError, getattr, sweden, 'overlord')
        self.assertRaises(AttributeError, setattr, sweden, 'overlord', 'Bears')
