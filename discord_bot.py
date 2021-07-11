# FIXME readme schrijven

# https://medium.com/@chaoren/how-to-timeout-in-python-726002bf2291
# FIXME ^^ usable for timeouts and checking if data can actually be retrieved

import os
import sys

import discord
from discord.ext import commands

import yfinance as yf

from datetime import datetime

from info_command import get_current

from help import *
from datetime import date


bot = commands.Bot(command_prefix='!')


user_list = []
ticker_list = ["tsla", "aapl", "amc", "sens"]
report = []

week_days = {"monday": 0, "tuesday": 1, "wednesday": 2,
             "thursday": 3, "friday": 4,
             "yesterday": (date.today().weekday()-1)}

startup_time = ''

@bot.event
async def on_ready():
    global startup_time
    startup_time = datetime.now().strftime('%H:%M:%S')
    print("\n#***************************************************#")
    print(f"*               Bot Name: {bot.user.name}               *")
    print(f"*            Bot ID: {bot.user.id}             *")
    print(f"*               Discord Version: {discord.__version__}              *")
    print(f"*               start time: {startup_time}                *")
    print(f"*                                                   * ")
    print(f"*  https://github.com/Hendrikjilderda/stonk-o-bot   * ")
    print("#***************************************************#\n")
    print("[info] start up complete")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing the required arguments.\nType !help {command} to get more info.")

@bot.command(name='add', help=add_help)
async def add(ctx, ticker_name):
    try:
        check = False
        if ticker_name not in ticker_list:
            ticker_list.append(ticker_name)
            check = True
        else:
            check = False

        if check:
            print(f"${ticker_name.upper()} added to watch list.")       #fixme toevoegen melding dat het in volgede report staat
            await ctx.send(f"${ticker_name.upper()} added to watch list.")
        else:
            print(f"${ticker_name.upper()} already on watch list.")
            await ctx.send(f"${ticker_name.upper()} already on watch list.")
    except:
        print(f"[error] {sys.exc_info()}")


@bot.command(name='commands', help=commands_help)
async def command_list(ctx):
    try:
        embed = discord.Embed(
            title='Commands',
            colour=discord.Colour.purple()
        )
        embed.add_field(name="!add {stonk}", value="add stonk to watchlist")
        embed.add_field(name="!dividend {stonk}", value="returns the latest data regarding dividend")
        embed.add_field(name="!history {stonk} {period}", value="returns summary of data from "
                                                                "certain time frame")
        embed.add_field(name="!info {stonk}", value="returns a short summary of the stonk")
        embed.add_field(name="!isin {stonk}", value="returns ISIN number")
        embed.add_field(name="!list", value="returns list of stonks on watchlist")
        embed.add_field(name="!remove {stonk}", value="removes stonk form watchlist")
        embed.add_field(name="!daily {weekday}", value="gives daily report from that day")
        embed.set_footer(text="https://github.com/Hendrikjilderda/stonk-o-bot")

        print(f"[info] !commands executed")

        await ctx.send(embed=embed)
    except:
        print(f"[error] {sys.exc_info()}")


@bot.command(name='daily', help=daily_help)
async def daily(ctx, weekday):
    try:
        print(f"[info] !daily {weekday} executed")
        await ctx.send(file=discord.File(f'./daily-reports/report {week_days[weekday.lower()]}.xlsx'))
    except:
        print(f"[error] {sys.exc_info()}")


@bot.command(name='dividend', help=dividend_help)         #FIXME beter layout voor dividend command
async def dividend(ctx, ticker):
    try:
        fticker = yf.Ticker(ticker)
        print(f"[info] !dividend {ticker} executed")
        await ctx.send(fticker.dividends)
    except:
        print(f"[error] {sys.exc_info()}")


@bot.command(name='events', help=events_help)         #FIXME beter layout voor dividend command
async def events(ctx, ticker):
    try:
        fticker = yf.Ticker(ticker)
        print(f"[info] !events {ticker} executed")
        await ctx.send(fticker.calendar)
    except:
        print(f"[error] {sys.exc_info()}")


@bot.command(name='financials', help=financials_help)         #FIXME beter layout voor dividend command
async def financials(ctx, ticker):
    try:
        fticker = yf.Ticker(ticker)
        print(f"[info] !financials {ticker} not executed")
        await ctx.send(fticker.financials)
    except:
        print(f"[error] {sys.exc_info()}")


@bot.command(name='history', help=history_help)         #FIXME beter layout voor history command
async def history(ctx, ticker, period):
    try:
        fticker = yf.Ticker(ticker)
        print(f"[info] !history {ticker} {period} executed")
        await ctx.send(fticker.history)
    except:
        print(f"[error] {sys.exc_info()}")


#FIXME

@bot.command(name='info', help=info_help)
async def info(ctx, ticker):
    try:
        response = get_current(ticker)
        print(f"[info] !info {ticker} executed")
        await ctx.send(embed=response)
    except:
        print(f"[error] {sys.exc_info()}")


@bot.command(name='isin', help=isin_help)             #FIXME beter layout voor isin command
async def isin(ctx, ticker):
    try:
        fticker = yf.Ticker(ticker)
        print(f"!isin {ticker} executed")
        await ctx.send(fticker.isin)

    except:
        print(f"[error] {sys.exc_info()}")



@bot.command(name='list', help=list_help)             #FIXME beter layout voor isin command
async def isin(ctx):
    try:
        pretty_list = "Stocks on the watch list are: "
        for element in ticker_list[:-1]:
            pretty_list += f"${element.upper()}, "
        pretty_list += f"${ticker_list[-1].upper()}"
        print(f"[info] {pretty_list}")

        await ctx.send(pretty_list)
    except:
        print(f"[error] {sys.exc_info()}")


@bot.command(name='remove', help=remove_help)
async def remove(ctx, ticker_name):
    try:
        check = False
        if ticker_name in ticker_list:
            ticker_list.remove(ticker_name)
            check = True
        else:
            check = False

        if check:
            print(f"[info] ${ticker_name.upper()} removed form watch list.")
            await ctx.send(f"${ticker_name.upper()} removed form watch list.")
        else:
            print(f"[info] ${ticker_name.upper()} not on watch list.")
            await ctx.send(f"${ticker_name.upper()} not on watch list.")
    except:
        print(f"[error] {sys.exc_info()}")


bot.run(os.getenv("TOKEN"))
# bot.run(TOKEN)


# https://www.javaer101.com/en/article/40873438.html
# FIXME ^^ execute on set time
def automatic_daily_report(report, ticker_list):

    channel = bot.get_channel(860842837494464512)

    for x in range(0, len(ticker_list)):
        embed = discord.Embed(
            title=f"{report[x]['name']}",
            colour=discord.Colour.purple()
        )
        embed.add_field(name='previous close', value=f"${report[x]['previous close']}", inline=True)
        embed.add_field(name='day high', value=f"${report[x]['day high']}", inline=True)
        embed.add_field(name='day low', value=f"${report[x]['day low']}", inline=True)
        channel.send(embed=embed)
