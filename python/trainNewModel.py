import numpy as np 
import pandas as pd 
import os

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import model_from_json

from sklearn.preprocessing import MinMaxScaler
min_max_scaler = MinMaxScaler()

file = os.path.dirname(os.path.realpath(__file__)) + '\\BTCPriceAppend.csv'
fileJS = os.path.dirname(os.path.realpath(__file__)) + '\\model.json'
fileH5 = os.path.dirname(os.path.realpath(__file__)) + '\\model.h5'

df = pd.read_csv(file)
df.drop(['Date','High','Low','Close**','Volume','Market Cap'], 1, inplace=True)

prediction_days = 7
data = df.values

training_set = min_max_scaler.fit_transform(data)
x_train = training_set[0:len(training_set)-7]
y_train = training_set[7:len(training_set)]
x_train = np.reshape(x_train, (len(x_train), 1, 1))

num_units = 5
activation_function = 'sigmoid'
optimizer = 'adam'
loss_function = 'mean_squared_error'
batch_size = 5
num_epochs = 50

# Initialize the RNN
regressor = Sequential()
# Adding the input layer and the LSTM layer
regressor.add(LSTM(units = num_units, activation = activation_function, input_shape=(None, 1)))
# Adding the output layer
regressor.add(Dense(units = 1))
# Compiling the RNN
regressor.compile(optimizer = optimizer, loss = loss_function)
# Using the training set to train the model
regressor.fit(x_train, y_train, batch_size = batch_size, epochs = num_epochs)
 
# serialize model to JSON
model_json = regressor.to_json()
with open(fileJS, "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
regressor.save_weights(fileH5)
print("Finish")
sys.stdout.flush()
