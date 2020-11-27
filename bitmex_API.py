from bitmex import bitmex
import json
from datetime import datetime, timedelta
import pandas as pd
from datetime import datetime
# get df, name columns, drop unneeded columns


# bitmex Testnet

secret_bitmex_testnet = 'pVF7qIjIQxhf4z4FPpnMZt6bTgfHchgJmrYtpaHRTCpStVgK'
id_bitmex_testnet = 'SXLwNRGThtcTy2xXPMdxz0-9'

bitmex_client = bitmex(test=False, api_key=id_bitmex_testnet, api_secret=secret_bitmex_testnet)


result = bitmex_client.Trade.Trade_getBucketed(symbol='XBTUSD', binSize='1m', count=4, startTime=datetime.now()).result()[0]

print(result)

# real bitmex secret: pwSlHy3xlRGFSCg7cTsWyKUyGMdI784zYWNPXOVSy5VeAuKS
#real bitmex id : izdAkKZICM2zJ-qsuUoOGI68

"""AttributeError: Resource Quote not found. Available resources: APIKey, Announcement, Chat, Execution,
 Funding, GlobalNotification, Instrument, Insurance, Leaderboard, Liquidation, Order, OrderBook, Position,
  Schema, Settlement, Stats, Trade, User, UserEvent"""