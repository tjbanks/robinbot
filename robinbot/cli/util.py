import click
import logging
import os

@click.group('util')
@click.pass_context
def cli(ctx):
    ctx.obj['logger'] = logging.getLogger('robinbot.cli.util')
    pass

@cli.command('generate-config', help="Generates a config file for the program to use")
@click.option('--location', type=click.STRING, default=None, help="override the default write location (current directory)")
@click.pass_context
def cell(ctx,location):
    logger = ctx.obj['logger']
    logger.info("Function not yet implemented.")