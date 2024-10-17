import discord
from discord import app_commands, Interaction, InteractionResponse, User, TextChannel
from discord.ext import commands, tasks
import json
from json.decoder import JSONDecodeError
import os
from datetime import datetime, time
from typing import List
from configparser import ConfigParser, NoSectionError
from classes.Pagination import Pagination

MONTH_NAMES: list[str] = ["January", "February", "March", "April", "May", "June",
                          "July", "August", "September", "October", "November", "December"]
DAYS_PER_MONTH: list[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
EXISTS: int = 0
MONTH: int = 1
DAY: int = 2
MIDNIGHT: time = time(hour=7, minute=0, second=0)
BIRTHDAY_PATH: str = './botsettings/birthday.json'
CHANNEL_PATH: str = './botsettings/channelsettings.ini'
OPEN_MODE: str = ""
BIRTHDAYS: list[list[dict[str, str]]] = []
BIRTHDAY_CHANNEL_ID: int = -1
BIRTHDAY_CHANNEL: TextChannel

birthday_group = app_commands.Group(name="birthday", description="Birthday Commands!")


@tasks.loop(time=MIDNIGHT)
async def happy_birthday() -> None:
    now = datetime.now()
    date = now.strftime("%m/%d/%Y")
    month = int(date[:2]) - 1
    day = int(date[3:5]) - 1
    year = int(date[6:])
    print("Today's Date: " + date)

    for user_id in list(BIRTHDAYS[month][day].keys()):
        user_year = int(BIRTHDAYS[month][day][user_id])
        user_id = int(user_id)

        await BIRTHDAY_CHANNEL.send(f"Happy Birthday, <@{user_id}>!")  # pyright: ignore


def insert_birthday(month: int, day: int, year: str, user_id: str) -> None:
    BIRTHDAYS[month][day].update({user_id: year})

    with open(BIRTHDAY_PATH, OPEN_MODE, encoding="utf-8") as birthday_file:
        json.dump(BIRTHDAYS, birthday_file, ensure_ascii=False, indent=4)
        birthday_file.truncate()


def remove_birthday(month: int, day: int, user_id: str) -> None:
    BIRTHDAYS[month][day].pop(user_id, None)

    with open(BIRTHDAY_PATH, OPEN_MODE, encoding="utf-8") as birthday_file:
        json.dump(BIRTHDAYS, birthday_file, ensure_ascii=False, indent=4)
        birthday_file.truncate()


def is_existing_user(user_id: str) -> List[bool | int]:
    for month in range(12):
        for day in range(DAYS_PER_MONTH[month]):
            if user_id in BIRTHDAYS[month][day]:
                return [True, month, day]
    return [False, -1, -1]


async def is_valid_date(interaction: Interaction, date: str) -> bool:
    response: InteractionResponse = interaction.response  # type: ignore

    try:
        datetime.strptime(date, '%m/%d/%Y').date()
        return True
    except ValueError:
        await response.send_message("That is an invalid date!", ephemeral=True)
        return False


def load_files(bot: commands.Bot):
    global OPEN_MODE
    global BIRTHDAYS
    global BIRTHDAY_CHANNEL_ID
    global BIRTHDAY_CHANNEL

    if BIRTHDAY_PATH == '':
        print("birthday.py: Please set a file path for BIRTHDAY_PATH")

    if CHANNEL_PATH == '':
        print("birthday.py: Please set a file path for CHANNEL_PATH")

    OPEN_MODE = 'r+' if os.path.exists(BIRTHDAY_PATH) else 'w+'
    with open(BIRTHDAY_PATH, OPEN_MODE, encoding="utf-8") as birthday_file:
        try:
            BIRTHDAYS = json.load(birthday_file)
        except JSONDecodeError as e:
            BIRTHDAYS = []
            for i in range(12):
                BIRTHDAYS.append([])
                for j in range(DAYS_PER_MONTH[i]):
                    BIRTHDAYS[i].append({})
            json.dump(BIRTHDAYS, birthday_file, ensure_ascii=False, indent=4)
            birthday_file.truncate()
            print("birthday.py: JSONDecodeError:" + str(e))

    OPEN_MODE = 'r+' if os.path.exists(CHANNEL_PATH) else 'w+'
    with open(CHANNEL_PATH, OPEN_MODE, encoding="utf-8") as channel_file:
        config = ConfigParser()
        config.read(CHANNEL_PATH)
        try:
            BIRTHDAY_CHANNEL_ID = int(config.get('Channel', 'birthday_channel'))
        except NoSectionError as e:
            BIRTHDAY_CHANNEL_ID = -1
            config["Channel"] = {"birthday_channel": str(BIRTHDAY_CHANNEL_ID)}
            config.write(channel_file)
            channel_file.truncate()
            print("birthday.py: NoSectionError: " + str(e))

    BIRTHDAY_CHANNEL = bot.get_channel(BIRTHDAY_CHANNEL_ID)  # pyright: ignore
    if BIRTHDAY_CHANNEL is None:
        for guild in bot.guilds:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    BIRTHDAY_CHANNEL = channel
                    BIRTHDAY_CHANNEL_ID = BIRTHDAY_CHANNEL.id
                    break

        with open(CHANNEL_PATH, OPEN_MODE, encoding="utf-8") as channel_file:
            config = ConfigParser()
        config.read(CHANNEL_PATH)
        config["Channel"] = {"birthday_channel": str(BIRTHDAY_CHANNEL_ID)}
        config.write(channel_file)
        channel_file.truncate()

    if OPEN_MODE == "":
        print("birthday.py: failed to set OPEN_MODE")

    if len(BIRTHDAYS) == 0:
        print("birthday.py: failed to load BIRTHDAYS")

    print("birthday.py: OPEN_MODE successfully set")
    print("birthday.py: BIRTHDAYS successfully loaded")


@birthday_group.command(name="add", description="Add a user's birthday to the list! "
                                                "Format for Date: MM/DD/YYYY")
async def add_birthday(interaction: Interaction, user: User, date: str) -> None:
    response: InteractionResponse = interaction.response  # type: ignore

    if not await is_valid_date(interaction, date):
        return

    month = int(date[:2]) - 1
    day = int(date[3:5]) - 1
    year = date[6:]
    user_id = str(user.id)
    user_info = is_existing_user(user_id)

    if user_info[EXISTS]:
        await response.send_message("A birthday already exists for this user.",
                                    ephemeral=True)
        return

    insert_birthday(month, day, year, user_id)
    print(f"birthday.py: add_birthday({user.name}, {date})")
    await response.send_message("Birthday was successfully added!", ephemeral=True)


@birthday_group.command(name="edit", description="Edit an existing user's birthday on the list "
                                                 "Format for Date: MM/DD/YYYY")
async def edit_birthday(interaction: Interaction, user: User, new_date: str) -> None:
    response: InteractionResponse = interaction.response  # type: ignore

    user_id = str(user.id)
    user_info = is_existing_user(user_id)

    if not user_info[EXISTS]:
        await response.send_message("User currently doesn't exist on the birthday list!",
                                    ephemeral=True)
        return

    if not await is_valid_date(interaction, new_date):
        return

    remove_birthday(user_info[MONTH], user_info[DAY], user_id)

    month = int(new_date[:2]) - 1
    day = int(new_date[3:5]) - 1
    year = new_date[6:]
    user_id = str(user.id)

    insert_birthday(month, day, year, user_id)
    print(f"birthday.py: edit_birthday({user.name}, {new_date})")
    await response.send_message("Birthday was successfully edited!", ephemeral=True)


@birthday_group.command(name="delete",
                        description="Remove an existing user's birthday on the list")
async def delete_birthday(interaction: Interaction, user: User):
    response: InteractionResponse = interaction.response  # type: ignore

    user_id = str(user.id)
    user_info = is_existing_user(user_id)

    if not user_info[EXISTS]:
        await response.send_message("User currently doesn't exist on the birthday list",
                                    ephemeral=True)
        return

    remove_birthday(user_info[MONTH], user_info[DAY], user_id)
    print(f"birthday.py: delete_birthday({user.name})")
    await response.send_message("Birthday was successfully removed", ephemeral=True)


@birthday_group.command(name="channel",
                        description="Sets the channel where birthdays will be announced!")
async def set_channel(interaction: Interaction, channel: TextChannel):
    global BIRTHDAY_CHANNEL_ID
    response: InteractionResponse = interaction.response  # type: ignore
    BIRTHDAY_CHANNEL_ID = channel.id

    config = ConfigParser()
    config.read(CHANNEL_PATH)
    config["Channel"] = {"birthday_channel": str(BIRTHDAY_CHANNEL_ID)}
    with open(CHANNEL_PATH, OPEN_MODE, encoding="utf-8") as channel_file:
        config.write(channel_file)
        channel_file.truncate()

    print(f"birthday.py: set_channel({channel.name})")
    await response.send_message("Birthday channel successfully set.", ephemeral=True)


@app_commands.command(name="birthdays", description="Lists all birthdays!")
async def list_birthdays(interaction: Interaction) -> None:
    async def get_page(page: int):
        embed = discord.Embed(title=MONTH_NAMES[page - 1], description="")
        for i in range(len(BIRTHDAYS[page - 1])):
            for user_id in list(BIRTHDAYS[page - 1][i]):
                embed.description += (f"<@{user_id}>    :    {MONTH_NAMES[page - 1]} {i + 1}, "
                                      f"{BIRTHDAYS[page - 1][i][user_id]}\n")  # pyright: ignore

        if embed.description == "":
            embed.description = "Nobody Yet"

        total_pages = 12
        embed.set_footer(text=f"Page {page}/{total_pages}")
        return embed, total_pages

    print(f"birthday.py: list_birthdays()")
    await Pagination(interaction, get_page, 30).navigate()


async def setup(bot: commands.Bot) -> None:
    load_files(bot)

    bot.tree.add_command(birthday_group)
    bot.tree.add_command(list_birthdays)

    if not happy_birthday.is_running():
        happy_birthday.start()
        print("birthday.py: Happy Birthday task started")
