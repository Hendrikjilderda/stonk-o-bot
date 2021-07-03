import json

import yfinance as yf

user_list = []
ticker_list = ["tsla", "aapl", "amc"]


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
    report = {"ticker": []}
    for x in ticker_list:
        ticker = yf.Ticker(f"{x}")
        report["ticker"].append({
            "name": ticker.info["shortName"],
            "previous close": ticker.info["previousClose"],
            "day high": ticker.info["dayHigh"],
            "day low": ticker.info["dayLow"]
        })

    with open("daily_report.txt", 'w') as f:
        json.dump(daily_report, f, indent=4)
    print("finished daily report")


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
