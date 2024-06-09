from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests


def tiktok_downloader(link):

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'HX-Request': 'true',
        'HX-Trigger': '_gcaptcha_pt',
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
    download_soup = BeautifulSoup(response.text, "html.parser")

    download_link = download_soup.a["href"]
    tiktok = urlopen(download_link)
    with open(f"videos/tiktok.mp4", "wb") as output:
        while True:
            data = tiktok.read(4096)
            if data:
                output.write(data)
            else:
                break
