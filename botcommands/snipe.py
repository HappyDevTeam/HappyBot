from discord.ext import commands
from discord import Client
from discord import Message
from discord import Embed
from discord import Member

snipeDataDeleted = {}
snipeDataEdited = {}


async def on_message_delete(message: Message) -> None:
    snipeDataDeleted[str(message.author.id * message.channel.id)] = message
    username = str(message.author)
    channel = str(message.channel)
    print(f'[{channel}] {username}: deleted meessage.')


async def on_message_edit(message: Message, after: Message) -> None:
    snipeDataEdited[str(message.author.id * message.channel.id)] = message
    username = str(message.author)
    channel = str(message.channel)
    print(f'[{channel}] {username}: edited meessage.')


@commands.hybrid_command(name="snipe")
async def snipe(ctx: commands.Context, member: Member):
    await snipeGeneral(ctx, member, snipeDataDeleted)


@commands.hybrid_command(name="snipe_edit")
async def snipeEdit(ctx: commands.Context, member: Member):
    await snipeGeneral(ctx, member, snipeDataEdited)


async def snipeGeneral(ctx: commands.Context, member: Member, data: dict):
    key = str(member.id * ctx.channel.id)
    if key not in data:
        await ctx.send("No message found.")
        return
    message: Message = data[key]
    contentEmbed = Embed(
        title="Sniping " + str(member.display_name),
        description=message.content,
        timestamp=message.created_at
    )
    contentEmbed.set_footer(text=message.channel.name) #type: ignore
    contentEmbed.set_author(name=member.display_name,
                     icon_url=member.display_avatar)

    await ctx.send(embed=contentEmbed)
    for embed in message.embeds:
        await ctx.send(embed.url)
    for attachment in message.attachments:
        await ctx.send(attachment.url)


async def setup(bot: commands.Bot):
    bot.add_command(snipe)
    bot.add_command(snipeEdit)
    bot.add_listener(on_message_delete)
    bot.add_listener(on_message_edit)