import discord
from discord import Message
from discord.ext import commands
import asyncio
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import os

dirname = os.path.dirname(__file__)
valid_links = ["https://www.tiktok.com/", "www.tiktok.com/",
               "https://vm.tiktok.com/", "vm.tiktok.com/"]


def is_valid_tiktok_link(user_input: str) -> bool:

    for link in valid_links:
        link_length = len(link)
        if user_input[:link_length] == link:
            return True

    return False


async def tiktok_downloader(link: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'HX-Request': 'true',
        'HX-Trigger': '_gcaptcha_p)t',
        'HX-Target': 'target',
        'HX-Current-URL': 'https://ssstik.io/en',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://ssstik.io',
        'Alt-Used': 'ssstik.io',
        'Connection': 'keep-alive',
        'Referer': 'https://ssstik.io/en',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Priority': 'u=1',
        # Requests doesn't support trailers
        # 'TE': 'trailers',e
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'a205SDQ_',
    }

    start = time.time()

    response = requests.post('https://ssstik.io/abc', params=params, headers=headers, data=data)
    while str(response.text) == "":
        await asyncio.sleep(10)
        response = requests.post('https://ssstik.io/abc', params=params, headers=headers,
                                 data=data)

    end = time.time()

    print("TIME TAKEN TO DOWNLOAD TIKTOK:" + str(end - start))

    download_soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    try:
        download_link: str = download_soup.a["href"]  # pyright: ignore
    except TypeError:
        return "TypeError"
    tiktok = urlopen(download_link)

    video_title = "tiktok"
    filename = os.path.join(dirname, f'videos/{video_title}.mp4')
    with open(filename, "wb") as output:
        while True:
            data = tiktok.read(4096)
            if data:
                output.write(data)
            else:
                break

    return filename


async def on_message(message: Message) -> None:
    user_input = message.content
    suppress: bool = True
    for embed in message.embeds:
        if is_valid_tiktok_link(str(embed.description)):
            user_input = str(embed.description)
            suppress = False
    if is_valid_tiktok_link(user_input):
        reply_message = await message.reply("Attempting to Download and Send TikTok")
        try:
            filename = await tiktok_downloader(user_input)
            if filename == "TypeError":
                return
            await message.reply(file=discord.File(filename))
            os.remove(filename)
            if suppress:
                await message.edit(suppress=True)
        except Exception as e:
            print(e)
        await reply_message.delete()


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
