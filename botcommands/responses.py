from discord.ext import commands

def get_response(user_input: str) -> str | None:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
    else:
        return None


def sync_curry(bot: commands.Bot):
    @commands.hybrid_command(name="sync")
    async def sync(ctx: commands.Context):
        try:
            await ctx.send("Syncing...")
            await bot.tree.sync(guild=ctx.guild)
            await ctx.send("Synced!")
        except Exception as e:
            print(e)

    return sync


@commands.hybrid_command(name="hello")
async def hello(ctx: commands.Context):
    try:
        await ctx.send(f"Hi {ctx.author.display_name} test", ephemeral=True)
    except Exception as e:
        print(e)

async def setup(bot: commands.Bot):
    bot.add_command(sync_curry(bot))
    bot.add_command(hello)
