import alpaca_trade_api as tradeapi
import threading
from fastapi import FastAPI, HTTPException, Response

class Martingale(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.key = open('Alpaca_Key.txt', 'r').read()
        self.secret = open('Alpaca_Secret.txt', 'r').read()
        self.alpaca_endpoint = 'https://paper-api.alpaca.markets'
        self.api = tradeapi.REST(self.key, self.secret, self.alpaca_endpoint)
        self.symbol = 'IVV'                                                     #selection of stocks in S&P500 - could pick any, like SPY
        self.current_order = None
        self.last_price = 1                                                     # Simplified poisiton for IVV (i.e., only 1 position open at a time for short and long)

        try:
            self.position = int(self.api.get_position(self.symbol).qty)
        except:
            self.position = 0


    def submit_order(self, target):
        with self.lock:
            if self.current_order is not None:                                      #if current order is open
                self.api.cancel_order(self.current_order.id)                        #cancel the possible 2nd order

            delta = target - self.position                                          # define delta (delta asset / delta derivative)

            if delta == 0:                                                          # Call: if delta > 1 | Put: if delta < 1
                return False, 'No Change in Position'                             # if there is no change, no point in changing our position
            #print(f'Processing the order for {target} shares')

            if delta > 0:                                                           # put - we want to buy
                buy_quantity = delta
                if self.position < 0:                                               # if there are no current orders open
                    buy_quantity = min(abs(self.position), buy_quantity)
                #print(f'Buying {buy_quantity} shares')
                self.current_order = self.api.submit_order(self.symbol, buy_quantity, "buy", "limit", "day", self.last_price)
                return True, f'Bought {buy_quantity} shares of {self.symbol}'

            elif delta < 0:                                                         # call - we want to sell
                sell_quantity = delta
                if self.position > 0:
                    sell_quantity = min(abs(self.position), sell_quantity)
                #print(f'Selling {sell_quantity} shares')
                self.current_order = self.api.submit_order(self.symbol, sell_quantity, "sell", "limit", "day", self.last_price)
                return True, f'Sold {abs(sell_quantity)} shares of {self.symbol}'


if __name__ == '__main__':
    app = Martingale()
    order = input("How many shares do you want to submit?")
    app.submit_order(int(order))
