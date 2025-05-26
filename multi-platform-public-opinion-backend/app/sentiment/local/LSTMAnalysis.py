import re
from collections import Counter

import jieba
import pandas as pd
import seaborn
import torch
from matplotlib import pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
from torch.utils.data import Dataset, DataLoader

from myConfig import LSTMConfig

plt.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei', 'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
plt.rcParams['font.size'] = 12  # 字体大小
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号


class TextPreprocessor:
    """文本预处理器类，用于处理文本数据和构建词汇表"""

    def __init__(self, max_vocab_size=10000, max_len=100):  # 词汇表最大大小，默认10000

        self.word2idx = {}  # 词到索引的映射字典
        self.max_vocab_size = max_vocab_size  # 词汇表大小上限
        self.max_len = max_len  # 文本长度上限

    def clean_text(self, text: str):
        """
        清理文本，移除特殊字符并标准化
        参数:
            text (str): 输入文本
        返回:
            str: 清理后的文本
        """
        text = re.sub(r'[^\w\s]', '', text)  # 移除所有标点符号和特殊字符
        text = text.lower()  # 转换为小写
        text = re.sub(r'\s+', ' ', text).strip()  # 规范化空白字符并去除首尾空格
        return text

    def build_vocab(self, texts):
        """
        构建词汇表
        参数:
            texts (List[str]): 文本列表
        """
        word_counts = Counter()  # 创建词频统计器

        # 对每个文本进行处理和分词
        for text in texts:
            text = self.clean_text(text)  # 清理文本
            word_counts.update(jieba.lcut(text))  # 使用jieba分词并更新词频统计

        # 构建词汇表，包含特殊标记和最常见的词
        vocab = ['<PAD>', '<UNK>'] + [  # PAD用于填充，UNK用于未知词
            word for word, count in word_counts.most_common(self.max_vocab_size)
        ]

        # 创建词到索引和索引到词的映射
        self.word2idx = {word: idx for idx, word in enumerate(vocab)}


class TextDataset(Dataset):

    def __init__(self,
                 texts,  # 文本列表
                 labels,  # 标签列表
                 preprocessor  # 预处理器实例
                 ):
        self.texts = texts
        self.labels = labels
        self.preprocessor = preprocessor

        # 预处理所有文本，避免重复处理
        self.tokenized_texts = [
            jieba.lcut(self.preprocessor.clean_text(text))
            for text in self.texts
        ]

    def __len__(self):
        """返回数据集的大小"""
        return len(self.texts)

    def __getitem__(self, idx):
        """
        获取单个样本
        参数:
            idx (int): 样本索引
        返回:
            tuple: (文本张量, 标签张量)
        """
        tokens = self.tokenized_texts[idx]

        # 将词转换为索引，未知词用UNK的索引替代
        indices = [
            self.preprocessor.word2idx.get(token, self.preprocessor.word2idx['<UNK>'])
            for token in tokens
        ]

        # 处理序列长度：填充或截断
        if len(indices) < self.preprocessor.max_len:
            # 如果长度不足，用PAD填充
            indices += [self.preprocessor.word2idx['<PAD>']] * (self.preprocessor.max_len - len(indices))
        else:
            # 如果超长，截断
            indices = indices[:self.preprocessor.max_len]

        # 转换为PyTorch张量
        return (
            torch.tensor(indices, dtype=torch.long),  # 文本索引序列
            torch.tensor(self.labels[idx], dtype=torch.float32)  # 标签
        )


class EmotionClassifier(torch.nn.Module):
    """情感分类模型"""

    def __init__(self,
                 vocab_size,  # 词汇表大小
                 embedding_dim,  # 词嵌入维度
                 hidden_dim,  # LSTM隐藏层维度
                 num_layers=3,  # LSTM层数
                 dropout=0.3,  # Dropout比率
                 ):
        super().__init__()

        # 词嵌入层，将词索引转换为密集向量
        self.embedding = torch.nn.Embedding(
            vocab_size,  # 词汇表大小
            embedding_dim=embedding_dim,  # 嵌入维度
        )

        # Dropout层，用于防止过拟合
        self.dropout = torch.nn.Dropout(dropout)
        # LSTM层
        self.lstm = torch.nn.LSTM(
            embedding_dim,  # 输入维度
            hidden_dim,  # 隐藏层维度
            num_layers=num_layers,  # LSTM层数
            # 因为LSTM接受的数据输入是(序列长度，batch，输入维数)
            # 这和我们cnn输入的方式不太一致，所以使用batch_first，
            # 我们可以将输入变成(batch，序列长度，输入维数)
            batch_first=True,  # batch在前
            bidirectional=True,  # 是否双向
            dropout=dropout if num_layers > 1 else 0  # 多层时使用dropout
        )

        # 确定LSTM输出维度（双向维度翻倍）
        lstm_output_dim = hidden_dim * 2

        # 全连接层，将LSTM输出映射到标签空间
        self.fc = torch.nn.Linear(lstm_output_dim, 1)

        # sigmoid激活函数，用于二分类
        self.activation = torch.nn.Sigmoid()

    def forward(self, x):
        """
        前向传播
        参数:
            x (torch.Tensor): 输入张量，形状为 (batch_size, sequence_length)
        返回:
            torch.Tensor: 输出张量，形状为 (batch_size, 1)
        """
        # 1. 词嵌入层
        embedded = self.dropout(self.embedding(x))  # (batch_size, sequence_length, embedding_dim)

        # 2. LSTM层
        lstm_out, (hidden, cell) = self.lstm(embedded)
        # print(cell)
        # 3. 处理LSTM输出
        # 对于双向LSTM，连接前向和后向的最后一个隐藏状态
        hidden_out = torch.cat((hidden[-2], hidden[-1]), dim=1)

        # 4. 全连接层
        output = self.fc(self.dropout(hidden_out))

        # 5. sigmoid激活
        # out = self.activation(output)
        return self.activation(output)


