class Trade:

    def __init__(self, buying_exchange, usd_buy, selling_exchange, usd_sell, trade_volume):
        self.buying_exchange = buying_exchange
        self.usd_buy = usd_buy
        self.selling_exchange = selling_exchange
        self.usd_sell = usd_sell
        self.trade_volume = trade_volume
