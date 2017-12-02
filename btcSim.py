import random
from forex_python.bitcoin import BtcConverter

class BTCSim(object):
    def __init__(self, btc, fund):
        self.btc = btc
        self.predictor = random.randint(0, 1) 
        self.fund = fund
        self.btcPrice  = BtcConverter().get_latest_price('USD')
        self.totalFund = self.fund + self.btcPrice*self.btc
    
    def trading(self):
        while(self.totalFund >= self.btcPrice):
            if (self.fund == 0):
                self.addFund();
            if(self.btc != 0):
                if(self.predictor == 0):
                    self.sell();
                else:
                    self.buy()
            
    def addFund (self):
        tradecont = raw_input("You do not have enough funds to buy more bitcoins. Would you like to continue to trade? y/n")
        tradecont = tradecont.lower()
        while(tradecont != 'y' or tradecont != 'n'):
            raw_input("Would you like to continue to trade? y/n")
            if(tradecont == 'n'):
                print("Have a nice day")
                break;
            else:
                self.fund  = int(raw_input("How much fund would you like to deposit into the bitcoin market?"))
    
                    
    def sell(self):
        self.btc = self.btc - 1
        self.fund  = self.fund + random.randint(1,100)
        self.updateTotal()
        self.predictor = random.randint(0, 1) 
        print ("You sold a bitcoin. Now you have {} bitcoins. Your current fund is {}".format(self.btc, self.fund))
    
    def buy(self):
        if(self.totalFund >= self.btcPrice):
            self.btc = self.btc + 1
            self.fund  = self.fund - random.randint(1,100)
            self.updateTotal()
            print ("You bought a bitcoin. Now you have {} bitcoins. Your current fund is {}".format(self.btc, self.fund))
        else:
            self.addFund()
        self.predictor = random.randint(0, 1) 
    
    def updateTotal(self):
        self.totalFund = self.fund + self.btcPrice*self.btc
       
def main():
    bitcoin = raw_input("How much bitcoin do you own? :)")
    fund = raw_input("How much fund did you deposit into the bitcoin market?")
    btcsim = BTCSim(int(bitcoin), int(fund))
    btcsim.trading()
if __name__ == "__main__":
    main()