# take csv of list of stocks get daily information if not argument
# 'SYMBOL1' 'SYMBOL2'
# else try to get history back to parameter
import re
import requests
import sys
import os
from multiprocessing import Process

# https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console #
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# extract sock symbols from list of stocks
def parse_stock_list(stocks):
	stocks = re.findall(r'\'([A-Z]+)\'', stocks)
	return stocks

# get contents of file as string
def read_stock_file(filename):
	with open(filename, 'r') as f:
		data = f.read()
	return data;

# specific query to retrieve information about a list of stocks prices for 1 year
# stores the stocks in the folder stock_data (which MUST already exist)
def make_request(stocks):
	api_command = ('https://api.iextrading.com/1.0/stock/', '/chart/1y')
	#from multiprocessing import Pool
	for symbol in stocks:
		with open('stock_data/' + symbol + '.txt', 'w') as f:
			query = api_command[0] + symbol + api_command[1]
			print('requesting: ' + query)
			res = requests.get(query)
			f.write(res.text)


# reads from the file stocks.txt to see which symbols data should be gathered for
if __name__ ==  '__main__':
	print('reading from stocks.txt')
	contents = read_stock_file('stocks.txt')
	stock_list = parse_stock_list(contents)
	# get 5yr stock price history

	PROCESSES = 8
	print('processes set at ' + str(PROCESSES))
	max_index = len(stock_list) - 1
	step = int(max_index / (PROCESSES - 1))
	parceled_stocks = []
	for x in range(0, max_index, step):
		start_index = x
		end_index = max_index if (x + step > max_index) else x + step;
		parceled_stocks.append(stock_list[start_index:end_index])

	process_l = []
	for x in range(0, PROCESSES):
		process_l.append(Process(target=make_request, args=(parceled_stocks[x],)))
		process_l[x].start()

	for x in range(0, PROCESSES):
		process_l[x].join()

	print('Finished getting stock data')

