from typing import Any, Coroutine, Never, Callable
from discord.ext import commands
from discord.ext.commands import Context
from google.cloud import translate_v2 as translator # type: ignore


def translate_text(target: str, text: str) -> dict:

    translate_client = translator.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print("Text: {}".format(result["input"]))
    print("Translation: {}".format(result["translatedText"]))
    print("Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result

@commands.hybrid_command(name="translate")
async def translate(ctx: commands.Context, lang: str, text: str) -> None:
    result = translate_text(lang, text)
    await ctx.send(result["translatedText"])


async def setup(bot: commands.Bot) -> None:
    bot.add_command(translate)
