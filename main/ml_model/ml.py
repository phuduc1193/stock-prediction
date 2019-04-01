import os
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.models import model_from_json

from sklearn.externals import joblib
from sklearn.preprocessing import MinMaxScaler

from django.conf import settings
from main.data_storage.data_center import DataCenter


def train(symbol):
    model_name = 'model.{}.json'.format(symbol)
    scaler_name = 'scaler.{}.sav'.format(symbol)
    
    dc = DataCenter(symbol=symbol)
    df = dc.get_intraday(outputsize='full')
    training_set = df.iloc[:, 0:1].copy()

    sc = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = sc.fit_transform(training_set)
    
    X_train = []
    y_train = []
    for i in range(60, training_set_scaled.shape[0]):
        X_train.append(training_set_scaled[i-60:i, 0])
        y_train.append(training_set_scaled[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    regressor = create_model((X_train.shape[1], 1))
    regressor.compile(optimizer='adam', loss='mean_squared_error')
    regressor.fit(X_train, y_train, epochs=100, batch_size=32)

    directory = settings.MODEL_ROOT
    if not os.path.exists(directory):
        os.makedirs(directory)

    model_path = os.path.join(directory, model_name)
    with open(model_path, 'w') as file:
        file.write(regressor.to_json())

    scaler_path = os.path.join(directory, scaler_name)
    with open(scaler_path, 'wb') as file:
        joblib.dump(sc, file)

    return (model_name, scaler_name)

def create_model(input_shape):
    model = Sequential()

    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50))
    model.add(Dropout(0.2))

    model.add(Dense(units=1))
    return model

def predict(symbol, scaler_name, model_name):
    dc = DataCenter(symbol=symbol)
    df = dc.get_intraday()
    inputs = df.tail(60).iloc[:, 0:1].copy()

    directory = settings.MODEL_ROOT
    model_name = os.path.join(directory, model_name)
    scaler_name = os.path.join(directory, scaler_name)

    json_file = open(model_name, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    regressor = model_from_json(loaded_model_json)

    sc = joblib.load(scaler_name)

    inputs = sc.transform(inputs)
    inputs = np.array(inputs)
    inputs = np.reshape(inputs, (inputs.shape[1], inputs.shape[0], 1))

    predicted_stock_price = regressor.predict(inputs)
    return sc.inverse_transform(predicted_stock_price)