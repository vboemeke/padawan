import sqlite3
import datetime
import os

data_dir = './data'
logs_dir = './data/logs'


def create_tables():
    exchanges = ['bitstamp', 'bitmex', 'bitfinex', 'bittrex', 'okcoin', 'kraken']

    create_attempt_table()

    for exchange in exchanges:
        create_exchange_table(exchange)


def create_log_path():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)


def create_exchange_table(exchange_name):
    db = sqlite3.connect('./data/padawan.db')
    cursor = db.cursor()

    cursor.execute(
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

    db.commit()
    db.close()


def create_attempt_table():
    db = sqlite3.connect('./data/padawan.db')
    cursor = db.cursor()

    cursor.execute(
        'CREATE TABLE IF NOT EXISTS attempts ('
        ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' created_at DATETIME NOT NULL,'
        ' actual_balance DECIMAL(8, 2),'
        ' target_entry_spread bid DECIMAL(8, 2),'
        ' profit_target bid DECIMAL(8, 2))')

    db.commit()
    db.close()


def add_bid_ask_to_db(exchange_name, bid, bid_volume, ask, ask_volume, attempt):
    db = sqlite3.connect('./data/padawan.db')
    cursor = db.cursor()

    cursor.execute('''INSERT INTO {table_name}(created_at, bid, bid_volume, ask, ask_volume, attempt_id)
                      VALUES(?,?,?,?,?,?)'''.format(table_name=exchange_name),
                   (datetime.datetime.now(), bid, bid_volume,
                    ask, ask_volume, attempt))
    db.commit()
    db.close()


def new_attempt(actual_balance, target_entry_spread, profit_target):
    db = sqlite3.connect('./data/padawan.db')
    cursor = db.cursor()

    cursor.execute('''INSERT INTO attempts(created_at,
                        actual_balance,
                        target_entry_spread,
                        profit_target)
                      VALUES(?,?,?,?)''',
                   (datetime.datetime.now(), actual_balance, target_entry_spread, profit_target))

    db.commit()
    db.close()

    return cursor.lastrowid
