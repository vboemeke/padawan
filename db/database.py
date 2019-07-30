import datetime
import os
import sqlite3


class Database:

    def __init__(self):
        self.__data_dir = './data'
        self.__logs_dir = './data/logs'
        self.__db_path = './data/padawan.db'
        self.__create_log_path()

        self.__conn = sqlite3.connect(self.__db_path)
        self.__cursor = self.__conn.cursor()
        self.__create_tables()

    def __del__(self):
        if self.__conn:
            self.__conn.close()

    def __create_log_path(self):
        if not os.path.exists(self.__data_dir):
            os.makedirs(self.__data_dir)

        if not os.path.exists(self.__logs_dir):
            os.makedirs(self.__logs_dir)

    def __create_tables(self):
        exchanges = ['kraken', 'bittrex', 'bitmex', 'bitfinex', 'bitstamp', 'okcoin', 'binance', 'coss', 'kucoin',
                     'poloniex', 'theocean', 'upbit']

        self.__create_attempt_table()
        self.__create_trade_table()
        self.__create_opportunity_table()

        for exchange in exchanges:
            self.__create_exchange_table(exchange)

    def __create_exchange_table(self, exchange_name):

        self.__cursor.execute(
            'CREATE TABLE IF NOT EXISTS {table_name} ('
            ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
            ' created_at DATETIME NOT NULL,'
            ' bid DECIMAL(8, 2),'
            ' bid_volume DECIMAL(8, 2),'
            ' ask DECIMAL(8, 2),'
            ' ask_volume DECIMAL(8, 2),'
            ' attempt_id INTEGER,'
            ' CONSTRAINT fk_attempts'
            '   FOREIGN KEY (attempt_id)'
            '   REFERENCES attempts(id))'.format(table_name=exchange_name))

        self.__conn.commit()

    def __create_attempt_table(self):

        self.__cursor.execute(
            'CREATE TABLE IF NOT EXISTS attempts ('
            ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
            ' created_at DATETIME NOT NULL,'
            ' actual_balance DECIMAL(8, 2),'
            ' target_entry_spread bid DECIMAL(8, 2),'
            ' profit_target bid DECIMAL(8, 2))')

        self.__conn.commit()

    def __create_trade_table(self):
        self.__cursor.execute(
            'CREATE TABLE IF NOT EXISTS trade ('
            ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
            ' created_at DATETIME NOT NULL,'
            ' buying_exchange TEXT,'
            ' usd_buy DECIMAL(8, 2),'
            ' selling_exchange TEXT,'
            ' usd_sell DECIMAL(8, 2),'
            ' trade_volume DECIMAL(8, 2),'
            ' attempt_id INTEGER,'
            ' opportunity_id INTEGER,'
            ' CONSTRAINT fk_attempts'
            '   FOREIGN KEY (attempt_id)'
            '   REFERENCES attempts(id),'
            ' CONSTRAINT fk_opportunity,'
            '   FOREIGN KEY (opportunity_id)'
            '   REFERENCES opportunity(id))')

        self.__conn.commit()

    def __create_opportunity_table(self):
        self.__cursor.execute(
            'CREATE TABLE IF NOT EXISTS opportunity ('
            ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
            ' created_at DATETIME NOT NULL,'
            ' selling_exchange TEXT NOT NULL,'
            ' buying_exchange TEXT NOT NULL,'
            ' max_bid_price DECIMAL(8, 2),'
            ' min_ask_price DECIMAL(8, 2),'
            ' max_bid_volume DECIMAL(8, 2),'
            ' min_ask_volume DECIMAL(8, 2),'
            ' spread DECIMAL(8, 2),'
            ' attempt_id INTEGER,'
            ' CONSTRAINT fk_attempts'
            '   FOREIGN KEY (attempt_id)'
            '   REFERENCES attempts(id))')

        self.__conn.commit()

    def add_bid_ask_to_db(self, exchange_name, bid, bid_volume, ask, ask_volume, attempt):

        self.__cursor.execute('''INSERT INTO {table_name}(created_at, bid, bid_volume, ask, ask_volume, attempt_id)
                          VALUES(?,?,?,?,?,?)'''.format(table_name=exchange_name),
                              (datetime.datetime.now(), bid, bid_volume,
                               ask, ask_volume, attempt))

        self.__conn.commit()

    def new_attempt(self, actual_balance, target_entry_spread, profit_target):

        self.__cursor.execute('''INSERT INTO attempts(created_at,
                            actual_balance,
                            target_entry_spread,
                            profit_target)
                          VALUES(?,?,?,?)''',
                              (datetime.datetime.now(), actual_balance, target_entry_spread, profit_target))

        self.__conn.commit()

        return self.__cursor.lastrowid

    def new_opportunity(self,
                        selling_exchange,
                        buying_exchange,
                        max_bid_price,
                        min_ask_price,
                        max_bid_volume,
                        min_ask_volume,
                        spread,
                        attempt_id):

        self.__cursor.execute('''INSERT INTO opportunity(created_at,
                            selling_exchange,
                            buying_exchange,
                            max_bid_price,
                            min_ask_price,
                            max_bid_volume,
                            min_ask_volume,
                            spread,
                            attempt_id)
                          VALUES(?,?,?,?,?,?,?,?,?)''',
                              (datetime.datetime.now(), selling_exchange, buying_exchange, max_bid_price,
                               min_ask_price, max_bid_volume, min_ask_volume, spread, attempt_id))

        self.__conn.commit()

    def new_trade(self,
                  buying_exchange,
                  usd_buy,
                  selling_exchange,
                  usd_sell,
                  trade_volume,
                  attempt_id,
                  opportunity_id):

        self.__cursor.execute('''INSERT INTO trade(created_at,
                            buying_exchange,
                            usd_buy,
                            selling_exchange,
                            usd_sell,
                            trade_volume,
                            attempt_id,
                            opportunity_id)
                          VALUES(?,?,?,?,?,?,?,?)''',
                              (datetime.datetime.now(), buying_exchange, usd_buy, selling_exchange,
                               usd_sell, trade_volume, attempt_id, opportunity_id))

        self.__conn.commit()
