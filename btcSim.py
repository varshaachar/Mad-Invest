from pprint import pprint

import random
import csv
import requests
import json


class BTCSim(object):
    def __init__(self, btc, fund, btcPrice):
        self.btc = btc
        self.predictor = random.randint(0, 1)
        self.fund = fund
        self.btcPrice = btcPrice
        self.iterate = 0
        self.trad = True
        self.totalFund = self.fund + float(self.btcPrice[self.iterate]) * self.btc

    def trading(self):
        while self.iterate < len(self.btcPrice) - 1:
            if (self.btc != 0):
                if (self.predictor == 0):
                    self.sell()
                else:
                    self.buy()

    # def addFund(self):
    #     tradecont = input("You do not have enough funds to buy more bitcoins. Would you like to continue to trade?
    # y/n")
    #     print("Current bitcoin price {}".format(self.btcPrice))
    #     tradecont = tradecont.lower()
    #     while (self.iterate < len(self.btcPrice)):
    #         input("Would you like to continue to trade? y/n")
    #         if (tradecont == 'n'):
    #             self.trad = False
    #             print("Have a nice day")
    #             return
    #         else:
    #             self.fund = int(input("How much fund would you like to deposit into the bitcoin market?"))
    #             return

    def sell(self):
        self.btc = self.btc - 1
        self.fund = self.fund + random.randint(1, 100)
        self.updateTotal()
        self.predictor = random.randint(0, 1)

    def buy(self):
        if (self.totalFund >= float(self.btcPrice[self.iterate])):
            self.btc = self.btc + 1
            self.fund = self.fund - random.randint(1, 100)
            self.updateTotal()
        else:
            self.addFund()
        self.predictor = random.randint(0, 1)

    def updateTotal(self):
        print(self.iterate, self.totalFund)
        self.iterate = self.iterate + 1
        self.totalFund = self.fund + float(self.btcPrice[self.iterate]) * self.btc
        # URL = whatever URL that we are aiming to do
        payload = {
            "btc": self.btc,
            "predictor": self.predictor,
            "fund": self.fund,
            "btcPrice": self.btcPrice,
            "trad": self.btcPrice,
            "totalFund": self.totalFund
        }


def main():
    r = requests.get('https://api.github.com/events')  # insert which ever url we are using
    # bitcoin = input("How much bitcoin do you own? :)")
    # fund = input("How much fund did you deposit into the bitcoin market?")
    bitcoin, fund = 3, 1000

    with open("hourlybtc.csv", 'r') as my_file:
        reader = csv.reader(my_file, delimiter=',')
        btcConvert = list(reader)

    # print(btcConvert)

    btcConvert.pop(0)

    btc_pricehistory = [float(x[2]) for x in btcConvert]

    # pprint(btc_pricehistory)
    btcsim = BTCSim(int(bitcoin), int(fund), btc_pricehistory)

    btcsim.trading()


if __name__ == "__main__":
    main()
