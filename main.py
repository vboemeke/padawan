# coding=utf-8

from fetch_infos import fetch_exchange_data
import time
import pandas as pd

target_entry_spread = 1.0015
target_exit_spread = 0.0004
in_trade = False
start_balance = float(0)
actual_balance = float(0)
temp_balance = float(0)
greatest_spread = float(0)
global book_df
fees = {'bitmex': 0.0020, 'bittrex': 0.0020, 'kraken': 0.0025}

print('Saldo inicial: US$ %f' % actual_balance)

def generate_dataframe():
    exchange_list = ['kraken', 'bittrex', 'bitmex']
    dict = {}
    list_of_books = []

    # todo increase exchange list (validate symbols 'BTC/USC' doesn't work on other exchanges
    # but we need to check if is the same coin - ex. Dolar vs. Stable Dolar)

    for exchange_name in exchange_list:
        exchange_data = fetch_exchange_data(exchange_name)
        if exchange_data != {}:
            dict[exchange_name] = exchange_data
            list_of_books.append(
                [exchange_name, exchange_data['bids'][0][0], exchange_data['bids'][0][1], exchange_data['asks'][0][0],
                 exchange_data['asks'][0][1]])
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
    return book_df.loc[(book_df['Ask Price'] == min_ask_price()) & (book_df['Ask Volume'] == min_ask_volume())][
        'Exchange'].values[0]


def best_opportunity():
    print('volume_bid: %f e volume_ask: %f' % (max_bid_volume(), min_ask_volume()))

    buying_exchange = best_ask_exchange_price()
    selling_exchange = best_bid_exchange_price()

    spread = float(max_bid_price() / min_ask_price())
    return [spread,
            max_bid_price(),
            min_ask_price(),
            trade_volume(max_bid_volume(), min_ask_volume()),
            selling_exchange,
            buying_exchange]


def trade_volume(bid, ask):
    return float(0.5 * ask) if bid > ask else float(0.5 * bid)


def simulate_trade(list_infos):
    usd_buy = -(list_infos[2] * list_infos[3])
    usd_sell = (list_infos[1] * list_infos[3])
    buying_exchange = list_infos[5]
    selling_exchange = list_infos[4]
    print('Comprou: \n Volume: %s \n Cotação: %s \n Custo da Operação: %s \n Exchange: %s' % (
        list_infos[3], list_infos[2], usd_buy, buying_exchange))
    print('Vendeu: \n Volume: %s \n Cotação: %s \n Receita da Operação: %s \nExchange: %s' % (
        list_infos[3], list_infos[1], usd_sell, selling_exchange))
    #TODO: fix volume information. repeating same value!
    return ('buying_exchange', buying_exchange, usd_buy, list_infos[3]), ('selling_exchange', selling_exchange, usd_sell, list_infos[3])


def spread_of(selling_exchange, buying_exchange):
    actual_book_df = generate_dataframe()
    selling_exchange_actual_bid = actual_book_df[actual_book_df['Exchange'] == selling_exchange].values[0][1]
    buying_exchange_actual_sell = actual_book_df[actual_book_df['Exchange'] == buying_exchange].values[0][3]

    return float(selling_exchange_actual_bid) / float(buying_exchange_actual_sell)


while 1 < 2:
    book_df = generate_dataframe()
    opportunity = best_opportunity()

    selling_exchange = opportunity[4]
    buying_exchange = opportunity[5]

    #TODO: greatest spread should be here so we can always monitor hightes values, even when traded!

    if not in_trade:
        if opportunity[0] > target_entry_spread:
            entry_spread = float(opportunity[0])
            entry_volume = float(opportunity[3])
            if entry_spread > greatest_spread:
                print('*** Novo Record de Spread ***')
                greatest_spread = entry_spread
            print('==== \n Maior spread da análise = %f \n====' % greatest_spread)
            print('Entrando na operação com spread: %f e volume: %f BTC (0.5x do volume do menor book)' % (
                entry_spread, entry_volume))

            operation = simulate_trade(opportunity)
            temp_balance = operation[0][2] + operation[1][2]
            in_trade = True
        else:
            print('pulando - atual %f < target %f' % (opportunity[0], target_entry_spread))
    else:
        print('Trying to close the transaction...')

        actual_sell_price_bought_exchange = book_df[book_df['Exchange'] == operation[0][1]]['Bid Price'].values[0]
        actual_buy_price_sold_exchange = book_df[book_df['Exchange'] == operation[0][1]]['Ask Price'].values[0]
        # manual calculating spread because actual spread is considering buy again what was already bought...
        real_actual_spread = actual_buy_price_sold_exchange/actual_sell_price_bought_exchange
        print('Real spread: %f' % real_actual_spread)

        actual_spread = spread_of(selling_exchange, buying_exchange) - 1
        # print('ACTUAL SPREAD %f' % actual_spread)
        # if target_exit_spread >= actual_spread:
        delta_spread = (entry_spread - real_actual_spread)
        print('Spread de entrada - spread atual: %f' % delta_spread)
        if target_exit_spread <= (entry_spread - real_actual_spread):
            # TODO: Considerar a taxa e volume inicial
            profit = temp_balance + ((actual_sell_price_bought_exchange*operation[0][3]) - (actual_buy_price_sold_exchange*operation[0][3]))
            actual_balance += profit
            # profit = (actual_spread - opportunity[0]1) * opportunity[3]
            print('\n*** Concluindo transação ***\n')
            print(' spread de entrada %f \n spread de saida: %f \n lucro US$ %f' % (opportunity[0], actual_spread, profit))
            print('Saldo atual: US$ %f' % actual_balance)
            in_trade = False

    time.sleep(2)
