from discord import app_commands
from discord.ext import commands
from discord import Message
from discord import Embed
from discord import Member
from discord import Interaction

snipeDataDeleted = {}
snipeDataEdited = {}

latestUserDeleted: Member | None = None
latestUserEdited: Member | None = None

async def on_message_delete(message: Message) -> None:
    snipeDataDeleted[str(message.author.id * message.channel.id)] = message
    global latestUserDeleted
    assert isinstance(message.author, Member)
    latestUserDeleted = message.author
    username = str(message.author)
    channel = str(message.channel)
    print(f'[{channel}] {username}: deleted meessage.')


async def on_message_edit(message: Message, after: Message) -> None:
    snipeDataEdited[str(message.author.id * message.channel.id)] = message
    global latestUserEdited
    assert isinstance(message.author, Member)
    latestUserEdited = message.author
    username = str(message.author)
    channel = str(message.channel)
    print(f'[{channel}] {username}: edited meessage.')

target_group = app_commands.Group(name="target", description="Snipe Specific People.")


@target_group.command(name="snipe", description="Target Snipe the Last Deleted Message sent by "
                                                "Specified User.")
async def target_snipe(ctx, member: Member) -> None:
    await general_snipe(ctx, member, snipeDataDeleted)


@target_group.command(name="editsnipe", description="Target Snipe the Last Edited Message sent by "
                                                    "Specified User.")
async def target_edit_snipe(ctx, member: Member) -> None:
    await general_snipe(ctx, member, snipeDataEdited)


@commands.hybrid_command(name="snipe", description="Snipe the Last Deleted Message.")
async def snipe(ctx: commands.Context):
    assert isinstance(latestUserDeleted, Member)
    await general_snipe(ctx, latestUserDeleted, snipeDataDeleted)


@commands.hybrid_command(name="editsnipe", description="Snipe the Last Edited Message.")
async def editsnipe(ctx: commands.Context):
    assert isinstance(latestUserEdited, Member)
    await general_snipe(ctx, latestUserEdited, snipeDataEdited)


async def general_snipe(ctx: commands.Context, member: Member, data: dict):

    if member is None:
        await ctx.send("There's nothing to snipe.")

    key = str(member.id * ctx.channel.id)
    if key not in data:
        await ctx.send("There's nothing to snipe.")
        return
    message: Message = data[key]
    contentEmbed = Embed(
        description=message.content,
        timestamp=message.created_at
    )
    contentEmbed.set_author(name=member.display_name,
                     icon_url=member.display_avatar)

    await ctx.send(embed=contentEmbed)
    for embed in message.embeds:
        await ctx.send(embed.url)
    for attachment in message.attachments:
        await ctx.send(attachment.url)


async def setup(bot: commands.Bot):
    bot.tree.add_command(target_group)
    bot.add_command(snipe)
    bot.add_command(editsnipe)
    bot.add_listener(on_message_delete)
    bot.add_listener(on_message_edit)
