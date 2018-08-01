import numpy as np
from pandas import read_csv, to_datetime, merge
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge
import get_optimal_set as gos
from stock_response_proc import get_dataframes, get_dataframe

# load dataframes from kaggle datasets
# bitcoin_dataframe = read_csv('data/btc_history.csv')
stockmarket_dataframe = read_csv('data/all_stocks_5yr.csv')
jill_dataframe = read_csv('data/JILL.csv')

# load all dataframes from STOCK txt files in stock_data folder
test_dataframes = get_dataframes('stock_data')

# combine test dataframes to create X test set of stocks opening values this month
combined_frames = None
for key, value in test_dataframes.items():
	value = value.iloc[:, 0:2]
	if combined_frames is None:
		combined_frames = value
	else:
		tmp = merge(combined_frames, value, on='date', how='inner')
		if len(tmp['date']) < 50:
			print('not sufficient merged date for {0}'.format(key))
		else:
			combined_frames = tmp

# isolate date and opening price of JILL stock price
test_jill_dataframe = get_dataframe('JILL.txt')
jill_test_values = test_jill_dataframe.iloc[:, 0:2]

# merge into test data frame
test_dataframe = merge(combined_frames, jill_test_values, on='date', how='inner')
print(test_dataframe)

'''
# create feature set (Each type of stock their prices and date)
# get how many seperate datasets in this case how many unique type of stocks
stock_datsets = stockmarket_dataframe.Name.unique()

# each stored array perform a year cutoff to match that of the first
# and last entry of the shorter set on each end
stockmarket_dataframe = stockmarket_dataframe[(stockmarket_dataframe['date'] > '2015-3-2')]

X = stockmarket_dataframe.query('Name == \'' + stock_datsets[0] + '\'').iloc[:, [0, 1]]
for x in range(1, len(stock_datsets)):
	results = stockmarket_dataframe.query('Name == \'' + stock_datsets[x] + '\'').iloc[:, [0, 1]]
	if(len(results) > 200):
		X = merge(X, results, on='date', how='inner')

#X = merge(X, bitcoin_dataframe.iloc[:, [0, 1]], left_on='date', right_on='Date', how='inner')
X = merge(X, jill_dataframe.iloc[:, [0, 1]], left_on='date', right_on='Date', how='inner')

# remove large dataframe from memory - not needed anymore
del stockmarket_dataframe;

# create dependent set (bitcoin prices)
y = X.iloc[:, -1:]

# isolate independent set
X = X.iloc[:, 0:-3]


# create test and train sets
from sklearn.model_selection import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)
# in this case use whole set, and will create the test set later
X_train = X
y_train = y

# create SVR regression object
from sklearn.svm import SVR
lr =  SVR()

# create Standard scaler for x and y and fit to training set
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc_y = StandardScaler()
sc.fit(X_train.iloc[:, 1:])
sc_y.fit(y_train)

# fit scaled parameters of train set to model
lr.fit(sc.transform(X_train.iloc[:, 1:]), sc_y.transform(y_train))

# plot real values
#plt.plot(X.iloc[:, 0], y)
# plot values using model
#plt.plot(X.iloc[:, 0], sc_y.inverse_transform(lr.predict(sc.transform(X.iloc[:, 1:]))))

# plot real test values
plt.plot(X.iloc[:, 0], y)
plt.plot(X.iloc[:, 0], sc_y.inverse_transform(lr.predict(sc.transform(X.iloc[:, 1:]))))

# disable bottom ticker, too many days on axis, annoying
#plt.tick_params()
plt.show()
'''