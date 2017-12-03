import random
import csv

class BTCSim(object):
    def __init__(self, btc, fund, btcPrice):
        self.btc = btc
        self.predictor = random.randint(0, 1) 
        self.fund = fund
        self.btcPrice  = btcPrice
        self.iterate = 0
        self.trad = True
        self.totalFund = self.fund + float(self.btcPrice[self.iterate][2])*self.btc
    
    def trading(self):
        while(self.trad):
            if (self.fund == 0):
                self.addFund();
            if(self.btc != 0):
                if(self.predictor == 0 or self.btcPrice[self.iterate][2] >= self.btcPrice[self.iterate+1][2] ):
                    self.sell();
                else:
                    self.buy()
            
    def addFund (self):
        tradecont = raw_input("You do not have enough funds to buy more bitcoins. Would you like to continue to trade? y/n")
        print ("Current bitcoin price {}".format(self.btcPrice))
        tradecont = tradecont.lower()
        while(tradecont != 'y' or tradecont != 'n'):
            raw_input("Would you like to continue to trade? y/n")
            if(tradecont == 'n'):
                self.trad = False
                print("Have a nice day")
                break;
            else:
                self.fund  = int(raw_input("How much fund would you like to deposit into the bitcoin market?"))
                break;
    
                    
    def sell(self):
        self.btc = self.btc - 1
        self.fund  = self.fund + random.randint(1,100)
        self.updateTotal()
        self.predictor = random.randint(0, 1) 
        print ("You sold a bitcoin. Now you have {} bitcoins. Your current fund is {}".format(self.btc, self.fund))
    
    def buy(self):
        if(self.totalFund >= float(self.btcPrice[self.iterate][2])):
            self.btc = self.btc + 1
            self.fund  = self.fund - random.randint(1,100)
            self.updateTotal()
            
            print ("You bought a bitcoin. Now you have {} bitcoins. Your current fund is {}".format(self.btc, self.fund))
        else:
            self.addFund()
        self.predictor = random.randint(0, 1) 
    
    def updateTotal(self):
        self.iterate = self.iterate + 1
        self.totalFund = self.fund + float(self.btcPrice[self.iterate][2])*self.btc
       
def main():
    bitcoin = raw_input("How much bitcoin do you own? :)")
    fund = raw_input("How much fund did you deposit into the bitcoin market?")
    with open("hourlybtc.csv", 'r') as my_file:
        reader = csv.reader(my_file, delimiter=',')
        btcConvert = list(reader)
        
    btcConvert.pop(0);
    btcsim = BTCSim(int(bitcoin), int(fund),btcConvert)
    btcsim.trading()
if __name__ == "__main__":
    main()