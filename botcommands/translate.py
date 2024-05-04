import discord
from discord import app_commands
from discord.ext import commands
from google.cloud import translate_v2 as translator
from google.auth.exceptions import DefaultCredentialsError
import random

try:
    translator_client = translator.Client()
except DefaultCredentialsError as e:
    raise e
langs = translator_client.get_languages()


def is_english(text: str) -> bool:
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    detected_language = translator_client.detect_language(text)["language"]
    english_language = list(filter(lambda lang: lang['name'] == 'English', langs))[0]["language"]

    return detected_language == english_language


def translate_text(lang: str, text: str) -> dict:
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translator_client.translate(text, target_language=lang)

    return result


def random_translate(text: str) -> str:
    for i in range(0, 10):

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        nextLang = random.randint(0, len(langs))
        result = translator_client.translate(text, target_language=langs[nextLang]["language"])
        text = result["translatedText"]

    return text


translate_group = app_commands.Group(name="translate", description="Translate texts.")


@translate_group.command(name="text", description="Translate Text to a Desired Language!")
async def translate(interaction: discord.Interaction, lang: str, text: str) -> None:

    result = translate_text(lang, text)
    await interaction.response.send_message(result["translatedText"])


@translate_group.command(name="random", description="Translate a text through many languages!")
async def translate_random(interaction: discord.Interaction, text: str) -> None:
    translated_text = random_translate(text)
    await interaction.response.send_message(f"Original Text: {text}\n"
                                            f"Translated Text: {translated_text}")


async def setup(bot: commands.Bot):
    bot.tree.add_command(translate_group)
