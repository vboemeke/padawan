import ccxt


def fetch_exchange_data(exchange_name):
    # binance = ccxt.binance()
    # kucoin = ccxt.kucoin()
    # poloniex = ccxt.poloniex()
    bitmex = ccxt.bitmex()
    bittrex = ccxt.bittrex()
    kraken = ccxt.kraken({
        'apiKey': 'YOUR_PUBLIC_API_KEY',
        'secret': 'YOUR_SECRET_PRIVATE_KEY',
    })
    dict_of_exchanges = {'kraken': kraken,
                         'bitmex': bitmex,
                         'bittrex': bittrex}
    try:
        return dict(dict_of_exchanges[exchange_name].fetch_order_book('BTC/USD'))
    except:
        return {}
