import json
import os
import time
import urllib.request
from collections import namedtuple
from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)
load_dotenv()
TickerInfo = namedtuple('TickerInfo', ['currency', 'logo_url', 'name', 'price', 'rank',
                                       'one_day_price_change', 'one_day_price_change_pct',
                                       'thirty_day_price_change', 'thirty_day_price_change_pct'])


def get_request_url(api_key, tickers):
    return f"https://api.nomics.com/v1/currencies/ticker?key={api_key}&exchange=binance&ids={tickers}&interval=1d,30d&convert=USD&"


def format_floats(num_to_format):
    return round(float(num_to_format), 2)


def make_ticker_info(ticker_info):
    return TickerInfo(currency=ticker_info['currency'],
                      logo_url=ticker_info['logo_url'],
                      name=ticker_info['name'], price=format_floats(ticker_info['price']), rank=ticker_info['rank'],
                      one_day_price_change=format_floats(ticker_info['1d']['price_change']),
                      thirty_day_price_change=format_floats(ticker_info['30d']['price_change']),
                      one_day_price_change_pct=ticker_info['1d']['price_change_pct'],
                      thirty_day_price_change_pct=ticker_info['30d']['price_change_pct'])


@app.route('/')
def home():
    API_KEY = os.getenv("API_KEY")
    CURRENCY = "BTC"
    NUM_CURRENCIES = len(CURRENCY.split(','))
    FONT = "Trebuchet MS"

    url = get_request_url(API_KEY, CURRENCY)
    try:
        request_response = json.loads(urllib.request.urlopen(url).read())[NUM_CURRENCIES - 1]
    except urllib.error.HTTPError:
        time.sleep(5)
        request_response = json.loads(urllib.request.urlopen(url).read())[NUM_CURRENCIES - 1]
    ticker_info = make_ticker_info(request_response)
    return f"""
        <h1 style="font-family:{FONT}"> Currency : {ticker_info.currency}  <img src="{ticker_info.logo_url}" style="width:30px;height:30px;"><h1/>
        <h1 style="font-family:{FONT}" > Last Price : {ticker_info.price} <h1/>
        <h1 style="font-family:{FONT}" > 1D Price Change : {ticker_info.one_day_price_change} <h1/>"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
