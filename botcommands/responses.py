from discord.ext import commands
from botcommands import translate


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if not translate.is_english(user_input):
        en_code = list(filter(lambda lang: lang['name'] == 'English', translate.langs))[0]["language"]
        translated_text = translate.translate_text(en_code, user_input)
        return translated_text["translatedText"]

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'


def sync_curry(bot):
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
