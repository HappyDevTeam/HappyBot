from typing import Final, Union
import atexit
import os
from dotenv import load_dotenv
from discord import Intents, Message
from discord.ext import commands
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent
CMDS_DIR = CURRENT_DIR / "botcommands"

load_dotenv()
TOKEN: Final[str | None] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready() -> None:
    print("Bot is Up")
    for extension in CMDS_DIR.glob("*.py"):
        if extension.name == "__init__.py":
            continue
        try:
            await bot.load_extension(f"botcommands.{extension.name[:-3]}")
        except Exception as e:
            print()
            print(f"Could not load extension {extension.name[:-3]}")
            print("Type: ", type(e).__name__)
            print(e.args)
            print()
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.hybrid_command(name="sync")
async def sync(ctx: commands.Context):
    try:
        await ctx.send("Syncing...")
        await bot.tree.sync(guild=ctx.guild)
        await ctx.send("Synced!")
    except Exception as e:
        print(e)
    return sync

if __name__ == '__main__':
    assert isinstance(TOKEN, str)
    bot.run(TOKEN)

def exit_handler():
    print('\n\n\nBot shutting down')

atexit.register(exit_handler)