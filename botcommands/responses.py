from discord.ext import commands
from discord import Message


@commands.hybrid_command(name="hello")
async def hello(ctx: commands.Context):
    try:
        await ctx.send(f"Hi {ctx.author.display_name} test", ephemeral=True)
    except Exception as e:
        print(e)


def get_response(user_input: str) -> str | None:
    lowered: str = user_input.lower()
    if lowered == 'Hello World!':
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
    bot.add_listener(on_message)
