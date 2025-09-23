import re
import types

import discord
from discord import Message
from discord.ext import commands
from botcommands.sources import tiktok, reel
import os

SOURCES = {
    tiktok,
    reel
}


async def handler(user_input: str) -> str:
    if not re.search(r'https://', user_input):
        user_input = "https://" + user_input

    source: types.ModuleType | None = None
    for script in SOURCES:
        if script.is_valid(user_input) is True:
            source = script
            print("[qwktok] detected valid url")
            break
    if source is None:
        return ""

    filename: str = await source.download(user_input)
    if filename == "":
        print("[qwktok] failed to download video")
        return ""
    print("[qwktok] video successfully downloaded")

    return filename


async def on_message(message: Message) -> None:
    filename: str = await handler(message.content)
    if filename == "":
        return

    await message.reply(file=discord.File(filename))
    os.remove(filename)
    await message.edit(suppress=True)


@commands.hybrid_command(name="qwktok")
async def qwktok(ctx: commands.Context, url: str) -> None:
    await ctx.defer()

    filename: str = await handler(url)
    if filename == "":
        await ctx.send("Invalid url.", ephemeral=True)

    await ctx.reply(file=discord.File(filename))
    os.remove(filename)

    print(f"qwktok.py: qwktok({url})")


async def setup(bot: commands.Bot):
    bot.add_command(qwktok)
    bot.add_listener(on_message)
