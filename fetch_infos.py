import ccxt


def fetch_data(exchange_name):
    bitmex = ccxt.bitmex()
    binance = ccxt.binance()
    bittrex = ccxt.bittrex()
    kucoin = ccxt.kucoin()
    poloniex = ccxt.poloniex()
    kraken = ccxt.kraken({
        'apiKey': 'YOUR_PUBLIC_API_KEY',
        'secret': 'YOUR_SECRET_PRIVATE_KEY',
    })
    dict_of_exchanges = {'kraken': kraken, 'bitmex': bitmex, 'bittrex': bittrex}
    the_book = {}
    try:
        the_book = dict(dict_of_exchanges[exchange_name].fetch_order_book('BTC/USD'))
    except:
        the = {}
    return the_book
