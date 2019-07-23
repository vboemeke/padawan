import ccxt

exchange_list = ['kraken', 'bittrex', 'bitmex', 'bitfinex', 'bitstamp', 'okcoin', 'binance', 'coss', 'kucoin', 'poloniex', 'theocean', 'upbit']

# Original fees (blackbird)
# exchange_fees = {'bitmex': 0.0020,
#                  'bittrex': 0.0020,
#                  'kraken': 0.0025,
#                  'bitfinex': 0.0025,
#                  'bitstamp': 0.0025,
#                  'okcoin': 0.0025}

# Fees for aprox. US$ 250k (monthly volume)
# exchange_fees = {'bitmex': 0.005,
#                  'bittrex': 0.0025,
#                  'kraken': 0.0016,
#                  'bitfinex': 0.0015,
#                  'bitstamp': 0.0024,
#                  'okcoin': 0.00075}

# simulating aprox. USD 2.500 -> 5.000 MM (Trading volume fees)
exchange_fees = {'bitmex': 0.005,
                 'bittrex': 0.0025,
                 'kraken': 0.0009,
                 'bitfinex': 0.0012,
                 'bitstamp': 0.0012,
                 'okcoin': 0.0004,
                 'binance': 0.006,
                 'coss': 0.006,
                 'kucoin': 0.006,
                 'poloniex': 0.006,
                 'theocean': 0.006,
                 'upbit': 0.006
                 }

def fetch_exchange_data(exchange_name):
    bitstamp = ccxt.bitstamp()
    bitmex = ccxt.bitmex()
    bitfinex = ccxt.bitfinex2()
    bittrex = ccxt.bittrex()
    okcoin = ccxt.okcoinusd()
    kraken = ccxt.kraken({
        'apiKey': 'YOUR_PUBLIC_API_KEY',
        'secret': 'YOUR_SECRET_PRIVATE_KEY',
    })
    binance = ccxt.binance()
    coss = ccxt.coss()
    kucoin = ccxt.kucoin2()
    poloniex = ccxt.poloniex()
    # theocean = ccxt.theocean()
    upbit = ccxt.upbit()
    dict_of_exchanges = {'kraken': kraken,
                         'bitmex': bitmex,
                         'bittrex': bittrex,
                         'bitstamp': bitstamp,
                         'bitfinex': bitfinex,
                         'okcoin': okcoin,
                         'binance': binance,
                         'coss': coss,
                         'kucoin': kucoin,
                         'poloniex': poloniex,
                         # 'theocean': theocean,
                         'upbit': upbit}
    try:
        return dict(dict_of_exchanges[exchange_name].fetch_order_book('BTC/USD'))
        # return dict(dict_of_exchanges[exchange_name].fetch_order_book('XRP/USD'))
        # return dict(dict_of_exchanges[exchange_name].fetch_order_book('LTC/USD'))
        # add BitcoinCash
        # return dict(dict_of_exchanges[exchange_name].fetch_order_book('ETH/USD'))
    except Exception as ex:
        print('%s - erro: %s' %(exchange_name, ex))
        return {}