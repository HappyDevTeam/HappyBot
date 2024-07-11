import discord
from discord import Message
from discord.ext import commands
import asyncio
import time
from bs4 import BeautifulSoup
import requests
import os
import re

HEADERS = {
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
    # 'Cookie': 'cf_clearance=9ProbLa2R5H2so6LWLxhGL4VbSe4xY6Gr4H1HpYJgNs-1718498522-1.0.1.1-DXBBrZ8M0qbj9QxebLYAoriFhdocCpmrDygmX4DCHjNYSYynYoeF1mH2Kb4eZKiGHBuinNSRaxFSpiOQx8tQdg',
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
VALID_LINKS = ["https://www.tiktok.com/", "www.tiktok.com/",
               "https://vm.tiktok.com/", "vm.tiktok.com/"]


def is_valid_tiktok_link(user_input: str) -> bool:
    for link in VALID_LINKS:
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
            filename = await tiktok_video_downloader(video_id, link)
            break
        if word == "photo":
            break
            # video_id = url_split[index + 1]
            # filename = await tiktok_photo_downloader(video_id)
            # break

    return filename


async def write_data(filename: str, link: str) -> str:
    file_path = os.path.join(DIRNAME, f'videos/{filename}.mp4')
    tiktok = requests.get(link, params=PARAMS, headers=HEADERS)
    while tiktok.status_code != 200:
        await asyncio.sleep(1)
        tiktok = requests.get(link, params=PARAMS, headers=HEADERS)
    with open(file_path, "wb") as output:
        for chunk in tiktok.iter_content(chunk_size=4096):
            if chunk:
                output.write(chunk)

    return file_path


async def tiktok_video_downloader(video_id: str, link: str) -> str:

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'a205SDQ_',
    }

    start = time.time()

    response = requests.post('https://ssstik.io/abc', params=PARAMS, headers=HEADERS, data=data)
    while str(response.text) == "":
        await asyncio.sleep(10)
        response = requests.post('https://ssstik.io/abc', params=PARAMS, headers=HEADERS,
                                 data=data)

    end = time.time()

    print("TIME TAKEN TO DOWNLOAD TIKTOK:" + str(end - start))

    download_soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    try:
        download_link: str = download_soup.a["href"]  # pyright: ignore
        if len(download_link) < 2:
            return ""
    except TypeError:
        return ""
    return await write_data(video_id, download_link)


async def tiktok_photo_downloader(video_id: str) -> str:
    return await write_data(video_id, f"https://r1.ssstik.top/ssstik/{video_id}")


async def on_message(message: Message) -> None:
    user_input = message.content
    suppress: bool = True
    for embed in message.embeds:
        if is_valid_tiktok_link(str(embed.description)):
            user_input = str(embed.description)
            suppress = False
    if is_valid_tiktok_link(user_input):
        try:
            filename = await tiktok_downloader(user_input)
            if filename == "":
                return
            await message.reply(file=discord.File(filename))
            os.remove(filename)
            if suppress:
                await message.edit(suppress=True)
        except Exception as e:
            print(e)


@commands.hybrid_command(name="qwktok")
async def qwktok(ctx: commands.Context, link: str) -> None:
    try:
        filename = await tiktok_downloader(link)
        await ctx.send(file=discord.File(filename))
        os.remove(filename)
    except Exception as e:
        await ctx.send("That is an invalid tiktok link.", ephemeral=True)
        print(e)
    print(f"qwktok.py: qwktok({link})")


async def setup(bot: commands.Bot):
    bot.add_command(qwktok)
    bot.add_listener(on_message)
