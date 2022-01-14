import backtrader as bt 
import datetime

class VIXStrategy(bt.Strategy):

    # "I save a reference to the vix close and spy open and close and im gonna use that in our strategy,
    # so im gonna reference that with self.vix and self.spyopen and self.spyclose"
    # --> search on when to use init, and self, why not use 'this' function?
    def __init__(self):
        self.vix = self.datas[0].vixclose
        self.spyopen = self.datas[0].open
        self.spyclose = self.datas[0].close 

    # simple logger utility function thats often used so you can just plot the date at any given time in a certain format 
    # and its just a print statement really and it just formats my logging data in a certain format 
    def log(self, txt, dt=None):
        ''' Logging function for this strategy '''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    # bulk of the strategy is in this next function 
    def next(self):
        # self.log(self.current_data)
        # so if the vix close is currently more than the arbitray VIX benchmark you have set, then you will engage this if statement
        # this is the arbitrary level you have set that you think past this point, will trigger chaos
        vix_benchmark = 35

        # this strategy is basically buying when the VIX level hits 35, cos that indicates huge selling volatility and downward pressure on the market 
        # then closing positions once the VIX level hits less than 12, cos it indicates good market stability and price should have reverted to mean or higher!
        if self.vix[0] > vix_benchmark:
            # logging the function calls 
            self.log('Previous VIX, %.2f' % self.vix[0])
            self.log('SPY Open, %.2f' % self.spyopen[0])

            # so if you dont already have a position, or if you have a cash reserve amount of more than $5000
            # then you will open a position in the market of size as calculated below 
            if not self.position or self.broker.getcash() > 5000:
                size = int(self.broker.getcash() / self.spyopen[0])
                print("Buying {} SPY at {}".format(size, self.spyopen[0]))
                self.buy(size=size)

        # if VIX goes less than 12, and you have a position in self.position,
        # having self.close() will close all open positions, you can also choose self.sell() to sell a certain number of shares 
        if self.vix[0] < 12 and self.position: 
            self.close()


