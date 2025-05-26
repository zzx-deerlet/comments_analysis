import re

import requests
from bs4 import BeautifulSoup

from enum import Enum

from fake_useragent import UserAgent

from myConfig import webCookies

order_dict = {
    "综合排序": "",
    "最多播放": "click",
    "最新发布": "pubdate",
    "最多弹幕": "dm",
    "最多收藏": "stow",
}
ua = UserAgent()
headers = {
    "User-Agent": ua.random,
    "accept": "application/json, text/plain, */*",
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    "If-Modified-Since": "Tue, 141 May 2024 09:00:23 GMT",
    "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    "Sec-Ch-Ua-Mobile": '?0',
    'Sec-Ch-Ua-Platform': "Windows",
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    "Cookie": webCookies.BilibiliCookies
}


def search_bilibili(search_keyword, search_order):
    url = f"https://search.bilibili.com/all?keyword={search_keyword}&order={search_order}"
    response = requests.get(url=url, headers=headers)
    print(response)
    return response.text


    # soup = BeautifulSoup(response.text, 'html.parser')
    #
    # video_list = []
    # videos = soup.find_all('li', class_='video-item matrix')
    # for video in videos:
    #     title = video.find('a', class_='title').text
    #     link = "https:" + video.find('a', class_='title')['href']
    #     views = video.find('span', class_='so-icon watch-num').text
    #     video_list.append((title, link, views))
    #
    # return video_list


keyword = "陶喆"
order = order_dict["最新发布"]
lines = search_bilibili(search_keyword=keyword, search_order=order)

# 从第 236 行之后开始提取内容
start_index = 235  # 索引从 0 开始，所以是 235
content = ''.join(lines[start_index:])

# 使用正则表达式提取 BV 号
bv_pattern = r'(BV[A-Za-z0-9]+)'
bv_numbers = re.findall(bv_pattern, content)
print(bv_numbers)
# 生成完整的视频链接
video_links = []
for bv in bv_numbers:
    video_link = f'https://www.bilibili.com/video/{bv}'
    video_links.append(video_link)

# 打印视频链接
for link in video_links:
    print(link)


# videos = search_bilibili(search_keyword=keyword, search_order=order)
# for video in videos:
# print(f"标题: {video[0]}, 链接: {video[1]}, 播放量: {video[2]}")
