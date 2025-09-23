import re
from botcommands.sources.common import video_downloader

HEADERS = {
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
VALID_URL = r'(.*\.)?instagram\.com'
GENERAL_DOWNLOADER = "https://reelsvideo.io/reel"


async def download(link: str) -> str:
    url: str = link
    url_split = re.split('[/?&]', url)
    filename: str = ""
    for index, word in enumerate(url_split):
        if word == "reel":
            video_id = url_split[index + 1]
            downloader = GENERAL_DOWNLOADER + "/" + video_id
            filename = await video_downloader(video_id, link, downloader, HEADERS)

    return filename


def is_valid(url: str) -> bool:
    if re.search(VALID_URL, url):
        return True
    return False
