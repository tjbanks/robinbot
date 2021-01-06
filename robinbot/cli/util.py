import click
import logging
import os,sys

from robinbot.data import DataRepository

@click.group('util')
@click.pass_context
def cli(ctx):
    ctx.obj['logger'] = logging.getLogger('robinbot.cli.util')
    pass

@cli.command('generate-config', help="Generates a config file for the program to use")
@click.option('--location', type=click.STRING, default=None, help="override the default write location (current directory)")
@click.pass_context
def generate_config(ctx,location):
    logger = ctx.obj['logger']
    logger.info("Function not yet implemented.")


@click.group('ai', help='AI related functions')
@click.pass_context
def ai(ctx):
    logger = ctx.obj['logger'] = logging.getLogger('robinbot.cli.util.ai')
    pass

cli.add_command(ai)


@ai.group('train', help="train an AI model on provided data")
@click.option('--csv', type=click.STRING, default="", help="read a csv for input data training")
@click.option('--sqlite', type=click.STRING, default="", help="input columns")
@click.option('-t', '--sql-table', type=click.STRING, default="", help="sql table to select the data from")
@click.option('-x', '--x-columns', type=click.STRING, default="", help="comma separated input columns [eg:col1,col2,etc.]")
@click.option('-y', '--y-columns', type=click.STRING, default="", help="comma separated output columns")
@click.option('-d', '--timestamp-column', type=click.STRING, default="timestamp", help="timestamp column")
@click.option('-f', '--timestamp-format', type=click.STRING, default="%Y-%m-%d %H:%M:%S", help="%Y-%m-%d %H:%M:%S")
@click.pass_context
def train(ctx,csv,sqlite,sql_table,x_columns,y_columns,timestamp_column, \
                timestamp_format):
    logger = ctx.obj['logger'] = logging.getLogger('robinbot.cli.util.ai.train')
    logger.info("Training model")

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

@train.command('lstm', help="train an LSTM model on provided data")
@click.option('-o', '--output-prefix', type=click.STRING, default="", help="output model filename prefix")
@click.pass_context
def lstm(ctx,output_prefix):
    logger = ctx.obj['logger'] = logging.getLogger('robinbot.cli.util.ai.train.lstm')
    logger.info('LSTM selected')

    data = ctx.obj['data']
    import pdb;pdb.set_trace()
