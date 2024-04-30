from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Intents, Message
from discord.ext import commands
import pathlib

from botcommands.responses import get_response

CURRENT_DIR = pathlib.Path(__file__).parent
CMDS_DIR = CURRENT_DIR / "botcommands"

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents = intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message empty because intents not enabled)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    response: str = get_response(user_message)
    if response == '':
        return
    try:
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    
    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

@bot.event
async def on_ready():
    print("Bot is Up")
    for extension in CMDS_DIR.glob("*.py"):
        await bot.load_extension(f"botcommands.{extension.name[:-3]}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

def main() -> None:
    bot.run(TOKEN)

if __name__ == '__main__':
    main()