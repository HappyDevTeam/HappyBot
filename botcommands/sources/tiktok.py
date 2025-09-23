import requests
import re
from botcommands.sources.common import video_downloader

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
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}
VALID_URL = r'(.*\.)?tiktok\.com'
DOWNLOADER = "https://ssstik.io/abc"


async def download(user_input: str) -> str:
    url: str = user_input
    if 'video' not in user_input:
        url = requests.get(url).url

    url_split: list[str] = re.split('[/?&]', url)
    filename: str = ""
    for index, word in enumerate(url_split):
        if word == "video":
            video_id: str = url_split[index + 1]
            filename = await video_downloader(video_id, url, DOWNLOADER, HEADERS)

    return filename


def is_valid(url: str) -> bool:
    if re.search(VALID_URL, url):
        return True
    return False
