import click
import logging
import os, sys

import pandas as pd
from time import strftime,gmtime
import sched, time

from robinbot.crypto import RobinhoodCryptoBot

@click.group('run')
@click.pass_context
def cli(ctx):

    pass

@cli.command('trader', help="Run the trading algorithm specified by your configuration file")
@click.option('-l','--logout', is_flag=True, default=False, help='logout at the end of run, disabled by default')
@click.pass_context
def trader(ctx,logout):
    logger = logging.getLogger('robinbot.cli.run.trader')
    logger.debug('initializing trader bot')

    username = ctx.obj['username']

    bot = RobinhoodCryptoBot('DOGE')
    bot.login(username,'')

    import pdb;pdb.set_trace()

    if logout:
        bot.logout()

@cli.command('recorder', help="Record a ticker into a csv file")
@click.pass_context
def recorder(ctx):
    logger = logging.getLogger('robinbot.cli.run.recorder')
    logger.debug('initializing trader bot')

    username = ctx.obj['username']

    bot = RobinhoodCryptoBot('DOGE')
    bot.login(username,'')
    
    i = 0
    rows = []
    errors = 0

    s = sched.scheduler(time.time, time.sleep)

    def record(sc):
        
        nonlocal i, errors
        temp = None
        
        try:
            temp = bot.get_crypto_quote()
        except Exception as e:
            errors = errors + 1
            logger.error("error occurred when obtaining robinhood data, retrying")
        
        sc.enter(1, 1, record, (sc,))

        if temp:
            errors = 0
            temp['timestamp'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            
            i = i + 1
            print(temp)
            rows.append(temp)

        if i % 10 == 0:
            df = pd.DataFrame.from_dict(rows,orient='columns')
            df.to_csv('DOGE1.csv')
        
        if errors == 10:
            logger.error("10 errors occurred in a row... quitting")
            sys.exit(1)

    s.enter(1, 1, record, (s,))
    s.run()



    