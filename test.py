# FIXME set_ticker in kleine functies schrijven
# FIXME readme schrijven
# fixme wanneer public repo, token weghalen!


import os
import random

import discord
from discord.ext import commands

from help import *
from commands import *
bot = commands.Bot(command_prefix='!')

TOKEN = "ODYwODQzMzcwOTIyNTA4MzA4.YOBI3Q.WZhUxJbW8OseQKZsQZm97n7kuuw"

@bot.event
async def on_ready():
    print("\n+***********************************+")
    print(f"* https://github.com/Hendrikjilderda/stonk-o-bot * ")
    print(f"*       Bot Name: {bot.user.name}       *")
    print(f"*     Bot ID: {bot.user.id}    *")
    print(f"*       Discord Version: {discord.__version__}      *")
    print("+***********************************+\n")
    print("[info] start up complete")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing the required arguments.\nType !help {command} to get more info.")


@bot.command(name='add', help=add_help)
async def add(ctx, ticker_name):
    check = add_daily_report(ticker_name)
    if check:
        print(f"${ticker_name.upper()} added to watch list.")       #fixme toevoegen melding dat het in volgede report staat
        await ctx.send(f"${ticker_name.upper()} added to watch list.")
    else:
        print(f"${ticker_name.upper()} already on watch list.")
        await ctx.send(f"${ticker_name.upper()} already on watch list.")


@bot.command(name='commands', help=commands_help)
async def command_list(ctx):
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

    await ctx.send(embed=embed)


@bot.command(name='daily', help=daily_help)
async def daily(ctx, weekday):
    await ctx.send(file=discord.File(get_daily_report_file(weekday)))


@bot.command(name='dividend', help=dividend_help)         #FIXME beter layout voor dividend command
async def dividend(ctx, ticker):
    await ctx.send(get_dividend(ticker))


@bot.command(name='events', help=events_help)         #FIXME beter layout voor dividend command
async def events(ctx, ticker):
    await ctx.send(get_next_event(ticker))


@bot.command(name='financials', help=financials_help)         #FIXME beter layout voor dividend command
async def financials(ctx, ticker):
    await ctx.send(get_fincancials(ticker))


@bot.command(name='history', help=history_help)         #FIXME beter layout voor history command
async def history(ctx, ticker, period):
    await ctx.send(get_history(ticker, period))


@bot.command(name='info', help=info_help)
async def info(ctx, ticker):
    await ctx.send(embed=get_current(ticker))


@bot.command(name='isin', help=isin_help)             #FIXME beter layout voor isin command
async def isin(ctx, ticker):
    await ctx.send(get_isin(ticker))


@bot.command(name='list', help=list_help)             #FIXME beter layout voor isin command
async def isin(ctx):
    await ctx.send(get_ticker_list())


@bot.command(name='remove', help=remove_help)
async def remove(ctx, ticker_name):
    check = remove_daily_report(ticker_name)
    if check:
        print(f"${ticker_name.upper()} removed form watch list.")
        await ctx.send(f"${ticker_name.upper()} removed form watch list.")
    else:
        print(f"${ticker_name.upper()} not on watch list.")
        await ctx.send(f"${ticker_name.upper()} not on watch list.")

bot.run(TOKEN)


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