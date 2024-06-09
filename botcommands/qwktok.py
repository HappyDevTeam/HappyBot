from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import discord
from discord import Message
from discord.ext import commands
import os
import re

dirname = os.path.dirname(__file__)
valid_links = ["https://www.tiktok.com/", "www.tiktok.com/"]


def tiktok_downloader(link: str) -> str:
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

    response = requests.post('https://ssstik.io/abc', params=params, headers=headers, data=data)
    downloadSoup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink: str = downloadSoup.a["href"]  # pyright: ignore
    urlSplit = re.split('/|\?|&', link)
    videotitle = ""
    for index, word in enumerate(urlSplit):
        print(word)
        if word == "video":
            videotitle = urlSplit[index + 1]
            break
    tiktok = urlopen(downloadLink)
    filename = os.path.join(dirname, f'videos/{videotitle}.mp4')
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
    if message.author.bot:
        return
    if user_input[0:23] == valid_links[0] or user_input[0:15] == valid_links[1]:
        try:
            filename = tiktok_downloader(user_input)
            await message.reply(file=discord.File(filename))
            os.remove(filename)
        except Exception as e:
            print(e)


@commands.hybrid_command(name="qwktok")
async def qwktok(ctx: commands.Context, link: str) -> None:
    try:
        filename = tiktok_downloader(link)
        await ctx.send(file=discord.File(filename))
        os.remove(filename)
    except Exception as e:
        await ctx.send("That is an invalid tiktok link.", ephemeral=True)
        print(e)


async def setup(bot: commands.Bot):
    bot.add_command(qwktok)
    bot.add_listener(on_message)