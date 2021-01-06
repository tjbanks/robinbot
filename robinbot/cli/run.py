import click
import logging
import os

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
def cell(ctx,logout):
    logger = logging.getLogger('robinbot.cli.run.trader')
    logger.debug('initializing trader bot')

    bot = RobinhoodCryptoBot('DOGE')
    bot.login('username','')

    import pdb;pdb.set_trace()

    if logout:
        bot.logout()

@cli.command('recorder', help="Record a ticker into a csv file")
@click.pass_context
def recorder(ctx):
    logger = logging.getLogger('robinbot.cli.run.recorder')
    logger.debug('initializing trader bot')

    bot = RobinhoodCryptoBot('DOGE')
    bot.login('username','')
    
    i = 0
    rows = []

    s = sched.scheduler(time.time, time.sleep)

    def record(sc):
        nonlocal i
        temp = bot.get_crypto_quote()
        temp['timestamp'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print(i)
        i = i + 1
        print(temp)
        rows.append(temp)
        if i % 10 == 0:
            df = pd.DataFrame.from_dict(rows,orient='columns')
            df.to_csv('DOGE.csv')
        sc.enter(1, 1, record, (sc,))

    s.enter(1, 1, record, (s,))
    s.run()



    