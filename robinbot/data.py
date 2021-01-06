import pandas as pd

class DataRepository():

    def __init__(self):
        self._src_path = None
        self.data = None
        self.x_columns = None
        self.y_columns = None
        self.datetime_column = None
        return

    def load_csv(self,csv_path,x_columns,y_columns,datetime_column="", \
                    datetime_format="%Y-%m-%d %H:%M:%S"):

        self._src_path = csv_path

        self.data = pd.read_csv(csv_path,usecols=x_columns+y_columns))
        self.x_columns = x_columns
        self.y_columns = y_columns
        self.datetime_column = datetime_column
        self.datetime_format = datetime_format

        return

    def load_sqlite(self,sqlite_path,x_columns,y_columns,datetime_column, \
                    datetime_format="%Y-%m-%d %H:%M:%S"):
        
        self._src_path = sqlite_path
        raise Exception("Not implemented")

