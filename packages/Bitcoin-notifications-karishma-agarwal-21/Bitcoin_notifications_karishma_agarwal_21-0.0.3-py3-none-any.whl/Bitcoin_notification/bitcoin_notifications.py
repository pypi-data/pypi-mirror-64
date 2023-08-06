import requests
import time
from datetime import datetime

BITCOIN_PRICE_THRESHOLD = 10000
BITCOIN_API_URL = 'https://api.coindesk.com/v1/bpi/currentprice.json'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/eA_ZN_ZsBcX4FZmsgzdc_7_yppNdLzDCWsJaoAz65Ci'

def get_latest_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    formatted_value = response_json['bpi']['USD']['rate']
    formatted_value = float(formatted_value.replace(",",""))
    print(formatted_value)
    return formatted_value

def post_ifttt_webhook(event, value):
    data = {'value1': value}  # The payload that will be sent to IFTTT service
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)  # Inserts our desired event
    requests.post(ifttt_event_url, json=data)  # Sends a HTTP POST request to the webhook URL

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')  # Formats the date into a string: '24.02.2018 15:09'
        price = bitcoin_price['price']
        # <b> (bold) tag creates bolded text
        row = '{}: $<b>{}</b>'.format(date, price)  # 24.02.2018 15:09: $<b>10123.4</b>
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    return '<br>'.join(rows)  # Join the rows delimited by <br> tag: row1<br>row2<br>row3

def main():
    bitcoin_history = []
    while True:
        price = get_latest_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Send an emergency notification
        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # Send a Telegram notification
        if len(bitcoin_history) == 5:  # Once we have 5 items in our bitcoin_history send an update
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
            # Reset the history
            bitcoin_history = []

        time.sleep(0.1 * 60)  # Sleep for 5 minutes

if __name__ == '__main__':
    main()
