#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

import os
import re
import time
import click
from .lib import TWSELIB


CONTEXT_SETTINGS = {'help_option_names': ['-h', '--help']}
STOCK_CONFIG = os.path.expanduser('~/.config/twsecli/config')


def initial_stock_config(stock_config):
    if not os.path.isfile(stock_config):
        os.makedirs(os.path.dirname(stock_config))
        with open(stock_config, 'w', encoding='utf-8') as f:
            f.write('0050\n')
            f.write('0056\n')
    return stock_config


def alignment(s, space):
    base = len(s)
    count = len(re.findall('[a-zA-Z0-9]', s))
    space = space - (2 * base) + count  # space - ((base - count) * 2) - count
    s = s + (' ' * space)
    return s


def colored(s, color):
    if color == 'green':
        return '\033[1;32m' + s + '\033[m'
    if color == 'red':
        return '\033[1;31m' + s + '\033[m'


def print2terminal(stock_infos):
    if stock_infos:
        print("\n代號  商品          成交   漲跌    幅度    單量    總量   最高   最低   開盤   昨收")
        for stock in stock_infos:
            change = float(stock['z']) - float(stock['y'])
            change_p = change / float(stock['y'])
            stock_name = alignment(stock['n'], 11)
            stock_price = f"{float(stock['z']):>6.2f}"
            stock_change = f"{change:>+6.2f}"
            stock_change_p = f"{change_p:>+7.2%}"
            if change >= 0:
                stock_price = colored(stock_price, 'red')
                stock_change = colored(stock_change, 'red')
                stock_change_p = colored(stock_change_p, 'red')
            else:
                stock_price = colored(stock_price, 'green')
                stock_change = colored(stock_change, 'green')
                stock_change_p = colored(stock_change_p, 'green')
            stock_change_high = f"{float(stock['h']):>6.2f}"
            if float(stock['h']) - float(stock['y']) >= 0:
                stock_change_high = colored(stock_change_high, 'red')
            else:
                stock_change_high = colored(stock_change_high, 'red')
            stock_change_low = f"{float(stock['l']):>6.2f}"
            stock_change_origin = f"{float(stock['o']):>6.2f}"
            if float(stock['l']) - float(stock['y']) >= 0:
                stock_change_low = colored(stock_change_low, 'red')
                stock_change_origin = colored(stock_change_origin, 'red')
            else:
                stock_change_low = colored(stock_change_low, 'green')
                stock_change_origin = colored(stock_change_origin, 'green')
            print(f"{stock['c']:<5} {stock_name} {stock_price} {stock_change} {stock_change_p}"
                  f" {int(stock['tv']):>7,} {int(stock['v']):>7,} {stock_change_high} {stock_change_low}"
                  f" {stock_change_origin} {float(stock['y']):>6.2f}")
        else:
            print(f"\n資料時間: {stock['d']} {stock['t']}")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('symbol', nargs=-1)
@click.option('-n', '--interval',
    default=0,
    help='seconds to wait between updates, minimum 60s',
    type=int
)
@click.option('-c', '--config',
    default=initial_stock_config(STOCK_CONFIG),
    help='stock symbol config, default path ~/.config/twsecli/config',
    type=click.File('r')
)
def main(config, interval, symbol):
    """
    The twsecil prints real-time stock price.

    You can use stock symbol argument or stock symbol config to control what stock price you want to prints.
    However, if you don't input stock symbol argument, the twsecli will use stock symbol config as default.
    """
    stock_keys = []
    stock_symbols = []
    stock_interval = None

    # parse parameters
    if symbol:
        stock_symbols = list(symbol)
    else:
        click.echo('讀取設定檔: {}'.format(config.name))
        stock_symbols = [line.strip() for line in config if line.strip()]
    if interval:
        stock_interval = 60 if interval < 60 else interval

    # create object
    twse_lib = TWSELIB()
    for stock_symbol in stock_symbols:
        key = twse_lib.get_stock_key(stock_symbol)
        stock_keys.append(key)
    while True:
        stock_infos = twse_lib.get_stock_info(stock_keys)
        if stock_infos:
            if stock_interval:
                os.system('clear')
            print2terminal(stock_infos)
            if stock_interval:
                try:
                    print('資料更新頻率: {}s'.format(stock_interval))
                    time.sleep(stock_interval)
                except KeyboardInterrupt:
                    break
            else:
                break
        else:
            break

    # delete object
    del twse_lib


if __name__ == '__main__':
    main()
