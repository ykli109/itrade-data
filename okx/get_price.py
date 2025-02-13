# import requests

# # 请求参数
# url = "https://www.okx.com/api/v5/market/ticker"
# params = {"instId": "BERA-USDT"}  # 交易对名称

# # 发送请求
# response = requests.get(url, params=params)

# # 处理响应
# if response.status_code == 200:
#     data = response.json()
#     print("最新价格:", data["data"][0]["last"])
# else:
#     print("请求失败，状态码:", response.status_code)

import requests

url = "https://www.okx.com/api/v5/market/candles"
params = {
    "instId": "BTC-USDT",
    "bar": "1D",    # 时间粒度（1天）
    "limit": 10     # 获取最近10条数据
}

response = requests.get(url, params=params)
data = response.json()
print("最近10天K线:", data["data"])