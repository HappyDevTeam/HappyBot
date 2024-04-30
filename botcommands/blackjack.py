from discord.ext import commands
import discord

@commands.hybrid_command(name="blackjack")
async def blackjack(ctx: commands.Context):
    embed = discord.Embed(
        color=discord.Colour.red(),
        title="Blackjack",
        description="gamba",
    )
    embed.set_footer(text="test")
    
    await ctx.send(embed=embed)
    


async def setup(bot: commands.Bot):
    bot.add_command(blackjack)

