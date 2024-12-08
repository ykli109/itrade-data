from loguru import logger
from models.daily_trading import DailyTrading
from models.trade_date import TradeDate

MODELS = {
    '1': ('股票日线数据', DailyTrading),
    '2': ('交易日历数据', TradeDate),
}

def init_all_tables():
    """初始化所有数据表"""
    for _, model in MODELS.values():
        model.init_table()

def show_menu():
    """显示菜单"""
    print("\n请选择要更新的数据：")
    for key, (desc, _) in MODELS.items():
        print(f"{key}. {desc}")
    print("q. 退出程序")

def main():
    logger.add("logs/stock_data_{time:YYYY-MM-DD}.log", rotation="1 day", retention="7 days")
    
    try:
        init_all_tables()
        
        while True:
            show_menu()
            choice = input("请输入选项: ").strip()
            
            if choice.lower() == 'q':
                break
                
            if choice in MODELS:
                desc, model = MODELS[choice]
                print(f"\n开始更新{desc}...")
                if model.update():
                    print(f"{desc}更新成功")
                else:
                    print(f"{desc}更新失败")
            else:
                print("无效的选项，请重新选择")

    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")

if __name__ == "__main__":
    main() 