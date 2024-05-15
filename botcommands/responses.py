from discord.ext import commands
from discord import Message
import json
from json.decoder import JSONDecodeError
from io import TextIOWrapper
import os

autoreplyPath = './botsettings/autoreply.json'
openmode = 'r+' if os.path.exists(autoreplyPath) else 'w'
autoreplyFile: TextIOWrapper = open(autoreplyPath, openmode, encoding='utf-8')
try:
    autoreply = json.load(autoreplyFile)
except JSONDecodeError as e:
    autoreply = {}
    print(e)


@commands.hybrid_command(name="hello")
async def hello(ctx: commands.Context):
    try:
        await ctx.send(f"Hi {ctx.author.display_name} test", ephemeral=True)
    except Exception as e:
        print(e)


@commands.hybrid_command(name="make_reply")
async def make_reply(ctx: commands.Context, target: str, response: str):
    autoreply[target] = response
    json.dump(autoreply, autoreplyFile, ensure_ascii=False, indent=4)
    await ctx.reply("Replies to " + target + " with " + autoreply[target])


@commands.hybrid_command(name="delete_reply")
async def delete_reply(ctx: commands.Context, target: str):
    autoreply.pop(target, None)
    json.dump(autoreply, autoreplyFile, ensure_ascii=False, indent=4)
    autoreplyFile.close()


def get_response(user_input: str) -> str | None:
    return autoreply.get(user_input, "")


async def send_message(message: Message, user_message: str) -> None:
    if user_message is None:
        print('(Message empty because intents not enabled)')
        return
    if user_message is None:
        return
    response: str | None = get_response(user_message)
    if response is None or message is None:
        return
    await message.channel.send(response)


async def on_message(message: Message) -> None:
    if message is None:
        raise Exception("Message instance does not exist")
    if message.author.bot:
        return
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)


async def setup(bot: commands.Bot):
    bot.add_command(hello)
    bot.add_command(make_reply)
    bot.add_listener(on_message)
