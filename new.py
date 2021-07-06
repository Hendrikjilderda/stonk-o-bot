import os
import random

TOKEN = "ODYwODQzMzcwOTIyNTA4MzA4.YOBI3Q.WZhUxJbW8OseQKZsQZm97n7kuuw"

# 1
from discord.ext import commands


# 2
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='info', help="responds random shit")
async def info(ctx, ticker):
    await ctx.send('blyat')

bot.run(TOKEN)