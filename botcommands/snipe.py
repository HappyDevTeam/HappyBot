from discord import app_commands, Message, Embed, Member, Interaction, InteractionResponse
from discord.ext import commands
from botcommands.qwktok import is_valid_tiktok_link

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
    print(f'[{channel}] {username}: deleted message.')


async def on_message_edit(message: Message, after: Message) -> None:
    snipeDataEdited[str(message.author.id * message.channel.id)] = message
    global latestUserEdited
    assert isinstance(message.author, Member)
    latestUserEdited = message.author
    username = str(message.author)
    channel = str(message.channel)
    print(f'[{channel}] {username}: edited message.')


target_group = app_commands.Group(name="target", description="Snipe Specific People.")


@target_group.command(name="snipe", description="Target Snipe the Last Deleted Message sent by "
                                                "Specified User.")
async def target_snipe(interaction: Interaction, member: Member) -> None:
    print(f"snipe.py: target_snipe({member.name})")
    await general_snipe(interaction, member, snipeDataDeleted)


@target_group.command(name="editsnipe", description="Target Snipe the Last Edited Message sent by "
                                                    "Specified User.")
async def target_edit_snipe(interaction: Interaction, member: Member) -> None:
    print(f"snipe.py: target_edit_snipe({member.name})")
    await general_snipe(interaction, member, snipeDataEdited)


@commands.hybrid_command(name="snipe", description="Snipe the Last Deleted Message.")
async def snipe(ctx: commands.Context):
    print(f"snipe.py: snipe()")
    await general_snipe(ctx, latestUserDeleted, snipeDataDeleted)  # pyright: ignore


@commands.hybrid_command(name="editsnipe", description="Snipe the Last Edited Message.")
async def edit_snipe(ctx: commands.Context):
    print(f"snipe.py: edit_snipe()")
    await general_snipe(ctx, latestUserEdited, snipeDataEdited)  # pyright: ignore


async def general_snipe(ctx: commands.Context | Interaction, member: Member, data: dict):
    response: commands.Context | InteractionResponse = ctx  # pyright: ignore
    if type(ctx) is Interaction:
        response = ctx.response  # type: ignore

    if member is None:
        if type(ctx) is commands.Context:
            await response.send("There's nothing to snipe.", ephemeral=True)
        else:
            await response.send_message("There's nothing to snipe.", ephemeral=True)
        return

    key = str(member.id * ctx.channel.id)  # pyright: ignore
    if key not in data:
        if type(ctx) is commands.Context:
            await response.send("There's nothing to snipe.", ephemeral=True)  # pyright: ignore
        else:
            await response.send_message("There's nothing to snipe.",  # pyright: ignore
                                        ephemeral=True)
        return
    message: Message = data[key]
    content_embed = Embed(
        description=message.content,
        timestamp=message.created_at
    )
    content_embed.set_author(name=member.display_name,
                             icon_url=member.display_avatar)

    if type(response) is commands.Context:
        await response.send(embed=content_embed)
    else:
        await response.send_message(embed=content_embed)  # pyright: ignore
    for attachment in message.attachments:
        if type(response) is commands.Context:
            await response.send(attachment.url)
        else:
            await response.send_message(attachment.url)  # pyright: ignore
    for embed in message.embeds:
        if is_valid_tiktok_link(str(embed.description)):
            return
        if type(response) is commands.Context:
            await response.send(embed.url)
        else:
            await response.send_message(embed.url)  # pyright: ignore


async def setup(bot: commands.Bot):
    bot.tree.add_command(target_group)
    bot.add_command(snipe)
    bot.add_command(edit_snipe)
    bot.add_listener(on_message_delete)
    bot.add_listener(on_message_edit)
