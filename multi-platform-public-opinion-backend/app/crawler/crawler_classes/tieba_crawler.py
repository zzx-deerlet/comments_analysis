import re
from time import sleep
import requests
import random
from fake_useragent import UserAgent
from lxml import etree

class TiebaCrawler:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {
            "User-Agent": self.ua.random,
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
        }

    def get_comments(self, tieba_urls, max_page=20):
        all_comments = []
        for url in tieba_urls:
            for page in range(1, max_page + 1):
                wait_seconds = random.uniform(0, 1)
                sleep(wait_seconds)
                full_url = f"{url}?pn={page}"
                r = requests.get(full_url, headers=self.headers)
                html = etree.HTML(r.text)
                text_tags = html.xpath('//*[@class="d_post_content j_d_post_content "]')
                ip_tags = html.xpath('.//*[contains(@class, "post-tail-wrap")]')
                for index in range(len(text_tags)):
                    text = ""
                    text_list = text_tags[index].xpath('./text()')
                    if len(text_list) >= 2:
                        for t in text_list:
                            text = t + text
                    else:
                        text = text_list[0]
                    text = re.sub(r"[ \t\n]+", "", text)
                    comment_data = {
                        'id': None,  # 贴吧评论未明确获取id，可根据实际情况修改
                        'content': text,
                        'publish_time': ip_tags[index].xpath('.//*[contains(@class, "tail-info")]')[-1].text,
                        'extra_info': {
                            'IP属地': ip_tags[index].xpath("./span[1]")[0].text.replace("IP属地:", ""),
                            'page': page
                        }
                    }
                    all_comments.append(comment_data)
        return all_comments