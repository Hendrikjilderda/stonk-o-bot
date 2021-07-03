# fixme ticker kan nog beginnen met teken ipv letter

# get commands
from commands import *


periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]


def set_ticker(discord_input):
    temp = discord_input.split()
    if len(temp) == 1:
        command = discord_input

        if command[1:] == "info" or command[1:] == "financials" or command[1:] == "cashflow" or \
            command[1:] == "dividend" or command[1:] == "isin" or command[1:] == "events":
            return f"Too few or too many arguments. given: 1, should be 2."

        elif command[1:] == "history":
            return f"Too few or too many arguments. given: 1, should be 3."

        if command[1:] == "join":
            check = join_daily_report()     # FIXME username toevoegen somehow?
            if check:
                return f"FIXME added to the subscriber list"
            else:
                return f"FIXME  already on subscriber list"

        elif command[1:] == "list":
            watch_list = get_ticker_list()
            print(watch_list)
            return watch_list

        elif command[1:] == "leave":
            check = leave_daily_report()
            if check:
                return f"FIXME is removed from subscriber list"
            else:
                return f"FIXME not on subscriber list"

        # temp functie om daily report te simuleren
        elif command[1:] == "daily":
            if len(temp) != 1:
                print(f"[bot] Too few or too many arguments. given: {len(temp)}, should be 1.")
                return f"Too few or too many arguments. given: {len(temp)}, should be 1."
            else:
                daily_report()

    else:
        command = temp[0]
        input_ticker = temp[1]

        # set ticker
        if input_ticker[0] == '$':
            ticker = yf.Ticker(f"{input_ticker[1:]}")
            ticker_name = input_ticker[1:]
        else:
            ticker = yf.Ticker(f"{input_ticker}")
            ticker_name = input_ticker.lower()

        if command[1:] == "info":
            if len(temp) != 2:
                print(f"[bot] Too few or too many arguments. given: {len(temp)}, should be 2.")
                return f"Too few or too many arguments. given: {len(temp)}, should be 2."
            else:
                output = get_current(ticker)
                return output

        elif command[1:] == "financials":       # FIXME krijg empty dataframe
            if len(temp) != 2:
                print(f"[bot] Too few or too many arguments. given: {len(temp)}, should be 2.")
                return f"Too few or too many arguments. given: {len(temp)}, should be 2."
            else:
                output = get_fincancials(ticker)
                print(f"[debug] {output}")
                return output

        elif command[1:] == "cashflow":         # FIXME krijg empty dataframe
            if len(temp) != 2:
                print(f"[bot] Too few or too many arguments. given: {len(temp)}, should be 2.")
                return f"Too few or too many arguments. given: {len(temp)}, should be 2."
            else:
                output = get_cashflow(ticker)
                print(f"[debug] {output}")
                return output

        elif command[1:] == "dividend":
            if len(temp) != 2:
                print(f"[bot] Too few or too many arguments. given: {len(temp)}, should be 2.")
                return f"Too few or too many arguments. given: {len(temp)}, should be 2."
            else:
                output = get_dividend(ticker)
                print(f"[debug] {output}")
                return output

        elif command[1:] == "isin":
            if len(temp) != 2:
                print(f"[bot] Too few or too many arguments. given: {len(temp)}, should be 2.")
                return f"Too few or too many arguments. given: {len(temp)}, should be 2."
            else:
                output = get_isin(ticker)
                print(f"[debug] {output}")
                return output

        elif command[1:] == "events":
            if len(temp) != 2:
                print(f"[bot] Too few or too many arguments. given: {len(temp)}, should be 2.")
                return f"Too few or too many arguments. given: {len(temp)}, should be 2."
            else:
                output = get_next_event(ticker)
                print(f"[debug] {output}")
                return output

        elif command[1:] == "history":
            if len(temp) != 3:
                print(f"[bot] Too few or too many arguments. given: {len(temp)}, should be 3.")
                return f"Too few or too many arguments. given: {len(temp)}, should be 3."
            else:
                if temp[2] not in periods:
                    print(f"invalid period: should be one of: {periods}.")
                    return f"invalid period: should be one of: {periods}."

                else:
                    output = get_history(ticker, temp[2])
                    print(f"[debug] {output}")
                    return output

        elif command[1:] == "add":
            if len(temp) != 2:
                print(f"[bot] Too few or too many arguments. given: {len(temp)}, should be 2.")
                return f"Too few or too many arguments. given: {len(temp)}, should be 2."
            else:
                check = add_daily_report(ticker_name)
                if check:
                    print(f"${ticker_name.upper()} added to watch list.")
                    return f"${ticker_name.upper()} added to watch list."
                else:
                    print(f"${ticker_name.upper()} already on watch list.")
                    return f"${ticker_name.upper()} already on watch list."

        elif command[1:] == "remove":
            if len(temp) != 2:
                print(f"[bot] Too few or too many arguments. given: {len(temp)}, should be 2.")
                return f"Too few or too many arguments. given: {len(temp)}, should be 2."
            else:
                check = remove_daily_report(ticker_name)
                if check:
                    print(f"${ticker_name.upper()} removed form watch list.")
                    return f"${ticker_name.upper()} removed form watch list."
                else:
                    print(f"${ticker_name.upper()} not on watch list.")
                    return f"${ticker_name.upper()} not on watch list."

        else:
            print("[bot] invalid command")
            return f"{command} is a invalid command. \nuse !command for all available commands"
