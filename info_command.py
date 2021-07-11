import discord

from colorthief import ColorThief
import requests

import yfinance as yf


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

