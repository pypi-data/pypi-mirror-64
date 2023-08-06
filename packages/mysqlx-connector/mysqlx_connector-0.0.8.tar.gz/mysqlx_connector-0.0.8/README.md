# MySQL X connector for python

This repo contains a skeleton for mysqlx connector. User has to just create a specific table class which inherits provided table class. Users own table class can contain any kinds of methods to manipulate the table.

This connector uses environment variables to connect to the database. You _need_ to set HOST, PORT, USER, and PASSWORD variables in the environment. By default MySQL uses port 33060 for the X protocol.

## Examples

Simple table example:

```python
from mysqlx_connector import Table, parse_results

class CityTable(Table):

	def get_cities(self):
		return parse_results(self._table.select().execute())
```

Usage of the created table:

```python
city_table = CityTable('cities', 'exampleDatabase')

with city_table as table:
	for row in table.get_cities():
		print(row)
```
