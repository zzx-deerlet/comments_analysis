import requests


class BaiduNLPAPI:
    """百度云自然语言处理 (NLP) API 工具类"""

    def __init__(self, api_key: str, secret_key: str):
        """
        初始化配置
        :param api_key: 百度云控制台获取的 API Key
        :param secret_key: 百度云控制台获取的 Secret Key
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = self._get_access_token()  # 初始化时自动获取 Token

    def _get_access_token(self) -> str:
        """
        私有方法：获取访问令牌 (Access Token)
        :return: 有效的 Token 字符串
        :raises: 请求失败时抛出异常
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()  # 抛出 HTTP 错误
            return response.json()["access_token"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"获取 Token 失败: {str(e)}") from e

    def sentiment_classify(self, text: str, charset: str = "GBK") -> dict:
        """
        情感倾向分析接口
        :param text: 待分析的文本内容（最大 2048 字符）
        :param charset: 文本编码格式（可选，默认 GBK，支持 UTF-8）
        :return: 分析结果字典
        :raises: 请求失败时抛出异常
        """
        if len(text) > 2048:
            raise ValueError("文本长度超过限制（最大 2048 字符）")

        # 拼接带 Token 的 API 地址
        api_url = f"https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token={self.access_token}"
        if charset.upper() == "UTF-8":
            api_url += "&charset=UTF-8"

        headers = {"Content-Type": "application/json"}
        payload = {"text": text}

        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()  # 抛出 HTTP 错误
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"情感分析请求失败: {str(e)}") from e
