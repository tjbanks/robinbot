import numpy as np

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Dense 

from sklearn.preprocessing import MinMaxScaler, OneHotEncoder



class LSTMNet():

    def __init__(self):
        return
    
    def load_config(self):
        return

    def save_config(self):
        return
    
    def predict(self,value):
        return

    def train(self, data, lookback=60):
        """
        :param data: DataRepository
        :param lookback: int
        """

        sc = MinMaxScaler(feature_range=(0,1))

        X_scaled = sc.fit_transform(data.x)

        X_train = []
        y_train = data.y[60:]
        for i in range(lookback, len(X_scaled)):
            X_train.append(X_scaled[i-lookback:i, 0])

        
        onehot_encoder = OneHotEncoder(sparse=False)
        y_train_encoded = onehot_encoder.fit_transform(y_train)

        X_train, y_train = np.array(X_train), np.array(y_train_encoded)

        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

        y_rebal = np.array([1/i for i in data.y[60:].value_counts()])
        y_rebalance = np.repeat([y_rebal], repeats=len(y_train_encoded),axis=0)

        model = Sequential()

        model.add(LSTM(units=50,return_sequences=True,input_shape=(X_train.shape[1], 1)))
        model.add(Dropout(0.2))

        model.add(LSTM(units=50,return_sequences=True))
        model.add(Dropout(0.2))

        model.add(LSTM(units=50,return_sequences=True))
        model.add(Dropout(0.2))

        model.add(LSTM(units=50))
        model.add(Dropout(0.2))

        model.add(Dense(units=3))

        model.compile(optimizer='adam',loss='mean_squared_error', sample_weight_mode="temporal")

        import pdb;pdb.set_trace()
        
        model.fit(X_train,y_train,epochs=10,batch_size=32,class_weight=y_rebalance)
        
        
        


        return