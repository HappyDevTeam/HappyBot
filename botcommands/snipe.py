from discord import app_commands
from discord.ext import commands
from discord import Message
from discord import Embed
from discord import Member

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
    await general_snipe(ctx, latestUserDeleted, snipeDataDeleted)  # pyright: ignore


@commands.hybrid_command(name="editsnipe", description="Snipe the Last Edited Message.")
async def edit_snipe(ctx: commands.Context):
    await general_snipe(ctx, latestUserEdited, snipeDataEdited)  # pyright: ignore


async def general_snipe(ctx: commands.Context, member: Member, data: dict):
    if member is None:
        await ctx.send("There's nothing to snipe.", ephemeral=True)
        return

    key = str(member.id * ctx.channel.id)
    if key not in data:
        await ctx.send("There's nothing to snipe.", ephemeral=True)
        return
    message: Message = data[key]
    content_embed = Embed(
        description=message.content,
        timestamp=message.created_at
    )
    content_embed.set_author(name=member.display_name,
                             icon_url=member.display_avatar)

    await ctx.send(embed=content_embed)
    for embed in message.embeds:
        await ctx.send(embed.url)
    for attachment in message.attachments:
        await ctx.send(attachment.url)


async def setup(bot: commands.Bot):
    bot.tree.add_command(target_group)
    bot.add_command(snipe)
    bot.add_command(edit_snipe)
    bot.add_listener(on_message_delete)
    bot.add_listener(on_message_edit)
