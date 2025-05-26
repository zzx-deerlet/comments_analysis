import jieba
import pandas as pd
import torch
from app.database.opinion_repository import OpinionRepository

from app.sentiment.local.LSTMAnalysis import building_text_dataset, preprocess_input
from myConfig import LSTMConfig


def doLocalAnalysis():
    model, preprocessor = building_text_dataset(LSTMConfig.max_vocab_size, LSTMConfig.MAX_LEN)

    # 获取数据库操作对象
    opinionRepository = OpinionRepository()

    for i in range(7420, 7430):
        # 获取还未处理的数据
        raw_data = opinionRepository.get_raw_opinion_by_id(i)
        raw_text = raw_data["content"]

        # 预处理输入句子
        input_tensor = preprocess_input(raw_text, preprocessor)

        # 将输入传入模型并进行预测
        with torch.no_grad():  # 不需要计算梯度
            output = model(input_tensor)
            prediction = output.item()  # 获取预测的情感得分

        # 输出结果
        print(f"\n==============第{i}条文本==============")
        print(raw_text)
        print(f"预测的情感得分: {prediction}")
        if prediction >= 0.5:
            print("情感：正面")
        else:
            print("情感：负面")


if __name__ == "__main__":
    doLocalAnalysis()



    # while True:
    #     input_sentence = input("请输入一个句子\n")
    #
    #     # 预处理输入句子
    #     input_tensor = preprocess_input(input_sentence, preprocessor)
    #
    #     # 将输入传入模型并进行预测
    #     with torch.no_grad():  # 不需要计算梯度
    #         output = model(input_tensor)
    #         prediction = output.item()  # 获取预测的情感得分
    #
    #     # 输出结果
    #     print(f"预测的情感得分: {prediction}")
    #     if prediction >= 0.5:
    #         print("情感：正面")
    #     else:
    #         print("情感：负面")
