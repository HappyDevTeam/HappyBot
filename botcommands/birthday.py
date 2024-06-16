import discord
from discord import app_commands
from discord.ext import commands
import json
from json.decoder import JSONDecodeError
from io import TextIOWrapper
import os
from datetime import datetime

birthday_path = './botsettings/birthday.json'
openmode = 'r+' if os.path.exists(birthday_path) else 'w+'
birthday_file: TextIOWrapper = open(birthday_path, openmode, encoding='utf-8')
try:
    birthday = json.load(birthday_file)
except JSONDecodeError as e:
    birthday = {}
    print(e)

birthday_group = app_commands.Group(name="birthday", description="Birthday Commands!")


@birthday_group.command(name="set", description="Add a user's birthday to the list! "
                                                "Format for Date: MM/DD/YYYY")
async def add_birthday(interaction: discord.Interaction, name: str, date: str) -> None:

    try:
        datetime.strptime(date, '%m/%d/%Y').date()
    except ValueError:
        await interaction.response.send_message("That is an invalid date!", ephemeral=True)
        return

    birthday[date] = [name]

    json.dump(birthday, birthday_file, ensure_ascii=False, indent=4)

    await interaction.response.send_message("Birthday was successfully added!", ephemeral=True)
    return


@birthday_group.command(name="list", description="Lists all birthdays!")
async def list_birthdays(interaction: discord.Interaction):



    return

async def setup(bot: commands.Bot):
    bot.tree.add_command(birthday_group)
    return

