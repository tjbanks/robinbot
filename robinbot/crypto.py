import logging

import robin_stocks as r

class RobinhoodCryptoBot():

    def __init__(self,ticker):
        self.logger = logging.getLogger('robinbot.crypto.RobinhoodCryptoBot')
        self.login_obj = None

        self.ticker = ticker

        return

    def login(self, username, password):
        """
        Login to trading service
        """
        
        self.logger.info("attempting Robinhood login with username \"" + username + "\"")
        self.login_obj = r.login(username,password)

        return
    
    def logout(self):
        self.logger.info("attempting Robinhood logout")
        r.logout()

    def get_robin_stocks_instance(self):
        return r

    def get_crypto_quote(self):
        return r.crypto.get_crypto_quote(self.ticker)

    def get_crypto_positions(self):
        return r.crypto.get_crypto_positions()

    def execute_buy(self):
        return

    def execute_sell(self):
        return

    def step(self):
        """
        This function will be called at a fixed interval to predict then buy, sell, or hold
        """
        return