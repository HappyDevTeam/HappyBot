from typing import Final, Union
import os
from dotenv import load_dotenv
from discord import Intents, Message
from discord.ext import commands
import pathlib

try:
    from botcommands import translate
except Exception as e:
    translate = None
    print(e)

CURRENT_DIR = pathlib.Path(__file__).parent
CMDS_DIR = CURRENT_DIR / "botcommands"

load_dotenv()
TOKEN: Final[str | None] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


def get_response(user_input: str) -> str | None:
    lowered: str = user_input.lower()

    if translate is not None:
        if translate.is_english(user_input) < -0.9:
            translated_text = translate.translate_text("en", user_input)
            return translated_text

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
    else:
        return None


async def send_message(message: Message, user_message: str) -> None:
    if user_message is None:
        print('(Message empty because intents not enabled)')
        return
    if user_message is None:
        return
    response: str | None = get_response(user_message)
    if response is None or message is None:
        return
    await message.author.send(response)


@bot.event
async def on_message(message: Message) -> None:
    if message is None:
        raise Exception("Message instance does not exist")
    if message.author == bot.user:
        return
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)


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

if __name__ == '__main__':
    assert isinstance(TOKEN, str)
    bot.run(TOKEN)
