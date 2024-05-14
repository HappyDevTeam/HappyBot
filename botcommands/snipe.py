from discord.ext import commands
from discord import Client
from discord import Message
from discord import Embed
from discord import Member

snipeData = {}


async def on_message_delete(message: Message) -> None:
    snipeData[str(message.author.id * message.channel.id)] = message
    username=str(message.author)
    channel=str(message.channel)
    print(f'[{channel}] {username}: deleted meessage.')


@commands.hybrid_command(name="snipe")
async def snipe(ctx: commands.Context, member: Member):
    message: Message = snipeData[str(member.id * ctx.channel.id)]
    embed = Embed(
        title="Sniping " + str(member.display_name),
        description=message.content,
        timestamp=message.created_at
    )
    embed.set_footer(text=message.channel.name)
    embed.set_author(name=member.display_name,
                     icon_url=member.display_avatar)
    await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    bot.add_command(snipe)
    bot.add_listener(on_message_delete)
