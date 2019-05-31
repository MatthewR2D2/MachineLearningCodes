'''
LSTM for Predict open stock price
'''
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import math
from sklearn.metrics import mean_squared_error

# Data preprocessing
training_set_path = "data/Google_Stock_Price_Train.csv "
test_set_path = "data/Google_Stock_Price_Test.csv "

dataset_train = pd.read_csv(training_set_path)
# Get first and last values using 1:2 i.e open and close data prices
training_set = dataset_train.iloc[:, 1:2].values

# Feature scaling Standardization or Normalization
# Apply normalization
sc = MinMaxScaler(feature_range=(0, 1))
# Scale the data set and normalize it between 0 and 1
training_set_scaled = sc.fit_transform(training_set)

# Create a data structure with 60 timesteps and 2 outputs
# Needed for RNN structure
x_train = []
y_train = []

for i in range(60, 1258):
    # Gives 0 to 60 stock prices
    x_train.append(training_set_scaled[i - 60:i, 0])
    y_train.append(training_set_scaled[i, 0])

# get them into numpy array into the right form
x_train, y_train = np.array(x_train), np.array(y_train)

# Reshaping the data
# this to keras input shape (batch_size, timesteps, input dim (# Of indicators)
x_train = np.reshape(x_train, (x_train.shape[0],
                               x_train.shape[1],
                               1))

# Build RNN
# Initialize the RNN
regressor = Sequential()

# Add layers to regressor model (Stacked LSTM model)
# First lstm layer
regressor.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
regressor.add(Dropout(0.2))
# Layer 2
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))
# Layer 3
regressor.add(LSTM(units=50, return_sequences=True))
regressor.add(Dropout(0.2))
# Layer 4 Last stacked layers
regressor.add(LSTM(units=50, return_sequences=False))
regressor.add(Dropout(0.2))

# Add output layer
regressor.add(Dense(units=1))
# Compile the RNN
regressor.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error', 'cosine_proximity'])
# Train the RNN
history = regressor.fit(x_train, y_train,
              batch_size= 32,
              epochs= 100)

# Make prediction and visualize
# Get real stock price of 2017
dataset_test = pd.read_csv(test_set_path)
real_stock_price = dataset_test.iloc[:, 1:2].values

# Concat the open prices to the training set and open set
dataset_total = pd.concat((dataset_train['Open'], dataset_test['Open']), axis = 0)
# Get the last 60 days of each stock prices
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range(60, 80):
    X_test.append(inputs[i-60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Predict with regressor
predicted_stock_price = regressor.predict(X_test)
# Inverse the scale of the predicted values get back prices from sc values
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

# Vizsulaize the result
plt.plot(real_stock_price, color = 'red', label = 'Real Google Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()

#Futher evaluation
rmse = math.sqrt(mean_squared_error(real_stock_price, predicted_stock_price))
print("RMSE:", rmse)

print(history.history.keys())
plt.plot(history.history['mean_squared_error'])
plt.plot(history.history['mean_absolute_error'])
plt.plot(history.history['mean_absolute_percentage_error'])
plt.plot(history.history['cosine_proximity'])
plt.show()