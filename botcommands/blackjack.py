from discord.ext import commands
import discord

class BJMenu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("test")
    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("test")
    @discord.ui.button(label="Split", style=discord.ButtonStyle.gray)
    async def split(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("test")


@commands.hybrid_command(name="blackjack")
async def blackjack(ctx: commands.Context):
    view = BJMenu()
    embed = discord.Embed(
        color=discord.Colour.red(),
        title="Blackjack",
        )
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
    embed.add_field(name="Dealer", value="Test")
    embed.add_field(name="Player", value="Test", inline=False)    
    await ctx.reply(embed=embed, view=view)


async def setup(bot: commands.Bot):
    bot.add_command(blackjack)

