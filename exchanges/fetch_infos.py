import ccxt

exchange_list = ['kraken', 'bittrex', 'bitmex', 'bitfinex', 'bitstamp', 'okcoin']

exchange_fees = {'bitmex': 0.0020,
                 'bittrex': 0.0020,
                 'kraken': 0.0025,
                 'bitfinex': 0.0025,
                 'bitstamp': 0.0025,
                 'okcoin': 0.0025}


def fetch_exchange_data(exchange_name):
    # binance = ccxt.binance()
    # kucoin = ccxt.kucoin()
    # poloniex = ccxt.poloniex()
    bitstamp = ccxt.bitstamp()
    bitmex = ccxt.bitmex()
    bitfinex = ccxt.bitfinex2()
    bittrex = ccxt.bittrex()
    okcoin = ccxt.okcoinusd()
    kraken = ccxt.kraken({
        'apiKey': 'YOUR_PUBLIC_API_KEY',
        'secret': 'YOUR_SECRET_PRIVATE_KEY',
    })
    dict_of_exchanges = {'kraken': kraken,
                         'bitmex': bitmex,
                         'bittrex': bittrex,
                         'bitstamp': bitstamp,
                         'bitfinex': bitfinex,
                         'okcoin': okcoin}
    try:
        return dict(dict_of_exchanges[exchange_name].fetch_order_book('BTC/USD'))
    except Exception as ex:
        print(ex)
        return {}
