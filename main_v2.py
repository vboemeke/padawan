# coding=utf-8

# import ccxt.async_support as ccxt
import ccxt
from fetch_infos import fetch_data
import time
import pandas as pd

dict = dict()
list_of_books = []
target_entry_spread = 1.0002
target_exit_spread = 0.00003
in_trade = False
start_balance = float(0)
temp_balance = float(0)
greatest_spread = float(0)

def generate_dataframe():
    dict = {}
    list_of_books = []
    #todo increase exchange list (validate symbols 'BTC/USC' doesn't work on other exchanges but we need to check if is the same coin - ex. Dolar vs. Stable Dolar)
    exchange_list = ['kraken', 'bittrex', 'bitmex']
    for i in exchange_list:
        book = {}
        book = fetch_data(i)
        if len(book) != 0 :
            dict[i] = book
            list_of_books.append([i,book['bids'][1][0],book['bids'][1][1],book['asks'][1][0],book['asks'][1][1]])
    book_dataframe = pd.DataFrame(list_of_books, columns = ['Exchange', 'Bid Price', 'Bid Volume', 'Ask Price', 'Ask Volume'])
    return book_dataframe

def calculate_spread(book_dataframe):
    max_bid_price = book_dataframe['Bid Price'].max()
    min_ask_price = book_dataframe['Ask Price'].min()
    #todo deal with more than one exchanges with exactly same price or volume
        #ValueError: The truth value of an array with more than one element is ambiguous
    volume_max_bid = float(book_dataframe[book_dataframe['Bid Price'] == max_bid_price]['Bid Volume'])
    volume_min_ask = float(book_dataframe[book_dataframe['Ask Price'] == min_ask_price]['Ask Volume'])
    print('volume_bid: %f e volume_ask: %f' % (volume_max_bid, volume_min_ask))
    buying_exchange = book_dataframe[book_dataframe['Ask Price'] == min_ask_price]['Exchange'].values.any()
    selling_exchange = book_dataframe[book_dataframe['Bid Price'] == max_bid_price]['Exchange'].values.any()
    if (volume_max_bid > volume_min_ask):
        volume_to_trade = float(0.5*volume_min_ask)
    else:
        volume_to_trade = float(0.5*volume_max_bid)
    spread = float(max_bid_price/min_ask_price)
    return [spread,max_bid_price,min_ask_price, volume_to_trade, selling_exchange, buying_exchange]

def simulate_trade(list_infos):
    usd_buy = -(list_infos[2]*list_infos[3])
    usd_sell = (list_infos[1]*list_infos[3])
    buying_exchange = list_infos[5]
    selling_exchange = list_infos[4]
    print('Comprado por (US$ %s): %s na: %s' % (list_infos[2],usd_buy, buying_exchange))
    print('Vendido por (US$ %s): %s na: %s' % (list_infos[1],usd_sell, selling_exchange))
    return float(usd_buy+usd_sell)

while 1 < 2:
    book_2 = generate_dataframe()
    spread = calculate_spread(book_2)

    if in_trade == False:
        if spread[0] > target_entry_spread:
            print(float(spread[3]))
            entry_spread = float(spread[0])
            entry_volume = float(spread[3])
            if entry_spread > greatest_spread:
                greatest_spread = entry_spread
            print('==== \n Maior spread da análise = %f \n====' % greatest_spread)
            print('Entrando na operação com spread: %f e volume: %f BTC (0.5x do volume do menor book)' % (entry_spread, entry_volume))
            temp_balance = simulate_trade(spread)
            in_trade = True
        else:
            print('target < %f' % target_entry_spread)
        # print('spread', spread)
        # print(book_2)
    else:
        # while in_trade == True:
        #     #trying to close the arbitrage. Focus on traded exchanges
        #     #create method to search closing opportunities... on traded exchanges
        #     print('')
        if (entry_spread-spread[0]) >= target_exit_spread:
            print('Saindo da operação no spread %f, sendo lucro: %f' % (spread[0], entry_spread-spread[0]))
            #todo to exit you need monitor traded exchanges - buy where sold and sell where bought!
            temp_balance += temp_balance + simulate_trade(spread)
            in_trade = False
    time.sleep(2)
