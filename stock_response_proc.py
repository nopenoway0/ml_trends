import re
from pandas import DataFrame
from os import listdir
filename = "jill_stock_data.txt"
directory = 'stock_data'
entry_reg, field_reg, value_reg = r'.*?\{(.*?)\}', r'.*?\"([a-zA-Z]+)\"\:', r'.*?\"([a-zA-Z]+)\"\:\"*([a-zA-Z0-9\- \.]+)\"*'

# converts the retrieved format from iextrading's, when saved as a text file,
# into a dataframe to be used by pandas
def get_dataframe(filename):
	df = None
	with open(filename, 'r') as f:
		contents = f.read()
		entries = re.findall(entry_reg, contents)
		if len(entries) == 0:
			raise Exception("No entries found in file")
		fields = re.findall(field_reg, entries[0])
		columns = {}
		for field in fields:
			columns[field] = []
		for entry in entries:
			values = re.findall(value_reg, entry)
			fields_c = fields.copy()
			for value in values:
				fields_c.remove(value[0])
				columns[value[0]].append(value[1])
			for field in fields_c:
				columns[field].append('NaN')
		df = DataFrame(data=columns)
	return df

# a directory of responses from iextrading and converts them into a dictionary of pandas dataframes
# where the key is the symbol name
def get_dataframes(directory):
	stock_dfs = {}
	# load all stock text files
	stock_files = listdir(directory)
	filename_reg = r'(.*?)\..*'
	for file in stock_files:
		name = re.match(filename_reg, file)[1]
		try:
			f_df = get_dataframe(directory + '/' + file)
			stock_dfs[name] = f_df
		except Exception as e:
			print('error {0} in {1}'.format(str(e), file))
	return stock_dfs