
'''From the Python Binance documenatation'''

# Create an order
from binance.enums import *
order = client.create_order(
    symbol='BNBBTC',
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=100,
    price='0.00001')

# Buy or sell
order = client.order_market_buy(
    symbol='BNBBTC',
    quantity=100)

order = client.order_market_sell(
    symbol='BNBBTC',
    quantity=100

# One cancels one order (one placed the other one canceled)
from binance.enums import *
order = client.create_oco_order(
    symbol='BNBBTC',
    side=SIDE_SELL,
    stopLimitTimeInForce=TIME_IN_FORCE_GTC,
    quantity=100,
    stopPrice='0.00001'
    price='0.00002')

# Test order creates and validates the order but not sent to the exchange
from binance.enums import *
order = client.create_test_order(
    symbol='BNBBTC',
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=100,
    price='0.00001')

# Cancel an order
result = client.cancel_order(
    symbol='BNBBTC',
    orderId='orderId')

# Get all open orders
orders = client.get_open_orders(symbol='BNBBTC')


#Get account info
info = client.get_account()
#Get asset balance
balance = client.get_asset_balance(asset='BTC')
#Get account status
status = client.get_account_status()
#Get trades
trades = client.get_my_trades(symbol='BNBBTC')

#Get trade fees
# get fees for all symbols
fees = client.get_trade_fee()
# get fee for one symbol
fees = client.get_trade_fee(symbol='BNBBTC')

#Get asset details
details = client.get_asset_details()
#Get dust log
log = client.get_dust_log()
#Transfer dust
transfer = client.transfer_dust(asset='BNZ')
#Get Asset Dividend History
history = client.get_asset_dividend_history()


"""Withdrawals have to be confirmed by email first before it can be done through the API"""
from binance.exceptions import BinanceAPIException, BinanceWithdrawException
try:
    # name parameter will be set to the asset value by the client if not passed
    result = client.withdraw(
        asset='ETH',
        address='<eth_address>',
        amount=100)
except BinanceAPIException as e:
    print(e)
except BinanceWithdrawException as e:
    print(e)
else:
    print("Success")

# passing a name parameter
result = client.withdraw(
    asset='ETH',
    address='<eth_address>',
    amount=100,
    name='Withdraw')

# if the coin requires a extra tag or name such as XRP or XMR then pass an `addressTag` parameter.
result = client.withdraw(
    asset='XRP',
    address='<xrp_address>',
    addressTag='<xrp_address_tag>',
    amount=10000

'''FAQ on the Python Binance documenation'''