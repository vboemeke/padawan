# coding=utf-8

import time

import pandas as pd

import exchanges.fetch_infos as exchanges
from db.database import Database
from log.logger import Logger

target_entry_spread = 1.0025
profit_target = 0.00001
in_trade = False
start_balance = 0.00
actual_balance = 0.00
temp_balance = 0.00
greatest_spread = 0.00
global book_df
db = Database()


def generate_dataframe(exchange_list):
    dict = {}
    list_of_books = []

    # TODO increase exchange list (validate symbols 'BTC/USC' doesn't work on other exchanges
    # but we need to check if is the same coin - ex. Dolar vs. Stable Dolar)

    for exchange_name in exchange_list:
        exchange_data = exchanges.fetch_exchange_data(exchange_name)
        if exchange_data != {}:
            dict[exchange_name] = exchange_data

            max_bid_price = exchange_data['bids'][0][0]
            max_bid_volume = exchange_data['bids'][0][1]
            min_ask_price = exchange_data['asks'][0][0]
            min_ask_volume = exchange_data['asks'][0][1]

            db.add_bid_ask_to_db(exchange_name, max_bid_price, max_bid_volume, min_ask_price, min_ask_volume, attempt)
            list_of_books.append([exchange_name, max_bid_price, max_bid_volume, min_ask_price, min_ask_volume])

    return pd.DataFrame(list_of_books, columns=['Exchange', 'Bid Price', 'Bid Volume', 'Ask Price', 'Ask Volume'])


def max_bid_price():
    return book_df['Bid Price'].max()


def min_ask_price():
    return book_df['Ask Price'].min()


# TODO: I need to validate when two exchanges contains the same max_bid_price
def max_bid_volume():
    return book_df[book_df['Bid Price'] == max_bid_price()]['Bid Volume'].max()


# TODO: I need to validate when two exchanges contains the same min_ask_price
def min_ask_volume():
    return book_df[book_df['Ask Price'] == min_ask_price()]['Ask Volume'].max()


def best_bid_exchange_price():
    return book_df.loc[(book_df['Bid Price'] == max_bid_price()) & (book_df['Bid Volume'] == max_bid_volume())][
        'Exchange'].values[0]


def best_ask_exchange_price():
    # need to check why: "IndexError: index 0 is out of bounds for axis 0 with size 0"
    # volume_bid: nan e volume_ask: nan
    return book_df.loc[(book_df['Ask Price'] == min_ask_price()) & (book_df['Ask Volume'] == min_ask_volume())][
        'Exchange'].values[0]


def best_opportunity():
    buying_exchange = best_ask_exchange_price()
    selling_exchange = best_bid_exchange_price()

    spread = float(max_bid_price() / min_ask_price())
    return [spread,
            max_bid_price(),
            min_ask_price(),
            trade_volume(max_bid_volume(), min_ask_volume()),
            selling_exchange,
            buying_exchange,
            max_bid_volume(),
            min_ask_volume()]


def trade_volume(bid, ask):
    return float(0.5 * ask) if bid > ask else float(0.5 * bid)


