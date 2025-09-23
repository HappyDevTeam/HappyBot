from typing import Any, Mapping
import discord
from discord import Message
from discord.ext import commands
import asyncio
import time
from bs4 import BeautifulSoup
import requests
import os
import re

HEADERS_TIKTOK = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'HX-Request': 'true',
    'HX-Trigger': '_gcaptcha_pt',
    'HX-Target': 'target',
    'HX-Current-URL': 'https://ssstik.io/en-1',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://ssstik.io',
    'Alt-Used': 'ssstik.io',
    'Connection': 'keep-alive',
    'Referer': 'https://ssstik.io/en-1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

HEADERS_REEL = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'HX-Request': 'true',
    'HX-Trigger': 'main-form',
    'HX-Target': 'target',
    'HX-Current-URL': 'https://reelsvideo.io/',
    'Referer': 'https://reelsvideo.io/',
    'Origin': 'https://reelsvideo.io',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

PARAMS = {
    'url': 'dl',
}

DIRNAME = os.path.dirname(__file__)
VALID_TIKTOK_LINK = r'(.*\.)?tiktok\.com'
VALID_INSTAGRAM_LINKS = ["https://www.instagram.com/", "www.instagram.com/"]

TIKTOK_DOWNLOADER = "https://ssstik.io/abc"
REEL_DOWNLOADER = "https://reelsvideo.io/reel"


async def write_data(filename: str, link: str, headers: Mapping[str, str]) -> str:
    file_path = os.path.join(DIRNAME, f'videos/{filename}.mp4')
    tiktok = requests.get(link, params=PARAMS, headers=headers)
    while tiktok.status_code != 200:
        await asyncio.sleep(1)
        tiktok = requests.get(link, params=PARAMS, headers=headers)
    with open(file_path, "wb") as output:
        for chunk in tiktok.iter_content(chunk_size=4096):
            if chunk:
                output.write(chunk)

    return file_path


async def video_downloader(
        video_id: str,
        link: str,
        downloader: str,
        headers: Mapping[str, str]
) -> str:
    data = {
        'id': link,
        'locale': 'en',
        'tt': 'a205SDQ_',
    }

    start = time.time()

    response = requests.post(downloader, params=PARAMS, headers=headers, data=data)
    while str(response.text) == "":
        await asyncio.sleep(10)
        response = requests.post(downloader, params=PARAMS, headers=headers, data=data)

    end = time.time()

    print("qwktok.py TIME TAKEN TO DOWNLOAD:", end - start)

    download_soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    try:
        html_element: Any = download_soup.find('a', class_='download_link', href=True)
        download_link: str = html_element['href']
        if len(download_link) < 2:
            return ""
    except TypeError:
        return ""
    return await write_data(video_id, download_link, headers)


def is_valid_tiktok_link(user_input: str) -> bool:
    if re.search(VALID_TIKTOK_LINK, user_input):
        return True
    return False


def is_valid_ig_link(user_input: str) -> bool:
    for link in VALID_INSTAGRAM_LINKS:
        link_length = len(link)
        if user_input[:link_length] == link:
            return True
    return False


async def tiktok_downloader(link: str) -> str:
    url: str = link
    if "video" not in link or "photo" not in link:
        url = requests.get(link).url

    url_split = re.split('[/?&]', url)
    filename: str = ""

    for index, word in enumerate(url_split):
        if word == "video":
            video_id = url_split[index + 1]
            filename = await video_downloader(video_id, link, TIKTOK_DOWNLOADER, HEADERS_TIKTOK)

    return filename


async def reel_downloader(link: str) -> str:
    url: str = link
    url_split = re.split('[/?&]', url)
    filename: str = ""

    for index, word in enumerate(url_split):
        if word == "reel":
            video_id = url_split[index + 1]
            downloader = REEL_DOWNLOADER + "/" + video_id
            filename = await video_downloader(video_id, link, downloader, HEADERS_REEL)

    return filename

async def handler(user_input: str) -> str:
    filename: str = ""

    if is_valid_tiktok_link(user_input):
        if not re.search(r'https://', user_input):
            user_input = "https://" + user_input
        try:
            print("qwktok.py: Detected tiktok link")
            filename = await tiktok_downloader(user_input)
            if filename == "":
                print("qwktok.py: Failed to download tiktok")
                return ""
            print("qwktok.py: Tiktok downloaded successfully")
        except Exception as e:
            print(e)

    if is_valid_ig_link(user_input):
        try:
            print("qwktok.py: Detected reel link")
            filename = await reel_downloader(user_input)
            if filename == "":
                print("qwktok.py: Failed to download reel")
                return ""
            print("qwktok.py: Reel downloaded successfully")
        except Exception as e:
            print(e)
    
    return filename

async def on_message(message: Message) -> None:
    user_input = message.content
    suppress: bool = True

    print("qwktok.py: on_message event, author: ", message.author)
    for embed in message.embeds:
        if is_valid_tiktok_link(str(embed.description)):
            user_input = str(embed.description)
            suppress = False
        if is_valid_ig_link(str(embed.description)):
            user_input = str(embed.description)
            suppress = False
    filename: str = await handler(user_input)
    if (filename == ''):
        return
    await message.reply(file=discord.File(filename))
    os.remove(filename)
    if suppress:
        await message.edit(suppress=True)


@commands.hybrid_command(name="qwktok")
async def qwktok(ctx: commands.Context, link: str) -> None:
    try:
        print(link)
        filename: str = await handler(link)
        await ctx.channel.send(file=discord.File(filename))
        os.remove(filename)
    except Exception as e:
        await ctx.send("That is an invalid tiktok link.", ephemeral=True)
        print(e)
    print(f"qwktok.py: qwktok({link})")


async def setup(bot: commands.Bot):
    bot.add_command(qwktok)
    bot.add_listener(on_message)
