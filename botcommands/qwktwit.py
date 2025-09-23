import requests
import discord
from discord import Message
from discord.ext import commands
import asyncio
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import os

dirname = os.path.dirname(__file__)
valid_links = ["www.x.com/", "https://x.com/",]

def is_valid_twitter_link(user_input: str) -> bool:

    for link in valid_links:
        link_length = len(link)
        if user_input[:link_length] == link:
            return True

    return False

async def twitter_downloader(link: str) -> str:

    tweet_link = link
    import requests

    cookies = {
        '_ga': 'GA1.1.513168944.1719875520',
        'XSRF-TOKEN': 'eyJpdiI6ImxaK0VyU1pubkhLMUw0S09uU2dCSHc9PSIsInZhbHVlIjoia05DSitRdHdOcTA3bW9uS0xUR2M4eUZTOS8zM09FVXk5S2YrL0hxNEpicWlPV2RUcUhXU21HSG8xRkR3NmFYYldkRVgwaVVOL2FpNzJGaDJtZ0xVOGw3c1FjaUNVVXRyRVRwRmlyb0d5VkpFT05KNVpRb05NUWhRQXRlejlEWjciLCJtYWMiOiI3MTViMjk4NDBjOGQ1ZTQ5ODk5Mzg5YWQ1ZmI2YzFhNTQyMTUwOThkNzIzZmRkYTY4Yjc1YTMxMGEzZGU5MDM4IiwidGFnIjoiIn0%3D',
        'twitsave_session': 'eyJpdiI6IllsNzJwZ1llWUh3cEZ6b2c4VURyL2c9PSIsInZhbHVlIjoiK3pBSnRmREdOU1c0cnlYcmJXcmJVcHlMcFU3Y1pJcTdWaWV1cEcvTjhjTlBqT2tBdm1ocFRtQ3EyVXlTV1N4QXA1ZFg5MVovR2oxeTkzNEd2S1N1dE1BZVpXaW5mUkowSHQ1OWg2a1pySWRmR1N3Z3ZmenBpQTFWL0lOUnNyRzYiLCJtYWMiOiI4MzNlOTM4MTU5YTU2ZmRjYTMxZWYwNDVkNzQxYjdkNTI0MzI2NjQ2ZmQ4MmYyMzhkMTdkY2FkZjQ5OWQzNzFmIiwidGFnIjoiIn0%3D',
        '_ga_0WHXEN5JDY': 'GS1.1.1719875519.1.1.1719875735.0.0.0',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': '_ga=GA1.1.513168944.1719875520; XSRF-TOKEN=eyJpdiI6ImxaK0VyU1pubkhLMUw0S09uU2dCSHc9PSIsInZhbHVlIjoia05DSitRdHdOcTA3bW9uS0xUR2M4eUZTOS8zM09FVXk5S2YrL0hxNEpicWlPV2RUcUhXU21HSG8xRkR3NmFYYldkRVgwaVVOL2FpNzJGaDJtZ0xVOGw3c1FjaUNVVXRyRVRwRmlyb0d5VkpFT05KNVpRb05NUWhRQXRlejlEWjciLCJtYWMiOiI3MTViMjk4NDBjOGQ1ZTQ5ODk5Mzg5YWQ1ZmI2YzFhNTQyMTUwOThkNzIzZmRkYTY4Yjc1YTMxMGEzZGU5MDM4IiwidGFnIjoiIn0%3D; twitsave_session=eyJpdiI6IllsNzJwZ1llWUh3cEZ6b2c4VURyL2c9PSIsInZhbHVlIjoiK3pBSnRmREdOU1c0cnlYcmJXcmJVcHlMcFU3Y1pJcTdWaWV1cEcvTjhjTlBqT2tBdm1ocFRtQ3EyVXlTV1N4QXA1ZFg5MVovR2oxeTkzNEd2S1N1dE1BZVpXaW5mUkowSHQ1OWg2a1pySWRmR1N3Z3ZmenBpQTFWL0lOUnNyRzYiLCJtYWMiOiI4MzNlOTM4MTU5YTU2ZmRjYTMxZWYwNDVkNzQxYjdkNTI0MzI2NjQ2ZmQ4MmYyMzhkMTdkY2FkZjQ5OWQzNzFmIiwidGFnIjoiIn0%3D; _ga_0WHXEN5JDY=GS1.1.1719875519.1.1.1719875735.0.0.0',
        'referer': 'https://twitsave.com/',
        'sec-ch-ua': '"Opera GX";v="109", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0',
    }

    params = {
        'url': tweet_link,
    }


    start = time.time()

    response = requests.get('https://twitsave.com/info', params=params, cookies=cookies, headers=headers)
    while str(response.text) == "":
        await asyncio.sleep(10)
        response = requests.get('https://twitsave.com/info', params=params, cookies=cookies, headers=headers)

    end = time.time()


    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    video_download = soup.find(class_="font-medium text-sm text-slate-600 hover:text-slate-800 block py-1.5 px-3") #pyright:ignore
    cut_link = str(video_download).partition('">')[0]
    link_index = cut_link.find('https')
    download_link = cut_link[link_index:]
    print(download_link)
    req = urllib.request.Request(download_link, None, headers)
    res = urllib.request.urlopen(req)
    video_title = "tweet"
    filename = os.path.join(dirname, f'videos/{video_title}.mp4')
    with open(filename, "wb") as output:
        while True:
            data = res.read(4096)
            if data:
                output.write(data)
            else:
                break

    return filename

@commands.hybrid_command(name="qwktwit")
async def qwktwit(ctx: commands.Context, link: str) -> None:
    try:
        filename = await twitter_downloader(link)
        await ctx.send(file=discord.File(filename))
        os.remove(filename)
    except Exception as e:
        await ctx.send("That is an invalid twitter link.", ephemeral=True)
        print(e)
    print(f"qwktok.py: qwktok({link})")

async def on_message(message: Message) -> None:
    user_input = message.content
    suppress: bool = True
    for embed in message.embeds:
        if is_valid_twitter_link(str(embed.description)):
            user_input = str(embed.description)
            suppress = False
    if is_valid_twitter_link(user_input):
        reply_message = await message.reply("Attempting to Download and Send Tweet")
        try:
            filename = await twitter_downloader(user_input)
            if filename == "TypeError":
                return
            await message.reply(file=discord.File(filename))
            os.remove(filename)
            if suppress:
                await message.edit(suppress=True)
        except Exception as e:
            print(e)
        await reply_message.delete()

async def setup(bot: commands.Bot):
    bot.add_command(qwktwit)
    bot.add_listener(on_message)