def simulate_trade(list_infos):
    usd_buy = -(list_infos[2] * list_infos[3])
    usd_sell = (list_infos[1] * list_infos[3])
    buying_exchange = list_infos[5]
    selling_exchange = list_infos[4]
    logger.run('Comprou: \n Volume: %s \n Cotação: %s \n Custo da Operação: %s \n Exchange: %s' % (
        list_infos[3], list_infos[2], usd_buy, buying_exchange))
    logger.run('Vendeu: \n Volume: %s \n Cotação: %s \n Receita da Operação: %s \nExchange: %s' % (
        list_infos[3], list_infos[1], usd_sell, selling_exchange))
    # TODO: fix volume information. repeating same value!
    return ('buying_exchange', buying_exchange, usd_buy, list_infos[3]), (
        'selling_exchange', selling_exchange, usd_sell, list_infos[3])


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
        book_df = generate_dataframe([trade_info[0][1], trade_info[1][1]])

    # TODO generate trade_info data_frame

    opportunity = best_opportunity()

    logger.run('###############################')
    # logger.run('Volume Bid: %f e Volume Ask: %f' % (opportunity[6], opportunity[7]))

    selling_exchange = opportunity[4]
    buying_exchange = opportunity[5]

    entry_spread = float(opportunity[0])
    if entry_spread > greatest_spread:
        logger.run('📈 *** Novo Record de Spread *** 📈')
        greatest_spread = entry_spread

    logger.run('==== \n Maior spread da análise = %f \n====' % greatest_spread)

    if not in_trade:
        print('Spread atual - taxas e lucro:  %f' % (entry_spread - profit_target - (
                2.0 * (exchanges.exchange_fees[opportunity[4]] + exchanges.exchange_fees[opportunity[5]]))))
        if 0 == 0:
            if (entry_spread > target_entry_spread) & ((entry_spread - profit_target - (
                    2.0 * (
                    exchanges.exchange_fees[opportunity[4]] + exchanges.exchange_fees[opportunity[5]]))) > 1.00) & (
                    selling_exchange != buying_exchange):
                entry_volume = float(opportunity[3])
                logger.run('💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰')
                logger.run('Entrando na operação com spread: %f e volume: %f BTC (0.5x do volume do menor book)' % (
                    entry_spread, entry_volume))
                logger.run('💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰💰')
                # creating traded spread to calculate exit_spread_target
                traded_spread = entry_spread
                trade_info = simulate_trade(opportunity)
                temp_balance = trade_info[0][2] + trade_info[1][2]
                in_trade = True
        else:
            logger.run(
                '🏃 ‍Jumping - Current Spread %f < Target Spread %f. ###### Selling %s X Buying %s ###### 🏃' %
                (opportunity[0], target_entry_spread, selling_exchange.upper(), buying_exchange.upper()))

    else:
        logger.run('Trying to close the transaction...')

        actual_sell_price_bought_exchange = book_df[book_df['Exchange'] == trade_info[0][1]]['Bid Price'].values[0]
        actual_buy_price_sold_exchange = book_df[book_df['Exchange'] == trade_info[0][1]]['Ask Price'].values[0]
        # manual calculating spread because actual spread is considering buy again what was already bought...
        real_actual_spread = actual_buy_price_sold_exchange / actual_sell_price_bought_exchange
        logger.run('Real Spread: %f' % real_actual_spread)

        # TODO look at "spread_of()" - it's probably losing performance generating a new dataframe!
        actual_spread = spread_of(selling_exchange, buying_exchange) - 1
        # logger.run('ACTUAL SPREAD %f' % actual_spread)
        exit_spread_target = traded_spread - profit_target - (
                2.0 * (exchanges.exchange_fees[trade_info[0][1]] + (exchanges.exchange_fees[trade_info[1][1]])))
        logger.run('Spread de entrada - spread atual: %f' % (entry_spread - real_actual_spread))
        logger.run('Spread target para sair: %f' % exit_spread_target)
        if exit_spread_target >= real_actual_spread:
            # TODO: Considerar a taxa e volume inicial
            profit = temp_balance + ((actual_sell_price_bought_exchange * trade_info[0][3]) - (
                    actual_buy_price_sold_exchange * trade_info[0][3]))
            actual_balance += profit
            logger.run('\n*** Concluindo transação ***\n')
            logger.run(' spread de entrada %f \n spread de saida: %f \n lucro US$ %f' % (
                opportunity[0], actual_spread, profit))

            # checking available exit volume:
            if opportunity[3] < trade_info[0][3]:
                logger.run(
                    '🚨 Atenção: volume de saída menor do que o de entrada! Entrada: %f BTC e saída: %f BTC 🚨' % (
                        trade_info[0][3], opportunity[3]))

            logger.run('🥂 Current balance: US$ %f 🥂' % actual_balance)
            in_trade = False

    time.sleep(1)
