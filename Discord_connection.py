import discord

import requests
from colorthief import ColorThief

from stonks import set_ticker

TOKEN = "ODYwODQzMzcwOTIyNTA4MzA4.YOBI3Q.WZhUxJbW8OseQKZsQZm97n7kuuw"

client = discord.Client()
list_commands = ["!add", "!dividend", "!history", "!info", "!isin", "!list", "!remove"]


@client.event
async def on_ready():
    print("+***********************************+")
    print(f"*       Bot Name: {client.user.name}       *")
    print(f"*     Bot ID: {client.user.id}    *")
    print(f"*       Discord Version: {discord.__version__}      *")
    print("+***********************************+")
    print("[info] start up complete\n")

@client.event
async def on_message(message):

    print(f"{message.author} : {message.content}")       # use for !join !leave commands!!

    if message.channel.name == "stonkie-stonks":
        if message.author == client.user:
            return

        if message.content.startswith('!'):
            if message.content.startswith("!commands"):
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
                embed.set_footer(text="https://github.com/Hendrikjilderda/stonk-o-bot")

                await message.channel.send(embed=embed)

            elif message.content.startswith("!info"):

                response = set_ticker(message.content)
                if type(response) is not str:
                    image = ColorThief(requests.get(response['logo'], stream=True).raw)
                    dominant_color = image.get_color(quality=1)
                    # print(dominant_color)

                    embed = discord.Embed(
                        title=f"{response['name']}",
                        description=f"{response['short summary']}",
                        colour=discord.Colour.from_rgb(dominant_color[0], dominant_color[1], dominant_color[2])
                        # fIXME niet heel accuraat atm
                    )

                    embed.set_thumbnail(url=response['logo'])
                    embed.set_footer(text='data acquired from Yahoo Finance')

                    embed.add_field(name='marketCap', value=f"${'{:,}'.format(response['marketCap'])}", inline=True)
                    embed.add_field(name='previous close', value=f"${response['previous close']}", inline=True)
                    embed.add_field(name='day high', value=f"${response['day high']}", inline=True)
                    embed.add_field(name='day low', value=f"${response['day low']}", inline=True)
                    embed.add_field(name='yearly high', value=f"${response['yearly high']}", inline=True)
                    embed.add_field(name='yearly low', value=f"${response['yearly low']}", inline=True)
                    embed.add_field(name='website', value=response['website'], inline=False)

                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send(response)

            elif message.content.startswith("!list"):
                response = set_ticker(message.content)
                pretty_list = "Stocks on the watch list are: "
                for element in response[:-1]:
                    pretty_list += f"${element.upper()}, "
                pretty_list += f"${response[-1].upper()}"
                print(pretty_list)
                await message.channel.send(pretty_list)

            else:
                response = set_ticker(message.content)
                await message.channel.send(response)

        if message.content.startswith("$"):
            await message.channel.send("Test message")

# fixme wanneer public repo, token weghalen!
client.run(TOKEN)
