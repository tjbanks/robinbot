import logging
import numpy as np

from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Dense 

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.utils.class_weight import compute_class_weight,compute_sample_weight

from tqdm.auto import tqdm



class LSTMNet():

    def __init__(self):
        self.logger = logging.getLogger('robinbot.ml.LSTMNet')
        return
    
    def load_config(self):
        return

    def save_config(self):
        return
    
    def predict(self,value):
        return

    def train(self, data, lookback=120, lookback_skip=1, every_other_hold=30,epochs=20,batch_size=50):
        """
        :param data: DataRepository
        :param lookback: int
        """
        sc = MinMaxScaler(feature_range=(0,1))
        data_x = data.x
        data_y = data.y

        X_scaled = sc.fit_transform(data_x)

        X_train = []
        y_train = []#data.y[lookback:]
        indicies = []
        
        self.logger.info('preparing dataset for LSTM training')
        pbar = tqdm(total=len(X_scaled))

        for i in range(lookback, len(X_scaled)):
            if data_y.iloc[i].labels == 0 or data_y.iloc[i].labels == 1 or i % every_other_hold == 0:
                X_train.append(X_scaled[i-lookback:i:lookback_skip, 0])
                y_train.append(data_y.iloc[i])
                indicies.append(i)
            pbar.update(1)

        pbar.close()
        self.logger.info('preparation complete')

        #Check out how the labeling falls by uncommenting here:
        #data.plot_labels(label_indicies=indicies)
        #import pdb;pdb.set_trace()

        onehot_encoder = OneHotEncoder(sparse=False)
        y_train_encoded = onehot_encoder.fit_transform(y_train)

        X_train, y_train = np.array(X_train), np.array(y_train_encoded)

        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

        x_train, x_test, y_train, y_test = train_test_split(X_train, y_train,shuffle=False)

        

        #y_rebal = np.array([1/i for i in data.y[60:].value_counts()])
        #y_rebalance = np.repeat([y_rebal], repeats=len(y_train_encoded),axis=0)
        y_rebalance = compute_sample_weight('balanced', y_train)

        model = Sequential()

        model.add(LSTM(units=100,return_sequences=True,input_shape=(X_train.shape[1], 1)))
        #model.add(Dropout(0.2))

        model.add(LSTM(units=100,return_sequences=True))
        #model.add(Dropout(0.2))

        model.add(LSTM(units=100,return_sequences=True))
        #model.add(Dropout(0.2))

        model.add(LSTM(units=50))
        #model.add(Dropout(0.2))

        model.add(Dense(units=3, activation='softmax', name='output'))

        model.compile(optimizer='adam',
                loss='categorical_crossentropy',#'mean_squared_error', 
                metrics=['accuracy'],
                )#sample_weight_mode="temporal")
       
        model.fit(x_train,y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(x_test, y_test),
                sample_weight=y_rebalance)
    

        score = model.evaluate(x_train, y_train)
        score_test = model.evaluate(x_test, y_test)
        
        self.logger.info(f'Train loss: {score[0]} / Train accuracy: {score[1]}')
        self.logger.info(f'Test loss: {score_test[0]} / Test accuracy: {score_test[1]}')

        
        import pdb;pdb.set_trace()

        # NEED TO IMPLEMENT KFOLD
        # https://machinelearningmastery.com/multi-class-classification-tutorial-keras-deep-learning-library/
        return