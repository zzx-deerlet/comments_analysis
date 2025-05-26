import time

from app.sentiment.Yun.BaiDuYun import BaiduNLPAPI
from myConfig import BaiDuYunConfig
from app.database.opinion_repository import OpinionRepository

if __name__ == "__main__":
    # BaiduYun 个人账号的 API_KEY
    API_KEY = BaiDuYunConfig.API_KEY

    # BaiduYun 个人账号的 SECRET_KEY
    SECRET_KEY = BaiDuYunConfig.SECRET_KEY

    opinionRepository = OpinionRepository()

    # 初始化客户端
    nlp_client = BaiduNLPAPI(api_key=API_KEY, secret_key=SECRET_KEY)

    try:
        # 调用情感分析接口

        for i in range(7450, 7460):
            raw_data = opinionRepository.get_raw_opinion_by_id(i)
            raw_text = raw_data["content"]
            # print(raw_text)
            result = nlp_client.sentiment_classify(text=raw_text, charset="UTF-8")  # 显式指定 UTF-8 编码
            time.sleep(1)
            # print(raw_data)
            # print(type(raw_data))
            # 解析结果
            if result:
                print(f"\n==============第{i}条文本==============")

                print("原始文本:", result.get("text"))
                items = result.get("items", [])
                if items:
                    item = items[0]
                    sentiment = item["sentiment"]
                    confidence = item["confidence"]
                    positive_prob = item["positive_prob"]
                    negative_prob = item["negative_prob"]

                    # 转换情感描述
                    sentiment_map = {0: "负向", 1: "中性", 2: "正向"}
                    sentiment_desc = sentiment_map.get(sentiment, "未知")

                    print(f"情感倾向: {sentiment_desc}")
                    print(f"置信度: {confidence:.2f}")
                    print(f"积极概率: {positive_prob:.2f}, 消极概率: {negative_prob:.2f}")
                else:
                    print("未获取到分析结果")
    except Exception as e:
        print(f"操作失败: {str(e)}")
