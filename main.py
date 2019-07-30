# coding=utf-8

import time

import pandas as pd

import exchanges.fetch_infos as exchanges
from db.database import Database
from log.logger import Logger
from opportunity import Opportunity

target_entry_spread = 1.0025
profit_target = 0.00001
in_trade = False
start_balance = 0.00
actual_balance = 0.00
temp_balance = 0.00
greatest_spread = 0.00
global book_df
global current_trade

db = Database()


def generate_dataframe(exchange_list):
    list_of_books = []

    # TODO increase exchange list (validate symbols 'BTC/USC' doesn't work on other exchanges
    # but we need to check if is the same coin - ex. Dolar vs. Stable Dolar)

    for exchange_name in exchange_list:
        exchange_data = exchanges.fetch_exchange_data(exchange_name)
        if exchange_data != {}:
            max_bid_price = exchange_data['bids'][0][0]
            max_bid_volume = exchange_data['bids'][0][1]
            min_ask_price = exchange_data['asks'][0][0]
            min_ask_volume = exchange_data['asks'][0][1]

            db.add_bid_ask_to_db(exchange_name, max_bid_price, max_bid_volume, min_ask_price, min_ask_volume, attempt)
            list_of_books.append([exchange_name, max_bid_price, max_bid_volume, min_ask_price, min_ask_volume])

    return pd.DataFrame(list_of_books, columns=['Exchange', 'Bid Price', 'Bid Volume', 'Ask Price', 'Ask Volume'])


def spread_of(selling_exchange, buying_exchange):
    selling_exchange_actual_bid = book_df[book_df['Exchange'] == selling_exchange].values[0][1]
    buying_exchange_actual_sell = book_df[book_df['Exchange'] == buying_exchange].values[0][3]

    return float(selling_exchange_actual_bid) / float(buying_exchange_actual_sell)


# The magic begins here!

attempt = db.new_attempt(actual_balance, target_entry_spread, profit_target)
logger = Logger(attempt, target_entry_spread, profit_target)

logger.run('✅💰 Saldo inicial: US$ %f 💰✅' % actual_balance)

while 1 < 2:

    if not in_trade:
        book_df = generate_dataframe(exchanges.exchange_list)
    else:
        book_df = generate_dataframe([current_trade.buying_exchange, current_trade.selling_exchange])

    opportunity = Opportunity(book_df, attempt)

    logger.run('###############################')

    entry_spread = float(opportunity.spread)
    if entry_spread > greatest_spread:
        logger.run('📈 *** Novo Record de Spread *** 📈')
        greatest_spread = entry_spread

        logger.run('==== \n Maior spread da análise = %f \n====' % greatest_spread)

    if not in_trade:
        logger.run('Spread atual - taxas e lucro:  %f' % (entry_spread - profit_target - (
                2.0 * (exchanges.exchange_fees[opportunity.selling_exchange] + exchanges.exchange_fees[opportunity.buying_exchange]))))
        if (entry_spread > target_entry_spread) & ((entry_spread - profit_target - (
                2.0 * (
                exchanges.exchange_fees[opportunity.selling_exchange] + exchanges.exchange_fees[opportunity.buying_exchange]))) > 1.00) & (
                opportunity.selling_exchange != opportunity.buying_exchange):
            entry_volume = float(opportunity.trade_volume)
            logger.run('💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰')
            logger.run('Entrando na operação com spread: %f e volume: %f BTC (0.5x do volume do menor book)' % (
                entry_spread, entry_volume))
            logger.run('💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰')
            # creating traded spread to calculate exit_spread_target
            traded_spread = entry_spread
            current_trade = opportunity.simulate_trade(logger, attempt)

            temp_balance = current_trade.usd_buy + current_trade.usd_sell
            in_trade = True
        else:
            logger.run(
                '🏃 ‍Jumping - Current Spread %f < Target Spread %f. ###### Selling %s X Buying %s ###### 🏃' %
                (opportunity.spread, target_entry_spread,
                 opportunity.selling_exchange.upper(),
                 opportunity.buying_exchange.upper()))

    else:
        logger.run('Trying to close the transaction...')

        actual_sell_price_bought_exchange = book_df[book_df['Exchange'] == current_trade.buying_exchange]['Bid Price'].values[0]
        actual_buy_price_sold_exchange = book_df[book_df['Exchange'] == current_trade.buying_exchange]['Ask Price'].values[0]
        # manual calculating spread because actual spread is considering buy again what was already bought...
        real_actual_spread = actual_buy_price_sold_exchange / actual_sell_price_bought_exchange
        logger.run('Real Spread: %f' % real_actual_spread)

        actual_spread = spread_of(opportunity.selling_exchange, opportunity.buying_exchange) - 1
        # logger.run('ACTUAL SPREAD %f' % actual_spread)
        exit_spread_target = traded_spread - profit_target - (
                2.0 * (exchanges.exchange_fees[current_trade.buying_exchange] + (exchanges.exchange_fees[current_trade.selling_exchange])))
        logger.run('Spread de entrada - spread atual: %f' % (entry_spread - real_actual_spread))
        logger.run('Spread target para sair: %f' % exit_spread_target)
        if exit_spread_target >= real_actual_spread:
            # TODO: Considerar a taxa e volume inicial
            profit = temp_balance + ((actual_sell_price_bought_exchange * current_trade.trade_volume) - (
                    actual_buy_price_sold_exchange * current_trade.trade_volume))
            actual_balance += profit
            logger.run('\n*** Concluindo transação ***\n')
            logger.run(' spread de entrada %f \n spread de saida: %f \n lucro US$ %f' % (
                opportunity.spread, actual_spread, profit))

            # checking available exit volume:
            if opportunity.trade_volume < current_trade.trade_volume:
                logger.run(
                    '🚨 Atenção: volume de saída menor do que o de entrada! Entrada: %f BTC e saída: %f BTC 🚨' % (
                        current_trade.trade_volume, opportunity.trade_volume))

            logger.run('🥂 Current balance: US$ %f 🥂' % actual_balance)
            in_trade = False

    time.sleep(1)
