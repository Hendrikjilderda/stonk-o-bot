import json, csv
import pandas as pd
from datetime import date

from colorthief import ColorThief
import requests


import yfinance as yf

user_list = []
ticker_list = ["tsla", "aapl", "amc", "sens"]
report = []

week_days = {"monday": 0, "tuesday": 1, "wednesday":2,
             "thursday": 3, "friday": 4,
             "yesterday": (date.today().weekday()-1)}


def get_current(input_ticker):
    ticker = yf.Ticker(input_ticker)

    wanted_output = {"ticker": ticker,
                     "name": ticker.info["shortName"],
                     "short summary": ticker.info["longBusinessSummary"],
                     "marketCap":  ticker.info["marketCap"],
                     "previous close": ticker.info["previousClose"],
                     "day low": ticker.info["dayLow"],
                     "day high": ticker.info["dayHigh"],
                     "yearly high": ticker.info["fiftyTwoWeekHigh"],
                     "yearly low": ticker.info["fiftyTwoWeekLow"],
                     "logo": ticker.info["logo_url"],
                     "website": ticker.info["website"]
                     }

    image = ColorThief(requests.get(wanted_output['logo'], stream=True).raw)
    dominant_color = image.get_color(quality=1)
    # print(dominant_color)
    embed = discord.Embed(
        title=f"{wanted_output['name']}",
        description=f"{wanted_output['short summary']}",
        colour=discord.Colour.from_rgb(dominant_color[0], dominant_color[1], dominant_color[2])
        # fIXME niet heel accuraat atm
    )

    embed.set_thumbnail(url=wanted_output['logo'])
    embed.set_footer(text='data acquired from Yahoo Finance')

    embed.add_field(name='marketCap', value=f"${'{:,}'.format(wanted_output['marketCap'])}", inline=True)
    embed.add_field(name='previous close', value=f"${wanted_output['previous close']}", inline=True)
    embed.add_field(name='day high', value=f"${wanted_output['day high']}", inline=True)
    embed.add_field(name='day low', value=f"${wanted_output['day low']}", inline=True)
    embed.add_field(name='yearly high', value=f"${wanted_output['yearly high']}", inline=True)
    embed.add_field(name='yearly low', value=f"${wanted_output['yearly low']}", inline=True)
    embed.add_field(name='website', value=wanted_output['website'], inline=False)

    return embed


def get_fincancials(input_ticker):        # fixme
    ticker = yf.Ticker(input_ticker)
    return ticker.financials


def get_cashflow(input_ticker):           # fixme
    ticker = yf.Ticker(input_ticker)
    return ticker.cashflow


def get_history(input_ticker, period):
    ticker = yf.Ticker(input_ticker)
    return ticker.history(period=period)


def get_dividend(input_ticker):
    ticker = yf.Ticker(input_ticker)
    temp = ticker.dividends
    return temp


def get_isin(input_ticker):
    ticker = yf.Ticker(input_ticker)
    return ticker.isin


def get_next_event(input_ticker):
    ticker = yf.Ticker(input_ticker)
    temp = ticker.calendar
    return temp


def daily_report():
    global ticker_list

    global report
    for x in ticker_list:
        ticker = yf.Ticker(f"{x}")
        report.append({
            'name': ticker.info["shortName"],
            'previous close': ticker.info["previousClose"],
            'day high': ticker.info["dayHigh"],
            'day low': ticker.info["dayLow"]

            })

    df = pd.DataFrame(report)
    df.to_excel(f'./daily-reports/report {date.today().weekday()}.xlsx', index=False)

    print("[info] daily report updated")
    automatic_daily_report(report, ticker_list)

def get_daily_report_file(weekday):
    return f'./daily-reports/report {week_days[weekday.lower()]}.xlsx'


def get_ticker_list():
    pretty_list = "Stocks on the watch list are: "
    for element in ticker_list[:-1]:
        pretty_list += f"${element.upper()}, "
    pretty_list += f"${ticker_list[-1].upper()}"
    print(pretty_list)
    return pretty_list


def add_daily_report(ticker):
    if ticker not in ticker_list:
        ticker_list.append(ticker)
        print(ticker_list)
        return True
    else:
        return False


def remove_daily_report(ticker):
    if ticker in ticker_list:
        ticker_list.remove(ticker)
        return True
    else:
        return False


def join_daily_report(username):
    if username not in user_list:
        user_list.append(username)
        return True
    else:
        return False


def leave_daily_report(username):
    if username in user_list:
        user_list.remove(username)
        return f"{username} is removed from subscriber list"
    else:
        return f"{username} not on subscriber list"

