from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Intents, Message
from discord.ext import commands

from responses import get_response

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
        
    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running!')

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
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    
@bot.hybrid_command(name="sync")
async def hello(ctx: commands.Context):
    await ctx.send("Syncing...")
    await bot.tree.sync(guild = ctx.guild)
    await ctx.send("Synced!")

@bot.hybrid_command(name="hello")
async def hello(ctx: commands.Context):
    await ctx.send(f"Hi {ctx.author.name} test", ephemeral=True)

def main() -> None:
    bot.run(TOKEN)

if __name__ == '__main__':
    main()