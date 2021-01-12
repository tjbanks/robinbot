import click
import logging
import os,sys

from robinbot.data import DataRepository
from robinbot.ml import LSTMNet

@click.group('data', help='Data related functions')
@click.option('-c', '--csv', type=click.STRING, default="", help="read a csv for input data training")
@click.option('-s', '--sqlite', type=click.STRING, default="", help="sqlite file to pull data from")
@click.option('-t', '--sql-table', type=click.STRING, default="", help="sql table to select the data from")
@click.option('-x', '--x-columns', type=click.STRING, default="ask_price,bid_price,mark_price,high_price,low_price", help="comma separated input columns [eg:col1,col2,etc.]")
@click.option('-y', '--y-columns', type=click.STRING, default="labels", help="comma separated output columns")
@click.option('-d', '--timestamp-column', type=click.STRING, default="timestamp", help="timestamp column")
@click.option('-f', '--timestamp-format', type=click.STRING, default="%Y-%m-%d %H:%M:%S", help="%Y-%m-%d %H:%M:%S")
@click.pass_context
def data(ctx,csv,sqlite,sql_table,x_columns,y_columns,timestamp_column, \
                timestamp_format):
    logger = ctx.obj['logger'] = logging.getLogger('robinbot.cli.data')

    data = DataRepository()
    x = x_columns.split(',')
    y = y_columns.split(',')

    if len(csv):
        logger.info("Reading csv file \"" + csv +"\"")
        
        data.load_csv(csv,x,y,timestamp_column=timestamp_column, \
                        timestamp_format=timestamp_format)
    elif len(sqlite):
        logger.warning("SQLite data source not implemented. Quitting.")
        sys.exit(1)
    else:
        logger.error("No input data specified. Quitting.")
        sys.exit(1)

    ctx.obj['data'] = data

    pass

@data.group('label', help="label provided data")
@click.option('-o', '--output-file',  default=None, help='specify an alternate output location [default: overwrite current file]')
@click.pass_context
def label(ctx,output_file):
    logger = ctx.obj['logger'] = logging.getLogger('robinbot.cli.data.label')

    data = ctx.obj['data']
    ctx.obj['label-output-file'] = output_file

@label.command('default', help="")
@click.option('-c', '--column-name', type=click.STRING, default="mark_price", help="column to generate labels with [default: mark_price]")
@click.option('-r', '--rolling-mean', type=click.STRING, default=10, help="window size for the rolling mean [default: 10]")
@click.option('-w', '--window-size', type=click.STRING, default=70, help="window size for determining labels [default: 70]")
@click.pass_context
def label_default(ctx,column_name,rolling_mean,window_size):
    logger = ctx.obj['logger'] = logging.getLogger('robinbot.cli.data.label.default')
    logger.info('default labeling mechanism selected')

    data = ctx.obj['data']
    output_file = ctx.obj['label-output-file']

    new_col_name = column_name + '_avg'
    data.apply_rolling_mean(int(rolling_mean),col_name=column_name, new_col_name=new_col_name)
    data.generate_labels(new_col_name,window_size=int(window_size))

    data.to_csv(output_file)
    
    logger.info('label creation complete')


@data.group('train', help="train an AI model on provided data")
@click.option('-b','--batch-size', type=click.INT, default=50, help="batch size of training if applicable [default: 50]")
@click.option('-e','--epochs', type=click.INT, default=20, help="number of epochs for training if applicable [default: 20]")
@click.pass_context
def train(ctx, batch_size, epochs):
    logger = ctx.obj['logger'] = logging.getLogger('robinbot.cli.data.train')
    logger.info("Model training utility started")

    ctx.obj['batch_size'] = batch_size
    ctx.obj['epochs'] = epochs


@train.command('lstm', help="train an LSTM model on provided data")
@click.option('-o', '--output-prefix', type=click.STRING, default="", help="output model filename prefix")
@click.option('-l','--lookback', type=click.INT, default=120, help="how far back should the lstm be trained to look back on [default: 120]")
@click.option('-s','--lookback-skip', type=click.INT, default=1, help="skip values for lookback to reduce the amount of input data [default: 1]")
@click.option('-h', '--every-other-hold', type=click.INT, default=30, help="only train using every other n \"hold\" values [default: 30]")
@click.pass_context
def lstm(ctx,output_prefix, lookback, lookback_skip, every_other_hold):
    logger = ctx.obj['logger'] = logging.getLogger('robinbot.cli.util.data.train.lstm')
    logger.info('LSTM selected')

    data = ctx.obj['data']
    batch_size = ctx.obj['batch_size']
    epochs = ctx.obj['epochs']

    lstm = LSTMNet()
    
    lstm.train(data,lookback=lookback, lookback_skip=lookback_skip, every_other_hold=every_other_hold,
                epochs=epochs, batch_size=batch_size)

