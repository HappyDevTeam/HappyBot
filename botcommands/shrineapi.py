import discord
from discord import app_commands
from discord.ext import commands
from discord import Message
import requests
import random
import json

@commands.hybrid_command(name="roll")
async def roll(ctx: commands.Context, size: int):
    generated_num = random.randint(1, size)
    try:
        await ctx.send(generated_num)
    except Exception as e:
        print(e)

@commands.hybrid_command(name="shrine")
async def shrine(ctx: commands.Context):
    response = requests.get("https://api.nightlight.gg/v1/shrine?pretty=true")
    data = response.text
    try:
        await ctx.send(data)
    except Exception as e:
        print(e)
    

async def setup(bot: commands.Bot):
    bot.add_command(roll)
    bot.add_command(shrine)