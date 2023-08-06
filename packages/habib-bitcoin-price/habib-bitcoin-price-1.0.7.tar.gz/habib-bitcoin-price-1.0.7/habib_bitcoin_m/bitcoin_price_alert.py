# -*- coding: utf-8 -*-

import requests
import time
from datetime import datetime
import argparse


def get_latest_bitcoin_price():
    api_req = requests.get(api_url).json()

    # Convert the price to a floating point number

    api_rate = float(api_req['bpi']['USD']['rate'].replace(',', ''))
    return api_rate


def post_ifttt_webhook(event, value):

    # The payload that will be sent to IFTTT service

    data = {'value1': value}

    # Inserts our desired event

    ifttt_event_url = ifttt_webhook_url.format(event)

    # Sends a HTTP POST request to the webhook URL

    requests.post(ifttt_event_url, json=data)


def bitcoin_price_list(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:

        # Formats the date into a string: '24.02.2018 15:09'

        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']

        # 24.02.2018 15:09: $<b>10123.4</b>

        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3

    return '<br>'.join(rows)


def main(interval, upperlimit):

    # print (interval, upperlimit)

    price_list = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        price_list.append({'date': date, 'price': price})

        # Send an emergency notification

        if price < upperlimit:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # Send a Telegram notification
        # Once we have 5 items in our price_list send an update

        if len(price_list) == 5:
            post_ifttt_webhook('bitcoin_price_update',
                               bitcoin_price_list(price_list))

            # Reset the price list

            price_list = []

        # (setting the time interval from CLI by default it is 1 minutes)

        time.sleep(interval * 60)


def arg_main():
    parser = \
        argparse.ArgumentParser(description=' Bitcoin price notification alert'
                                )

    # adding argument for notification

    parser.add_argument('--d', default=['Y'], type=str, nargs=1,
                        help=' Enter (Yes/No) to run the bitcoin notification'
                        )

    # adding argument for interval

    parser.add_argument(
        '--i',
        '--interval',
        default=[1],
        type=float,
        nargs=1,
        help=' Time interval for updated price \
                in minutes in this (0.1,1,2)  format')

    # adding argument for theroshold

    parser.add_argument(
        '--u',
        '--Upper threshold',
        default=[10000],
        type=int,
        nargs=1,
        help=' Set the upper threshold limit in USD for notification',
        )

    args = parser.parse_args()
    des = args.d[0]
    if des == 'Y':
        main(args.i[0], args.u[0])
    else:
        print('No notification')


api_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
ifttt_webhook_url = \
    'https://maker.ifttt.com/trigger/{}/with/key/pWH5sS7jvzihh5y5RdVdYt2-IxwcEPkDzMKJs-KDaM3'

if __name__ == '__main__':
    arg_main()
