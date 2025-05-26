from app.database.platform_repository import PlatformRepository

def insert_platforms():
    # 创建 PlatformRepository 实例
    platform_repo = PlatformRepository()

    # 定义要插入的平台信息
    platforms = [
        ("今日头条", "https://www.toutiao.com"),
        ("微博", "https://weibo.com"),
        ("贴吧", "https://tieba.baidu.com"),
        ("知乎", "https://www.zhihu.com"),
        ("B站", "https://www.bilibili.com")
    ]

    # 遍历平台信息列表，插入到平台表中
    for name, base_url in platforms:
        try:
            platform_id = platform_repo.create(name, base_url)
            print(f"成功插入平台 {name}，platform_id: {platform_id}")
        except Exception as e:
            print(f"插入平台 {name} 时出错: {e}")

if __name__ == "__main__":
    insert_platforms()