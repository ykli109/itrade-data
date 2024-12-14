import requests
# import schedule
# import time

def update_akshare_documentation():
    url = "https://akshare.akfamily.xyz/_sources/data/stock/stock.md.txt"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open('akshare_api.md', 'w', encoding='utf-8') as file:
            file.write(response.text)
        print("文档已成功更新。")
    else:
        print(f"更新文档失败，状态码: {response.status_code}")

# 每天定时更新文档
# schedule.every().day.at("00:00").do(update_akshare_documentation)

if __name__ == "__main__":
    update_akshare_documentation()
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1) 