def train_model(
        model,  # 待训练的模型
        train_loader,  # 训练数据加载器
        criterion,  # 损失函数
        optimizer,  # 优化器
        num_epochs,  # 训练轮数
        device  # 训练设备(CPU/GPU)
):
    """
    模型训练函数
    返回:
        List[dict]: 训练历史记录
        List[int]:  每轮损失值列表
    """
    model = model.to(device)  # 将模型移到指定设备
    history = []  # 用于记录训练历史
    # train_loss_list = []
    for epoch in range(num_epochs):
        # 训练阶段
        model.train()  # 设置为训练模式
        train_loss = 0

        for batch_x, batch_y in train_loader:
            # 将数据移到指定设备
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)

            # 清零梯度
            optimizer.zero_grad()

            # 前向传播
            outputs = model(batch_x).squeeze()

            # 计算损失
            loss = criterion(outputs, batch_y)

            # 反向传播
            loss.backward()

            # 更新参数
            optimizer.step()

            train_loss += loss.item()

        # train_loss_list.append(train_loss)

        # 验证阶段
        # model.eval()  # 设置为评估模式
        # val_loss = 0
        # correct = 0  # 正确预测数
        # total = 0  # 总样本数

        # with torch.no_grad():  # 不计算梯度
        #     for batch_x, batch_y in val_loader:
        #         batch_x = batch_x.to(device)
        #         batch_y = batch_y.to(device)
        #
        #         # 前向传播
        #         outputs = model(batch_x).squeeze()
        #
        #         # 计算验证损失
        #         val_loss += criterion(outputs, batch_y).item()
        #
        #         # 计算准确率
        #         predicted = (outputs >= 0.5).float()  # 二分类阈值0.5
        #         total += batch_y.size(0)
        #         correct += (predicted == batch_y).sum().item()

        # 记录每个epoch的统计信息
        epoch_stats = {
            'epoch': epoch + 1,
            'train_loss': train_loss / len(train_loader),  # 平均训练损失
            # 'test_loss': val_loss / len(val_loader),  # 平均验证损失
            # 'test_accuracy': correct / total  # 验证准确率
        }
        history.append(epoch_stats)

        # 打印训练状态
        print(f"Epoch {epoch + 1}/{num_epochs}")
        print(f"Train Loss: {epoch_stats['train_loss']:.4f}")
        # print(f"Val Loss: {epoch_stats['val_loss']:.4f}")
        # print(f"Val Accuracy: {epoch_stats['val_accuracy']:.4f}")

    # 绘制损失曲线
    print(history)
    plt.plot(range(1, num_epochs + 1), [hist['train_loss'] for hist in history])
    plt.xlabel("次数")
    plt.ylabel("损失")
    plt.title("训练损失曲线")
    plt.show()

    return history


