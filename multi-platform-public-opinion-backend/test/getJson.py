import re

# 读取 HTML 文件
with open('../titles2.html', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 从第 236 行之后开始提取内容
start_index = 235  # 索引从 0 开始，所以是 235
content = ''.join(lines[start_index:])

# 使用正则表达式提取 BV 号
bv_pattern = r'(BV[A-Za-z0-9]+)'
bv_numbers = re.findall(bv_pattern, content)

# 生成完整的视频链接
video_links = []
for bv in bv_numbers:
    video_link = f'https://www.bilibili.com/video/{bv}'
    video_links.append(video_link)

# 打印视频链接
for link in video_links:
    print(link)