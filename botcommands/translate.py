from discord.ext import commands
from google.cloud import translate_v2 as translator
import random

translatorClient = translator.Client()
langs = translatorClient.get_languages()

def translate_text(target: str, text: str) -> dict:

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translatorClient.translate(text, target_language=target)

    print("Text: {}".format(result["input"]))
    print("Translation: {}".format(result["translatedText"]))
    print("Detected source language: {}".format(result["detectedSourceLanguage"]))

    return result

def randomTranslate(text: str) -> str:

    for i in range(0, 10):

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        nextLang = random.randint(0, len(langs))
        result = translatorClient.translate(text, target_language=langs[nextLang]["language"])
        text = result["translatedText"]

    return text

@commands.hybrid_command(name="translate")
async def translate(ctx: commands.Context, lang: str, text: str) -> str:
    result = translate_text(lang, text)
    await ctx.send(result["translatedText"])

@commands.hybrid_command(name="randomtranslate")
async def randomtranslate(ctx: commands.Context, text: str) -> str:
    translated_text = randomTranslate(text)
    await ctx.send(f"Original Text: {text} \nTranslated Text: {translated_text}")


async def setup(bot: commands.Bot):
    bot.add_command(translate)
    bot.add_command(randomtranslate)
