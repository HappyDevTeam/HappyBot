import discord
from discord import app_commands
from discord.ext import commands
from discord import Message
from discord import Embed
import requests
from bs4 import BeautifulSoup
import random
import json
from classes.Pagination import Pagination
inconsistencies = {"Friends ‘Til the End":"Friends 'til the End"}

async def getPerks():
    response = requests.get("https://api.nightlight.gg/v1/shrine?pretty=true")
    data = response.text
    perkPOS = data.find("|")
    onlyPerks = data[0:perkPOS]
    res = [s.strip() for s in onlyPerks.split(',')]
    for i in range(0, 4): 
        if res[i] in list(inconsistencies.keys()):
            res[i] = inconsistencies[res[i]]
        res[i] = res[i].replace(" ", "_")
    return res

async def getDescription(perks):

    cookies = {
        'wikia_beacon_id': 'J6RquB0h0j',
        '_b2': '7fsP5wCVqK.1710380267360',
        'Geo': '{%22region%22:%22BC%22%2C%22city%22:%22vancouver%22%2C%22country_name%22:%22canada%22%2C%22country%22:%22CA%22%2C%22continent%22:%22NA%22}',
        '__qca': 'P0-676208460-1710380270411',
        'fandom_global_id': '4acb465c-948d-417e-a5ad-1196de12887d',
        'eb': '87',
        'wikia_session_id': 'xyhLfyD9fe',
        'exp_bucket': '27',
        'exp_bucket_2': 'v2-80',
        '_scor_uid': '5ac39d5f339541f1a68cf9a16a5e823d',
        'fandom_mwuser-sessionId': '93f8cf4c260e96ccc09a',
        'fan_visited_wikis': '2025468,2332006,2293814,1071836,1987696,2974420,5813,2298187,985887,22782,74,2803004,7857,2979208,2294132,2169014',
        'basset': 'icTrafficDivider-0_A_97:false|icConnatixPlayer-0_B_95:true|icPrebidId5-0_A_97:false|icLiveIntentConnectedId-0_B_97:true|icFeaturedVideoPlayer-0_A_75:false',
        'disable_no_video_exp': '1',
        'sessionId': '5ec2abf0-8917-47dc-96ce-969d5fb7f109',
        'tracking_session_id': '5ec2abf0-8917-47dc-96ce-969d5fb7f109',
        '_gid': 'GA1.2.1217895333.1719527492',
        'active_cms_notification': '380',
        'pvNumber': '3',
        'pvNumberGlobal': '3',
        'pv_number_global': '3',
        'pv_number': '3',
        '_ga': 'GA1.1.1963460535.1710380270',
        '_ga_LVKNCJXRLW': 'GS1.1.1719527493.71.1.1719527608.0.0.0',
        'nol_fpid': 'kdwoueqwpr1nthdoewbusmpeixsoo1710380276|1710380276136|1719527608733|1719527571078',
        '__bm_s%23455901': '',
        'AMP_MKTG_6765a55f49': 'JTdCJTdE',
        '_gat': '1',
        'AMP_6765a55f49': 'JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJlODY4MDdhMi04NWJlLTQxMGMtOWViYi1kOGFlZWEzOWQzN2MlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE5NTI3NDkwMzk0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxOTUyODUxNDE0NCUyQyUyMmxhc3RFdmVudElkJTIyJTNBODA2JTdE',
        '_ga_LFNSP5H47X': 'GS1.1.1719527493.69.1.1719528518.0.0.0',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': 'wikia_beacon_id=J6RquB0h0j; _b2=7fsP5wCVqK.1710380267360; Geo={%22region%22:%22BC%22%2C%22city%22:%22vancouver%22%2C%22country_name%22:%22canada%22%2C%22country%22:%22CA%22%2C%22continent%22:%22NA%22}; __qca=P0-676208460-1710380270411; fandom_global_id=4acb465c-948d-417e-a5ad-1196de12887d; eb=87; wikia_session_id=xyhLfyD9fe; exp_bucket=27; exp_bucket_2=v2-80; _scor_uid=5ac39d5f339541f1a68cf9a16a5e823d; fandom_mwuser-sessionId=93f8cf4c260e96ccc09a; fan_visited_wikis=2025468,2332006,2293814,1071836,1987696,2974420,5813,2298187,985887,22782,74,2803004,7857,2979208,2294132,2169014; basset=icTrafficDivider-0_A_97:false|icConnatixPlayer-0_B_95:true|icPrebidId5-0_A_97:false|icLiveIntentConnectedId-0_B_97:true|icFeaturedVideoPlayer-0_A_75:false; disable_no_video_exp=1; sessionId=5ec2abf0-8917-47dc-96ce-969d5fb7f109; tracking_session_id=5ec2abf0-8917-47dc-96ce-969d5fb7f109; _gid=GA1.2.1217895333.1719527492; active_cms_notification=380; pvNumber=3; pvNumberGlobal=3; pv_number_global=3; pv_number=3; _ga=GA1.1.1963460535.1710380270; _ga_LVKNCJXRLW=GS1.1.1719527493.71.1.1719527608.0.0.0; nol_fpid=kdwoueqwpr1nthdoewbusmpeixsoo1710380276|1710380276136|1719527608733|1719527571078; __bm_s%23455901=; AMP_MKTG_6765a55f49=JTdCJTdE; _gat=1; AMP_6765a55f49=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJlODY4MDdhMi04NWJlLTQxMGMtOWViYi1kOGFlZWEzOWQzN2MlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE5NTI3NDkwMzk0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxOTUyODUxNDE0NCUyQyUyMmxhc3RFdmVudElkJTIyJTNBODA2JTdE; _ga_LFNSP5H47X=GS1.1.1719527493.69.1.1719528518.0.0.0',
        'referer': 'https://deadbydaylight.fandom.com/wiki/Windows_of_Opportunity?so=search',
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
        'so': 'search',
    }

    
    response = []
    desc = []
    for i in range(0, 4): 
        response.append(requests.get(
        'https://deadbydaylight.fandom.com/wiki/' + perks[i],
        params=params,
        cookies=cookies,
        headers=headers,
        ))
        soup: BeautifulSoup = BeautifulSoup(response[i].text, "html.parser") #pyright:ignore
        desc.append(soup.find("div",class_="perkDesc divTableCell").get_text()) #pyright:ignore


    return desc
    
    

@commands.hybrid_command(name="roll")
async def roll(ctx: commands.Context, size: int):
    generated_num = random.randint(1, size)
    try:
        await ctx.send(str(generated_num))
    except Exception as e:
        print(e)
    print(f"shrineapi.py: roll()")

@app_commands.command(name="shrine", description="Lists all perks in current Shrine of Secrets!")
async def list_shrine(interaction: discord.Interaction) -> None:
    perks = await getPerks()
    description = await getDescription(perks)
    async def get_page(page: int):
        embed = discord.Embed(title=perks[page - 1], description=description[page - 1])
        total_pages = 4
        embed.set_footer(text=f"Page {page}/{total_pages}")
        return embed, total_pages
    await Pagination(interaction, get_page, 300).navigate()

async def setup(bot: commands.Bot):
    bot.add_command(roll)
    bot.tree.add_command(list_shrine)