def evaluate_model(model, test_loader, criterion, device):
    """
    在测试集上评估模型性能
    参数:
        model (torch.nn.Module): 训练好的模型
        test_loader (DataLoader): 测试数据加载器
        criterion (torch.nn.Module): 损失函数
        device (torch.device): 计算设备
    返回:
        None
    """
    model = model.to(device)  # 将模型移到设备（GPU/CPU）
    model.eval()  # 设置模型为评估模式

    test_loss = 0
    correct = 0
    total = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():  # 禁止计算梯度
        for batch_x, batch_y in test_loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)

            # 前向传播
            outputs = model(batch_x).squeeze()  # 输出的形状是(batch_size, 1)

            # 计算损失
            loss = criterion(outputs, batch_y)
            test_loss += loss.item()

            # 计算预测值
            predicted = (outputs >= 0.5).float()  # 二分类阈值0.5
            correct += (predicted == batch_y).sum().item()
            total += batch_y.size(0)

            all_preds.extend(predicted.cpu().numpy())  # 保存预测结果
            all_labels.extend(batch_y.cpu().numpy())  # 保存真实标签

    # 计算准确率
    accuracy = correct / total

    # 打印测试损失和准确率
    print(f'Test Loss: {test_loss / len(test_loader):.4f}')
    print(f'Test Accuracy: {accuracy:.4f}')

    # 生成分类报告
    print("\nClassification Report:")
    print(classification_report(all_labels, all_preds))

    # 生成混淆矩阵
    cm = confusion_matrix(all_labels, all_preds)
    print("\nConfusion Matrix:")
    print(cm)

    # 可视化混淆矩阵
    plt.figure(figsize=(6, 5))
    seaborn.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=["消极", "积极"], yticklabels=["消极", "积极"])
    plt.title("混淆矩阵")
    plt.xlabel("预测值")
    plt.ylabel("真实值")
    plt.show()


def main():
    # 配置训练参数
    BATCH_SIZE = LSTMConfig.BATCH_SIZE
    MAX_LEN = LSTMConfig.MAX_LEN
    VOCAB_SIZE = LSTMConfig.max_vocab_size
    EMBEDDING_DIM = 300
    HIDDEN_DIM = 128
    NUM_EPOCHS = LSTMConfig.NUM_EPOCHS
    LEARNING_RATE = LSTMConfig.LEARNING_RATE

    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # 加载数据
    train_data = pd.read_csv("./data/comprehensive/OK_train.csv")
    test_data = pd.read_csv("./data/comprehensive/OK_test.csv")

    # 初始化预处理器并构建词汇表
    preprocessor = TextPreprocessor(max_vocab_size=VOCAB_SIZE, max_len=MAX_LEN)
    preprocessor.build_vocab(train_data["评论内容"])

    # 创建数据集
    train_dataset = TextDataset(
        train_data["评论内容"].tolist(),
        train_data["情感得分"].tolist(),
        preprocessor
    )
    test_dataset = TextDataset(
        test_data["评论内容"].tolist(),
        test_data["情感得分"].tolist(),
        preprocessor
    )

    # 创建数据加载器
    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True  # 训练时打乱数据
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE
    )

    # 初始化模型
    model = EmotionClassifier(
        vocab_size=len(preprocessor.word2idx),
        embedding_dim=EMBEDDING_DIM,
        hidden_dim=HIDDEN_DIM
    )

    # 定义损失函数和优化器
    criterion = torch.nn.BCELoss()  # 二分类交叉熵损失
    optimizer = torch.optim.Adam(  # Adam优化器
        model.parameters(),
        lr=LEARNING_RATE
    )

    # 训练模型
    history = train_model(model, train_loader, criterion, optimizer, NUM_EPOCHS, DEVICE)

    evaluate_model(model, test_loader, criterion, DEVICE)

    return model, history, preprocessor


# 定义输入句子的预处理
def preprocess_input(input_text: str, preprocessor):
    """
    将输入文本转换为模型可以理解的格式
    """
    # 清理文本
    cleaned_text = preprocessor.clean_text(input_text)

    # 分词
    tokenized_text = jieba.lcut(cleaned_text)

    # 将分词转换为索引
    indices = [
        preprocessor.word2idx.get(token, preprocessor.word2idx['<UNK>'])
        for token in tokenized_text
    ]

    # 填充或截断
    if len(indices) < preprocessor.max_len:
        indices += [preprocessor.word2idx['<PAD>']] * (preprocessor.max_len - len(indices))
    else:
        indices = indices[:preprocessor.max_len]

    result = torch.tensor(indices).unsqueeze(0)  # 增加batch维度

    return result


def building_text_dataset(max_vocab_size, max_len):
    """初始化预处理器并构建词汇表"""
    # 加载数据
    train_data = pd.read_csv(
        r"D:\大三\下\r软件工程\second_demoProject\app\sentiment\local\data\comprehensive\OK_train.csv")

    # 初始化预处理器并构建词汇表
    preprocessor_for_dataset = TextPreprocessor(max_vocab_size=max_vocab_size, max_len=max_len)
    preprocessor_for_dataset.build_vocab(train_data["评论内容"])

    # 加载模型
    model = EmotionClassifier(
        vocab_size=15002,
        embedding_dim=300,
        hidden_dim=128
    )
    model.load_state_dict(
        torch.load(r'D:\大三\下\r软件工程\second_demoProject\app\sentiment\local\emotion_classifier.pth'))
    model.eval()  # 切换到评估模式

    return model, preprocessor_for_dataset

# if __name__ == "__main__":
#     model, history, preprocessor = main()  # 执行主函数
#     # 保存模型
#     torch.save(model.state_dict(), 'emotion_classifier.pth')
#
#     # print(history)
