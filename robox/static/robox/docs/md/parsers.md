### Adding a parser:
To add a parser, simply place the parser.py file into the parsers/parsers directory and restart the server.

### Creating a parser
A parser file should looks something like this:

	from parsing import make_and_add_parser
	
	def accept(f):
		# Return True if the passed in file can be parsed, False otherwise.

	def parse(f):
		# Yield a dictionary corresponding to each entry in the file.
		# e.g:
		for line in f:
			cells = line.decode('ascii').replace("\n", "").split(",")
			# ...
			yield {"name": name, "address": slot, "value": concentration, "units": units}

	make_and_add_parser("parser_description", parse, accept)

The `"parser_description"` string should be a unique code for identifying which parser the file was parsed with.

The `f` parameter is a binary file, so will need to be decoded before use.