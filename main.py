from fetch_infos import fetch_data
import time
import pandas as pd

target_entry_spread = 1.0002
target_exit_spread = 0.00003
in_trade = False
start_balance = float(0)
temp_balance = float(0)
greatest_spread = float(0)
global book_df


def generate_dataframe(**kwargs):
    exchange_list = ['kraken', 'bittrex', 'bitmex']
    # if (len(exchanges) == 0):
    #     exchange_list = ['kraken', 'bittrex', 'bitmex']
    # else:
    #     exchange_list = exchagens

    dict = {}
    list_of_books = []

    # todo increase exchange list (validate symbols 'BTC/USC' doesn't work on other exchanges
    # but we need to check if is the same coin - ex. Dolar vs. Stable Dolar)

    for i in exchange_list:
        book = fetch_data(i)
        if len(book) != 0:
            dict[i] = book
            list_of_books.append([i, book['bids'][1][0], book['bids'][1][1], book['asks'][1][0], book['asks'][1][1]])
    return pd.DataFrame(list_of_books, columns=['Exchange', 'Bid Price', 'Bid Volume', 'Ask Price', 'Ask Volume'])


def max_bid_price():
    return book_df['Bid Price'].max()


def min_ask_price():
    return book_df['Ask Price'].min()


def max_bid_volume():
    return book_df[book_df['Bid Price'] == max_bid_price()]['Bid Volume'].max()


def min_ask_volume():
    return book_df[book_df['Ask Price'] == min_ask_price()]['Ask Volume'].max()


def calculate_spread():
    # todo deal with more than one exchanges with exactly same price or volume
    # ValueError: The truth value of an array with more than one element is ambiguous
    print('volume_bid: %f e volume_ask: %f' % (max_bid_volume(), min_ask_volume()))
    print(book_df)

    buying_exchange = best_ask_exchange_price()
    selling_exchange = best_bid_exchange_price()

    print(buying_exchange)
    print(selling_exchange)

    spread = float(max_bid_price() / min_ask_price())
    return [spread, max_bid_price(),
            min_ask_price(),
            trade_volume(max_bid_volume(), min_ask_volume()),
            selling_exchange,
            buying_exchange]


def simulate_trade(list_infos):
    usd_buy = -(list_infos[2] * list_infos[3])
    usd_sell = (list_infos[1] * list_infos[3])
    buying_exchange = list_infos[5]
    selling_exchange = list_infos[4]
    print('Comprado por (US$ %s): %s na: %s' % (list_infos[2], usd_buy, buying_exchange))
    print('Vendido por (US$ %s): %s na: %s' % (list_infos[1], usd_sell, selling_exchange))
    return ('buying_exchange', buying_exchange, usd_buy), ('selling_exchange', selling_exchange, usd_sell)


def best_bid_exchange_price():
    return book_df.loc[(book_df['Bid Price'] == max_bid_price()) & (book_df['Bid Volume'] == max_bid_volume())][
        'Exchange']


def best_ask_exchange_price():
    return book_df.loc[(book_df['Ask Price'] == min_ask_price()) & (book_df['Ask Volume'] == min_ask_volume())][
        'Exchange']


def trade_volume(bid, ask):
    if bid > ask: return float(0.5 * ask)
    return float(0.5 * bid)


while 1 < 2:
    book_df = generate_dataframe()
    spread = calculate_spread()

    if not in_trade:
        if spread[0] > target_entry_spread:
            print(float(spread[3]))
            entry_spread = float(spread[0])
            entry_volume = float(spread[3])
            if entry_spread > greatest_spread:
                greatest_spread = entry_spread
            print('==== \n Maior spread da análise = %f \n====' % greatest_spread)
            print('Entrando na operação com spread: %f e volume: %f BTC (0.5x do volume do menor book)' % (
                entry_spread, entry_volume))
            # buying_exchange = list_infos[5]
            # selling_exchange = list_infos[4]

            operation = simulate_trade(spread)
            temp_balance = operation[0][2] + operation[1][2]
            in_trade = True
        else:
            print('target < %f' % target_entry_spread)
        # print('spread', spread)
        # print(book_2)
    else:
        print('Trying to close the transaction...')
    # while in_trade == True:
    #     #trying to close the arbitrage. Focus on traded exchanges
    #     #create method to search closing opportunities... on traded exchanges
    #     print('')
    # actual_traded_spread = (book2[book2[selling_exchange]]['Bid Price'])/(book2[book2[buying_exchange]]['Ask Price'])
    # if (entry_spread-actual_traded_spread) >= target_exit_spread:
    #     print('Saindo da operação no spread %f, sendo lucro: %f' % (actual_traded_spread, entry_spread-actual_traded_spread))
    #     #todo to exit you need monitor traded exchanges - buy where sold and sell where bought!
    #     temp_balance += temp_balance + simulate_trade(spread)
    #     print('Saldo atual: %f' % temp_balance)
    #     in_trade = False
    time.sleep(2)
