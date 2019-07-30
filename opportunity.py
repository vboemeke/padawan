from db.database import Database
from trade import Trade


class Opportunity:

    def __init__(self, book_df, attempt):
        self.book_df = book_df
        self.max_bid_price = self.__max_bid_price()
        self.min_ask_price = self.__min_ask_price()
        self.max_bid_volume = self.__max_bid_volume()
        self.min_ask_volume = self.__min_ask_volume()
        self.selling_exchange = self.__best_bid_exchange_price()
        self.buying_exchange = self.__best_ask_exchange_price()
        self.trade_volume = self.__trade_volume(self.max_bid_volume, self.min_ask_volume)
        self.spread = float(self.max_bid_price / self.min_ask_price)

        self.__db = Database()
        self.__save_new_opportunity(attempt)

    def __max_bid_price(self):
        return self.book_df['Bid Price'].max()

    def __min_ask_price(self):
        return self.book_df['Ask Price'].min()

    def __best_ask_exchange_price(self):
        # need to check why: "IndexError: index 0 is out of bounds for axis 0 with size 0"
        # volume_bid: nan e volume_ask: nan
        return self.book_df.loc[
            (self.book_df['Ask Price'] == self.min_ask_price) &
            (self.book_df['Ask Volume'] == self.min_ask_volume)]['Exchange'].values[0]

    def __best_bid_exchange_price(self):
        return self.book_df.loc[
            (self.book_df['Bid Price'] == self.max_bid_price) &
            (self.book_df['Bid Volume'] == self.max_bid_volume)]['Exchange'].values[0]

    @staticmethod
    def __trade_volume(bid, ask):
        return float(0.5 * ask) if bid > ask else float(0.5 * bid)

    # TODO: I need to validate when two exchanges contains the same max_bid_price
    def __max_bid_volume(self):
        return self.book_df[self.book_df['Bid Price'] == self.max_bid_price]['Bid Volume'].max()

    # TODO: I need to validate when two exchanges contains the same min_ask_price
    def __min_ask_volume(self):
        return self.book_df[self.book_df['Ask Price'] == self.min_ask_price]['Ask Volume'].max()

    def simulate_trade(self, logger, attempt):
        usd_buy = -(self.min_ask_price * self.trade_volume)
        usd_sell = (self.max_bid_price * self.trade_volume)

        trade = Trade(self.buying_exchange, usd_buy, self.selling_exchange, usd_sell, self.trade_volume)

        # TODO save opportunity_id
        self.__db.new_trade(self.buying_exchange, usd_buy, self.selling_exchange, usd_sell, self.trade_volume, attempt, 0)

        logger.run('Comprou: \n Volume: %s \n Cotação: %s \n Custo da Operação: %s \n Exchange: %s' % (
            trade.trade_volume, self.min_ask_price, trade.usd_buy, trade.buying_exchange))
        logger.run('Vendeu: \n Volume: %s \n Cotação: %s \n Receita da Operação: %s \nExchange: %s' % (
            trade.trade_volume, self.max_bid_price, trade.usd_sell, trade.selling_exchange))

        return trade

    def __save_new_opportunity(self, attempt):
        self.__db.new_opportunity(self.selling_exchange,
                                  self.buying_exchange,
                                  self.max_bid_price,
                                  self.min_ask_price,
                                  self.max_bid_volume,
                                  self.min_ask_volume,
                                  self.spread,
                                  attempt)
