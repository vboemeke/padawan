import sqlite3
import datetime


def create_tables():
    exchanges = ['bitstamp', 'bitmex', 'bitfinex', 'bittrex', 'okcoin', 'kraken']

    for exchange in exchanges:
        create_table(exchange)


def create_table(exchange_name):
    db = sqlite3.connect('./data/padawan.db')

    cursor = db.cursor()

    cursor.execute(
        'CREATE TABLE IF NOT EXISTS {table_name} ('
        'created_at DATETIME NOT NULL,'
        ' bid DECIMAL(8, 2),'
        ' bid_volume DECIMAL(8, 2),'
        ' ask DECIMAL(8, 2),'
        ' ask_volume DECIMAL(8, 2))'
        .format(table_name=exchange_name))

    db.commit()
    db.close()


def add_bid_ask_to_db(exchange_name, bid, bid_volume, ask, ask_volume):
    db = sqlite3.connect('./data/padawan.db')

    cursor = db.cursor()

    cursor.execute('''INSERT INTO {table_name}(created_at, bid, bid_volume, ask, ask_volume)
                      VALUES(?,?,?,?,?)'''.format(table_name=exchange_name), (datetime.datetime.now(), bid, bid_volume,
                                                                              ask, ask_volume))
    db.commit()
    db.close()
