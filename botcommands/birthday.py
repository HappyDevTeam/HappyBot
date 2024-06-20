import discord
from discord import app_commands
from discord.ext import commands
import json
from json.decoder import JSONDecodeError
import os
from datetime import datetime
import threading

birthday_path = './botsettings/birthday.json'
open_mode = 'r+' if os.path.exists(birthday_path) else 'w+'
with open(birthday_path, open_mode, encoding="utf-8") as birthday_file:
    try:
        birthday = json.load(birthday_file)
    except JSONDecodeError as e:
        birthday = {}
        print(e)

birthday_group = app_commands.Group(name="birthday", description="Birthday Commands!")


def check_time():

    now = datetime.now()
    time = float(now.strftime("%H"))*3600 + float(now.strftime("%M"))*60 + float(now.strftime("%S"))
    interval = 24.0 * 3600 - time

    threading.Timer(interval, check_time).start()

    current_date = now.strftime("%m/%d/%Y")
    print("Today's Date: " + current_date)


@birthday_group.command(name="set", description="Add a user's birthday to the list! "
                                                "Format for Date: MM/DD/YYYY")
async def add_birthday(interaction: discord.Interaction, user: discord.User, date: str) -> None:
    global birthday

    try:
        datetime.strptime(date, '%m/%d/%Y').date()
    except ValueError:
        await interaction.response.send_message("That is an invalid date!", ephemeral=True)
        return

    key = date[0:5]
    year = date[6:]
    user_id = user.id

    try:
        if {str(user_id): year} in birthday[key]:
            await interaction.response.send_message("Birthday already exists for this user.",
                                                    ephemeral=True)
            return
        birthday[key].append({user_id: year})
    except KeyError:
        birthday.update({key: [{user_id: year}]})

    birthday = dict(sorted(birthday.items()))

    with open(birthday_path, open_mode, encoding="utf-8") as birthday_file:
        json.dump(birthday, birthday_file, ensure_ascii=False, indent=4)

    await interaction.response.send_message("Birthday was successfully added!", ephemeral=True)
    return


@birthday_group.command(name="list", description="Lists all birthdays!")
async def list_birthdays(interaction: discord.Interaction):
    return


async def setup(bot: commands.Bot):
    check_time()
    bot.tree.add_command(birthday_group)
    return
