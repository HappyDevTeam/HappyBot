import asyncio
from typing import Mapping, Any
import requests
from bs4 import BeautifulSoup
import os

PARAMS = {
    'url': 'dl',
}
DIRNAME = os.path.dirname(__file__)


async def write_data(
        filename: str,
        url: str,
        headers: Mapping[str, str]
) -> str:
    file_path = os.path.join(DIRNAME, f'../videos/{filename}.mp4')
    video = requests.get(url, params=PARAMS, headers=headers)
    while video.status_code != 200:
        await asyncio.sleep(1)
        video = requests.get(url, params=PARAMS, headers=headers)
    with open(file_path, "wb") as output:
        for chunk in video.iter_content(chunk_size=4096):
            if chunk:
                output.write(chunk)

    return file_path


async def video_downloader(
        video_id: str,
        url: str,
        downloader: str,
        headers: Mapping[str, str]
) -> str:
    data = {
        'id': url,
        'locale': 'en',
        'tt': 'a205SDQ_',
    }

    response = requests.post(downloader, params=PARAMS, headers=headers, data=data)
    while str(response.text) == "":
        await asyncio.sleep(10)
        response = requests.post(downloader, params=PARAMS, headers=headers, data=data)

    download_soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    try:
        html_element: Any = download_soup.find('a', class_='download_link', href=True)
        download_link: str = html_element['href']
        if len(download_link) < 2:
            return ""
    except TypeError:
        return ""

    return await write_data(video_id, download_link, headers)