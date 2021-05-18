import math
import os
import time

import numpy
import tinvest
from tinvest import CandleResolution


token = os.environ['TINKOFF_INVEST_TOKEN']
client = tinvest.SyncClient(token)


def calculate_risk_and_expect_growth_in_month(ticker):
    resp = make_request(client.get_market_search_by_ticker, ticker)
    instruments = resp.payload.instruments

    if len(instruments) == 0:
        return None

    figi = instruments[0].figi

    candlesHistoryInMonth = make_request(client.get_market_candles,
                                         figi,
                                         '2019-01-01T00:00:00.00+00:00',
                                         '2021-04-30T23:59:59.00+00:00',
                                         CandleResolution.month)

    prices = []
    for candle in candlesHistoryInMonth.payload.candles:
        prices.append((candle.h + candle.l) / 2)

    growths = []
    for i in range(0, len(prices) - 1):
        growths.append(math.log(prices[i + 1] / prices[i]))

    expect_growth = numpy.mean(growths)
    risk = numpy.std(growths)

    return expect_growth * 100, risk * 100  # To percent


def make_request(request, *args):
    try:
        return request(*args)
    except tinvest.TooManyRequestsError as e:
        print('Too many request, wait 5 minute')
        time.sleep(60 * 5 + 5)  # 5 min 5 sec
        return request(tuple(args))
