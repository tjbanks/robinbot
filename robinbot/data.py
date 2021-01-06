import logging

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

import matplotlib.pyplot as plt

class DataRepository():

    def __init__(self):
        self._src_path = None
        self.data = None
        self.x_columns = None
        self.y_columns = None
        self.timestamp_column = None

        self.logger = logging.getLogger('robinbot.data.DataRepository')
        return

    def load_csv(self,csv_path,x_columns,y_columns,timestamp_column="", \
                    timestamp_format="%Y-%m-%d %H:%M:%S"):

        self._src_path = csv_path
        self.x_columns = x_columns
        self.y_columns = y_columns
        self.timestamp_column = timestamp_column
        self.timestamp_format = timestamp_format

        df = pd.read_csv(csv_path,usecols=x_columns+y_columns+[timestamp_column])
        df['timestamp'] = pd.to_datetime(df[timestamp_column],format=timestamp_format)
        if timestamp_column != 'timestamp':
            df.drop([timestamp_column],axis=1,inplace=True)

        df.sort_values('timestamp', inplace=True)
        df.reset_index(drop=True, inplace=True)

        prev_len = len(df)
        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)
        self.logger.info("Dropped {0} nan rows before label calculation".format(prev_len - len(df)))

        self.data = df
        return

    def load_sqlite(self,sqlite_path,x_columns,y_columns,datetime_column, \
                    timestamp_format="%Y-%m-%d %H:%M:%S"):
        
        self._src_path = sqlite_path
        raise Exception("Not implemented")


    def generate_labels(self, col_name, ask, bid, window_size=11,inplace=True):
        """
        Data is labeled as per the logic in research paper
        Algorithmic Financial Trading with Deep Convolutional Neural Networks: Time Series to Image Conversion Approach
        Label code : BUY => 1, SELL => 0, HOLD => 2
        params :
            df => Dataframe with data
            col_name => name of column which should be used to determine strategy
        returns : numpy array with integer codes for labels with
                  size = total-(window_size)+1
        """

        self.logger.info("creating label with x strategy")
        row_counter = 0
        total_rows = len(self.data)
        labels = np.zeros(total_rows)
        labels[:] = np.nan
        self.logger.info("Calculating labels")
        pbar = tqdm(total=total_rows)
        
        while row_counter < total_rows:
            if row_counter >= window_size - 1:
                window_begin = row_counter - (window_size - 1)
                window_end = row_counter
                window_middle = (int)((window_begin + window_end) / 2)

                min_ = np.inf
                min_index = -1
                max_ = -np.inf
                max_index = -1
                for i in range(window_begin, window_end + 1):
                    price = self.data.iloc[i][col_name]
                    if price < min_:
                        min_ = price
                        min_index = i
                    if price > max_:
                        max_ = price
                        max_index = i

                if max_index == window_middle :
                    labels[window_middle] = 0
                elif min_index == window_middle:
                    labels[window_middle] = 1
                else:
                    labels[window_middle] = 2

            row_counter = row_counter + 1
            pbar.update(1)

        pbar.close()
        if inplace:
            self.data['labels'] = labels
            return self.data
        return labels

    def plot_labels(self):
        
        zero = self.data[self.data['labels']==0]
        one = self.data[self.data['labels']==1]

        plt.scatter(zero.timestamp,zero.mark_price,color='red')
        plt.scatter(one.timestamp,one.mark_price,color='green')

        plt.plot(self.data.timestamp,self.data.mark_price)
        plt.show()
        