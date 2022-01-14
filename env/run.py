# so the matplotlib, is now the older version of 3.2.2, the newer version has some bug that doesnt allow for proper plotting
import backtrader as bt
import os
# you import VIXStrategy from the class in the other python script 
import main

cerebro = bt.Cerebro()
# setting the starting amount to 100,000 in brokerage account 
cerebro.broker.set_cash(100000)

# you connect a data feed into cerebro 
# and then you connect a strategy that you apply to that data feed 
# and then see the outcome on the final amount of your portfolio 

class SPYVIXData(bt.feeds.GenericCSVData):

    # can use these lines as attributes in your strategy 
    lines = ('vixopen', 'vixhigh', 'vixlow', 'vixclose',)

    # formatting the columns in the excel
    # file properly and assigning them to columns 
    # which is signified by the numbers

    params = (
        ('dtformat', '%Y-%M-%d'),
        ('date', 0),
        ('spyopen', 1),
        ('spyhigh', 2),
        ('spylow', 3),
        ('spyclose', 4),
        ('spyadjclose', 5),
        ('spyvolume', 6),
        ('vixopen', 7),
        ('vixhigh', 8),
        ('vixlow', 9),
        ('vixclose', 10)
    )


# creating a vix data feed cos you will want to plot 2 data feeds side by side 
class VIXData(bt.feeds.GenericCSVData):
    params = (
        ('dtformat', '%Y-%M-%d'),
        ('date', 0),
        ('vixopen', 1),
        ('vixhigh', 2),
        ('vixlow', 3),
        ('vixclose', 4),
        ('volume', -1),
        ('openinterest', -1)
    )

# giving the file directory 
csv_file = os.path.dirname(os.path.realpath(__file__)) + '/spy_vix.csv'
vix_csv_file = os.path.dirname(os.path.realpath(__file__)) + '/vix.csv'

# passing the data from csv excel files to the class objects 
spyVixDataFeed = SPYVIXData(dataname=csv_file)
vixDataFeed = VIXData(dataname=vix_csv_file)
cerebro.adddata(spyVixDataFeed)
cerebro.adddata(vixDataFeed)

cerebro.addstrategy(main.VIXStrategy)

cerebro.run()
cerebro.plot(volume=False)
