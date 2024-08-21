import os

# 设置环境变量
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['all_proxy'] = 'socks5://127.0.0.1:7890'

# OpenAI API 配置
API_KEY = "sk-EJOGzWcDlZ2kKjUd806b4cBc6b094fEbB28e17F834EcE945"  # 请替换成您的 API 密钥
BASE_URL = "https://aihubmix.com/v1"
