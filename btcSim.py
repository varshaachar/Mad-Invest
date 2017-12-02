import random
class BTCSim(object):
    def __init__(self, btc, fund):
        self.btc = btc
        self.predictor = random.randint(0, 1) 
        self.fund = fund
    
    def trading(self):
        while(self.fund >= 0):
            
            if(self.btc != 0):
                if(self.predictor == 0):
                    self.sell();
            
    def addFund (self):
        tradecont = raw_input("Would you like to continue to trade? y/n")
        tradecont = tradecont.lower()
        while(tradecont != 'y' or tradecont != 'n'):
            raw_input("Would you like to continue to trade? y/n")
            if(tradecont == 'n'):
                break;
            else:
                self.fund  = int(raw_input("How much fund would you like to deposit into the bitcoin market?"))
                    
    def sell(self):
        self.btc = self.btc - 1
        self.fund  = self.fund + random.randint(1,100)
        print ("You sold a bitcoin. Now you have {} bitcoins. Your current fund is {}".format(self.btc, self.fund))
    
    def buy(self):
        self.btc = self.btc + 1
        self.fund  = self.fund - random.randint(1,100)
        print ("You bought a bitcoin. Now you have {} bitcoins. Your current fund is {}".format(self.btc, self.fund))
       
def main():
    bitcoin = raw_input("How much bitcoin do you own? :)")
    fund = raw_input("How much fund did you deposit into the bitcoin market?")
    btcsim = BTCSim(int(bitcoin), int(fund))
    btcsim.trading()
if __name__ == "__main__":
    main()