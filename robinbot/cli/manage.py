import click
import logging
import os

from clint.textui import puts, colored, indent

from . import run as run_commands
from . import util as util_commands

@click.group()
@click.option('-v','--verbose', is_flag=True, default=False, help='enable verbose debug output on-screen')
@click.option('--log-location', type=click.STRING, default="./robinbot_log.txt", help='modify the log output location [default: robinbot_log.txt')
@click.option('-d','--disable-log-file', is_flag=True, default=False, help='disable the output log file')
@click.pass_context
def cli(ctx, verbose, log_location, disable_log_file):  

    log_format = '%(asctime)s:%(msecs)d %(name)s %(levelname)s \"%(message)s\"'
    screen_log_format = '%(asctime)s %(name)s %(levelname)s :: %(message)s'

    if not disable_log_file:
        logging.basicConfig(filename=log_location,
                            filemode='a',
                            format=log_format,
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.DEBUG)

        console = logging.StreamHandler()
        if verbose:
            console.setLevel(logging.DEBUG)
        else:
            console.setLevel(logging.INFO)
        formatter = logging.Formatter(screen_log_format)
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger().addHandler(console)

        logger = logging.getLogger('robinbot')
        logger.info("Robinbot started")
        logger.info("Writing logs to " + log_location)
        

    ctx_obj = {}
    ctx.obj = ctx_obj


cli.add_command(run_commands.cli)
cli.add_command(util_commands.cli)

if __name__ == "__main__":
    cli()