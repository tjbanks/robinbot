import click
import logging
import os

from clint.textui import puts, colored, indent

from . import run as run_commands
from . import util as util_commands
from . import data as data_commands

@click.group()
@click.option('-u','--username', default=None, help='the provided username to login to trading service')
@click.option('-v','--disable-debug', is_flag=True, default=True, help='disable verbose debug output on-screen')
@click.option('-l','--log-file-location', type=click.STRING, default="./robinbot_log.txt", help='modify the log output location [default: robinbot_log.txt')
@click.option('-d','--disable-log-file', is_flag=True, default=False, help='disable the output log file')
@click.pass_context
def cli(ctx, username, disable_debug, log_file_location, disable_log_file):  

    log_format = '%(asctime)s:%(msecs)d %(name)s %(levelname)s \"%(message)s\"'
    screen_log_format = '%(asctime)s %(name)s %(levelname)s :: %(message)s'

    if not disable_log_file:
        logging.basicConfig(filename=log_file_location,
                            filemode='a',
                            format=log_format,
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.DEBUG)

        console = logging.StreamHandler()
        if disable_debug:
            console.setLevel(logging.INFO)
        else:
            console.setLevel(logging.DEBUG)
        formatter = logging.Formatter(screen_log_format)
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger().addHandler(console)

        logger = logging.getLogger('robinbot')
        logger.info("Robinbot started")
        logger.info("Writing logs to " + log_file_location)
        

    ctx_obj = {}
    ctx_obj['username'] = username
    ctx.obj = ctx_obj


cli.add_command(run_commands.cli)
cli.add_command(util_commands.cli)
cli.add_command(data_commands.data)

if __name__ == "__main__":
    cli()