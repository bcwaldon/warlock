# Warlock!

1) Create a class

    import warlock

	schema = {
	    'name': 'Country':
	    'properties': {
	        'name': {'type': 'string'},
	        'abbreviation': {'type': 'string'},
	    },
	}

	Country = warlock.schema_class(schema)

2) Create an object using your class

	sweden = Country(name='Sweden', abbreviation='SE')

3) Let the object validate itself!

    sweden.name = 5
    # Raises ValueError

    sweden.overlord = 'Brian'
    # Raises AttributeError
