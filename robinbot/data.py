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

        
        # Make sure that the columns we're trying to load will be available
        df = pd.read_csv(csv_path)

        for col in x_columns + y_columns + [timestamp_column]:
            if col not in list(df.columns):
                self.logger.warning("'"+col+"' column not found in dataset. Continuing but this may cause problems later")        

        #df = pd.read_csv(csv_path,usecols=x_columns+y_columns+[timestamp_column])

        df['timestamp'] = pd.to_datetime(df[timestamp_column],format=timestamp_format)
        if timestamp_column != 'timestamp':
            df.drop([timestamp_column],axis=1,inplace=True)

        df.sort_values('timestamp', inplace=True)
        df.reset_index(drop=True, inplace=True)

        prev_len = len(df)
        df.dropna(inplace=True)
        df.reset_index(drop=True, inplace=True)
        self.logger.info("Dropped {0} nan rows".format(prev_len - len(df)))

        self.data = df
        return

    def to_csv(self,location=None):
        loc = self._src_path

        if location:
            loc = location

        self.data.to_csv(loc,index=False)

        self.logger.info('data file written to ' + loc)


    def load_sqlite(self,sqlite_path,x_columns,y_columns,datetime_column, \
                    timestamp_format="%Y-%m-%d %H:%M:%S"):
        
        self._src_path = sqlite_path
        raise Exception("Not implemented")

    def apply_rolling_mean(self, rolling_mean_window_size, col_name='mark_price', new_col_name='mark_price_avg'):

        self.data[new_col_name] = self.data[col_name].rolling(window=rolling_mean_window_size).mean()


    def generate_labels(self, col_name, window_size=11,inplace=True):
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

    def plot_labels(self,col_name='mark_price',labels_col='labels'):
        
        zero = self.data[self.data[labels_col]==0]
        one = self.data[self.data[labels_col]==1]

        plt.scatter(zero.timestamp,zero.mark_price,color='red')
        plt.scatter(one.timestamp,one.mark_price,color='green')

        plt.plot(self.data.timestamp,self.data[col_name])
        plt.show()
        

    def simulate_return(self,col_name='mark_price',num_coins=100000,buy_price_col='ask_price',sell_price_col='bid_price',label='labels'):

        self.logger.info("simulating return")
        row_counter = 0
        total_rows = len(self.data)
        pbar = tqdm(total=total_rows)

        cash_held = 0
        coin_count = 10000

        price = self.data.iloc[0][col_name]
        start_worth = cash_held + (coin_count*price)

        self.logger.info("starting worth:" + str(start_worth))

        while row_counter < total_rows:
            
            price = self.data.iloc[row_counter][col_name]
            buy_price = self.data.iloc[row_counter][buy_price_col]
            sell_price = self.data.iloc[row_counter][sell_price_col]

            action = self.data.iloc[row_counter][label]

            
            old_worth = cash_held + (coin_count*price)

            if action == 0: #Sell
                if coin_count > 0:
                    
                    cash_held = (coin_count*sell_price)
                    #self.logger.info("Selling coins:[" + str(coin_count) + "] for [" + str(cash_held) + "]")

                    coin_count = 0
                
            elif action == 1: #Buy
                if cash_held > 0:
                    coin_count = (cash_held/buy_price)
                    #self.logger.info("Buying coins:[" + str(coin_count) + "] for [" + str(cash_held) + "]")

                    cash_held = 0
            elif old_worth == 0:
                break
            else:
                pass


            current_worth = cash_held + (coin_count*price)

            #if current_worth != old_worth:
                #self.logger.info("current worth:" + str(current_worth))

            row_counter = row_counter + 1
            pbar.update(1)

        pbar.close()
        end_worth = cash_held + (coin_count*price)
        self.logger.info("ending worth:" + str(end_worth))

        hold_wait_strat = self.data.iloc[-1].mark_price / self.data.iloc[0].mark_price 
        hold_wait_strat_val = hold_wait_strat * start_worth
        self.logger.info("ending worth if held and waited:" + str(hold_wait_strat_val))
        improvement = end_worth/start_worth - hold_wait_strat
        self.logger.info("improvement: " + str(improvement))

        return improvement

    def find_best_return(self):
        best_roll = 0
        best_window = 0
        best_improvement = 0

        for roll in range(10,90,10):
            for window in range(10,90,10):
                self.logger.info('testing rolling mean val: ' + str(roll))
                self.logger.info('testing label window: ' + str(window))
                self.data['mark_price_avg'] = self.data.mark_price.rolling(window=roll).mean()
                self.generate_labels('mark_price_avg',window_size=window)
                improvement = self.simulate_return()
                
                if improvement > best_improvement:
                    best_improvement = improvement
                    best_roll = roll
                    best_window = window
                    
                self.logger.info('current best improvement: ' + str(best_improvement))
                self.logger.info('current best roll: ' + str(best_roll))
                self.logger.info('current best window: ' + str(best_window))