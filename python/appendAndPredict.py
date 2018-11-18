import sys
import os
from time import gmtime, strftime
import numpy as np 
import pandas as pd 
from keras.models import Sequential
from keras.models import model_from_json
from sklearn.preprocessing import MinMaxScaler
min_max_scaler = MinMaxScaler()

file = os.path.dirname(os.path.realpath(__file__)) + '\\BTCPriceAppend.csv'
fileResult = os.path.dirname(os.path.realpath(__file__)) + '\\predict.json'

def appendData(df, price):
	now = strftime("%d-%m-%Y", gmtime())
	if df.loc[len(df)-1].Date == now:
		df.at[len(df)-1,'Price'] = sys.argv[1]
	else:
		df = df.append({
			'Date': now,
			'Price': price,
			'High': 'None',
			'Low': 'None',
			'Close**': 'None',
			'Volume': 'None',
			'Market Cap': 'None'}, ignore_index=True)

	df.to_csv(file, index=False, encoding='utf8')

def predict(df):
	df.drop(['Date','High','Low','Close**','Volume','Market Cap'], 1, inplace=True)
	prediction_days = 30
	df_train= df[:len(df)-prediction_days]
	training_set = df_train.values
	training_set = min_max_scaler.fit_transform(training_set)
	x_train = training_set[0:len(training_set)-7]
	y_train = training_set[7:len(training_set)]
	x_train = np.reshape(x_train, (len(x_train), 1, 1))


	df_test= df[len(df)-prediction_days:]
	test_set= df_test.values
	realData = np.reshape(test_set[len(test_set)-7:], 7)
	inputs = np.reshape(test_set, (len(test_set), 1))
	inputs = min_max_scaler.transform(inputs)
	inputs = np.reshape(inputs, (len(inputs), 1, 1))

	# load json and create model
	json_file = open(os.path.dirname(os.path.realpath(__file__)) + '\\model.json', 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	# load weights into new model
	loaded_model.load_weights(os.path.dirname(os.path.realpath(__file__)) + '\\model.h5')

	predicted_price = loaded_model.predict(inputs)
	predicted_price = min_max_scaler.inverse_transform(predicted_price)

	savePredict(predicted_price, realData)

def savePredict(predict, realData):
	predict = np.reshape(predict, (len(predict)))
	predictString = ','.join(str(e) for e in predict[len(predict)-7:])
	realDataString = ','.join(str(e) for e in realData)
	
	with open(fileResult, "w") as json_file:
	    json_file.write(predictString+'\n'+realDataString)

df = pd.read_csv(file)
if len(sys.argv) >= 2:
	appendData(df, sys.argv[1]);

predict(df)

sys.stdout.flush()