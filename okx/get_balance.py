from dotenv import load_dotenv
import os
import requests
import time
import hmac
import hashlib
import base64
from html_generator import generate_balance_html, save_balance_html

class OKXClient:
    def __init__(self):
        # 加载 .env 文件
        load_dotenv()

        # 从环境变量中获取 API 密钥
        self.api_key = os.getenv("OKX_API_KEY")
        self.api_secret = os.getenv("OKX_API_SECRET")
        self.passphrase = os.getenv("OKX_PASSPHRASE")

        if not self.api_key or not self.api_secret or not self.passphrase:
            raise ValueError("请在 .env 文件中设置 OKX_API_KEY, OKX_API_SECRET 和 OKX_PASSPHRASE")

    def _generate_signature(self, timestamp, method, request_path):
        """生成API请求签名"""
        message = f"{timestamp}{method}{request_path}"
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256
        ).digest()
        return base64.b64encode(signature).decode("utf-8")

    def get_balance(self):
        """获取账户余额"""
        method = "GET"
        request_path = "/api/v5/account/balance"
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        
        # 生成签名
        signature = self._generate_signature(timestamp, method, request_path)

        # 请求头
        headers = {
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": signature,
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": self.passphrase,
        }

        try:
            # 发送请求
            response = requests.get(
                f"https://www.okx.com{request_path}",
                headers=headers
            )
            data = response.json()
            
            # 生成并保存HTML
            html_content = generate_balance_html(data)
            save_balance_html(html_content)
            
            return data
        except Exception as e:
            print(f"获取账户余额失败: {str(e)}")
            return None

def main():
    """主函数"""
    try:
        client = OKXClient()
        balance_data = client.get_balance()
        if balance_data:
            print("账户余额获取成功")
        else:
            print("账户余额获取失败")
    except Exception as e:
        print(f"程序执行失败: {str(e)}")

if __name__ == "__main__":
    main()