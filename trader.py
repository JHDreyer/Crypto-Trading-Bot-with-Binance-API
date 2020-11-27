from binance.client import Client


class Trader:
    def __init__(self, file):
        self.connect(file)

    def connect(self, file):  # Creates Binance client
        lines = [line.rstrip('\n') for line in open(file)]
        key = lines[0]
        secret = lines[1]
        self.client = Client(key, secret)

    def getBalances(self):  # Gets all account balances
        prices = self.client.get_withdraw_history()
        return prices


filename = 'credentials.txt'
trader = Trader(filename)
balances = trader.getBalances()
print(balances)