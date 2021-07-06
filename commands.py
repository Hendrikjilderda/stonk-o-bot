import json, csv
import pandas as pd
from datetime import date

from Discord_connection import automatic_daily_report


import yfinance as yf

user_list = []
ticker_list = ["tsla", "aapl", "amc", "sens"]
report = []

week_days = {"monday": 0, "tuesday": 1, "wednesday":2,
             "thursday": 3, "friday": 4,
             "yesterday": (date.today().weekday()-1)}


def get_current(ticker):
    # can be used to see all info that is available
    # output = ticker.info
    # print(output)

    # print(output, '\n \n')
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
                     "website": ticker.info["website"]}

    return wanted_output


def get_fincancials(ticker):        # fixme
    return ticker.financials


def get_cashflow(ticker):           # fixme
    return ticker.cashflow


def get_history(ticker, period):
    return ticker.history(period=period)


def get_dividend(ticker):
    return ticker.dividends


def get_isin(ticker):
    return ticker.isin


def get_next_event(ticker):
    return ticker.calendar


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


def get_daily_report(weekday):
        return f'./daily-reports/report {week_days[weekday]}.xlsx'


def get_ticker_list():
    return ticker_list


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
