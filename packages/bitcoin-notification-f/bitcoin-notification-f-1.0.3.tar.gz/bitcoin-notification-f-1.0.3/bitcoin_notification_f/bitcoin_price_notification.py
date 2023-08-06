#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import time
from datetime import datetime
import argparse

bitcoin_api_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
IFTTT_URL = \
    'https://maker.ifttt.com/trigger/{}/with/key/finWCJgtcfRqC0Nae5iwiu7jfjwOFCJL_-nvRHuZX8-'


def bitcoin_price():

    response_recieved = requests.get(bitcoin_api_url)
    response_recieved = response_recieved.json()

    # Convert the price to a floating point number

    key_value = float(response_recieved['bpi']['USD']['rate'].replace(',', ''))
    return key_value


def notification(event, value):

    # The data that will be sent to IFTTT servive

    data = {'value1': value}

    # inserts our desired event

    ifttt_event_url = IFTTT_URL.format(event)

    # Sends a HTTP POST request to webhook url

    requests.post(ifttt_event_url, json=data)


def format_bitcoin_history(list_price_of_bitcoin):
    rows = []
    for bitcoin_price in list_price_of_bitcoin:

        # Formats the date into a string: '2018-02-23 15:09'

        date = bitcoin_price['date'].strftime('%Y-%m-%d %H:%M')
        price = bitcoin_price['price']

        # <b> (bold) tag creates bolded text
        # 24.02.2018 15:09: $<b>10123.4</b>

        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3

    return '<br>'.join(rows)


def main(interval, upper_threshold):

    list_price_of_bitcoin = []

    while True:
        price = bitcoin_price()
        date = datetime.now()
        list_price_of_bitcoin.append({'date': date, 'price': price})

        # Send an emergency notification

        if price >= upper_threshold:
            notification('bitcoin_price_emergency', price)

        # Send a Telegram notification
        # Once we have 5 items in our list_price_of_bitcoin send an update

        if len(list_price_of_bitcoin) == 5:
            notification('bitcoin_price_update',
                         format_bitcoin_history(list_price_of_bitcoin))

            # Reset the history

            list_price_of_bitcoin = []

        if 5000 < price < 8000:
            notification('bitcoin_gmail_notification', price)

        # Sleep for 5 minutes
        # (For testing purposes you can set it to a lower number)

        time.sleep(interval * 60)


def cli():

    parser = argparse.ArgumentParser(description=' Bitcoin Notification Alert ')

    # argument for notification

    parser.add_argument(
        '--d',
        default=['Yes'],
        type=str,
        nargs=1,
        metavar='decision',
        help=' Enter (Yes/No) - Yes will run the program',
        )

    # argument for interval

    parser.add_argument(
        '--i',
        metavar='interval',
        default=[0.1],
        type=float,
        nargs=1,
        help=' Enter time interval',
        )

    # argument for thershold

    parser.add_argument(
        '--u',
        metavar='upper threshold',
        default=[10000],
        type=int,
        nargs=1,
        help=' Set upper threshold limit in USD for notification',
        )

    args = parser.parse_args()

    decision = args.d[0]
    if decision == 'Yes':
        main(args.i[0], args.u[0])
    else:
        print('No Notification')


if __name__ == '__main__':
    cli()
