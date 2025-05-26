import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def spider_bvid(keyword):
    """
    利用seleniume获取搜索结果的bvid，供给后续程序使用
    :param keyword: 搜索关键词
    :return: 生成去重的output_filename = f'{keyword}BV号.csv'
    """
    # 保存的文件名
    input_filename = f'{keyword}BV号.csv'
    service = webdriver.ChromeService(executable_path='chromedriver.exe')
    # 启动爬虫
    options = Options()
    options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=options)  # 设置无界面爬虫
    browser.set_window_size(2800, 1800)  # 设置全屏，注意把窗口设置太小的话可能导致有些button无法点击
    browser.get('https://bilibili.com')
    # 刷新一下，防止搜索button被登录弹框遮住
    browser.refresh()
    print("============成功进入B站首页！！！===========")
    input = browser.find_element(By.CLASS_NAME, 'nav-search-input')
    button = browser.find_element(By.CLASS_NAME, 'nav-search-btn')

    # 输入关键词并点击搜索
    input.send_keys(keyword)
    button.click()
    print(f'==========成功搜索{keyword}相关内容==========')

    # 设置窗口
    all_h = browser.window_handles
    browser.switch_to.window(all_h[1])
    """
    # 这里可以通过xpath或者其他方法找到B站搜索结果页最下方的页码数值
    # 但B站网页代码更改后，显示为34页，网页内容检查后显示为42页（至多）
    # 由于我们的搜索结果很多，肯定超出B站最大显示的42页，故而直接设置最大页数为42
    # 找到最后一个页码所在位置，并获取值
    # total_btn = browser.find_element(By.XPATH,"//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[4]/div/div/button[9]"")
    # //*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[4]/div/div/button[9]
    # total = int(total_btn)
    # print(f'==========成功搜索！ 总页数: {total}==========')
    """

    # B站最多显示42页
    total_page = 42
    # 同样由于B站网页代码的更改，通过找到并点击下一页的方式个人暂不能实现（对，不会分析那个破网页！！！）
    # 因此这里利用总页数进行循环访问来实现自动翻页的效果

    for i in range(0, total_page):
        # url 需要根据不同关键词进行调整内容！！！
        url = (f"https://search.bilibili.com/all?keyword={keyword}"
               f"&from_source=webtop_search&spm_id_from=333.1007&search_source=5&page={i}")

        print(f"===========正在尝试获取第{i + 1}页网页内容===========")
        print(f"===========本次的url为：{url}===========")
        browser.get(url)
        # 这里请求访问网页的时间也比较久(可能因为我是macos)，所以是否需要等待因设备而异
        # 取消刷新并长时间休眠爬虫以避免爬取太快导致爬虫抓取到js动态加载源码
        browser.refresh()
        # print('正在等待页面加载：3')
        # time.sleep(1)
        print('正在等待页面加载：2')
        time.sleep(1)
        print('正在等待页面加载：1')
        time.sleep(1)

        # 直接分析网页
        html = browser.page_source
        # print("网页源码" + html) 用于判断是否获取成功
        soup = BeautifulSoup(html, 'lxml')
        infos = soup.find_all(class_='bili-video-card')
        bv_id_list = []
        for info in infos:
            # 只定位视频链接
            href = info.find('a').get('href')
            # 拆分
            split_url_data = href.split('/')
            # 利用循环删除拆分出现的空白
            for element in split_url_data:
                if element == '':
                    split_url_data.remove(element)
            # 打印检验内容
            # print(split_url_data)
            # 获取bvid
            bvid = split_url_data[2]

            # 利用if语句直接去重
            if bvid not in bv_id_list:
                bv_id_list.append(bvid)
        for bvid in bv_id_list:
            # 写入 input_filename
            print(bvid)
        # 输出提示进度
        print('写入文件成功')
        print("===========成功获取第" + str(i + 1) + "次===========")
        time.sleep(1)
        i += 1

    # 退出爬虫
    browser.quit()

    # 打印信息显示是否成功
    print(f'==========爬取完成。退出爬虫==========')


if __name__ == '__main__':
    spider_bvid("陶喆")
