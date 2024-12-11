from loguru import logger
from models.daily_trading import DailyTrading
from models.trade_date import TradeDate

MODELS = {
    '1': ('股票日线数据-所有', DailyTrading),
    '2': ('股票日线数据-当日', DailyTrading),
    '3': ('交易日历数据', TradeDate),
}

def init_table(choice):
    """根据选择初始化对应的数据表"""
    if choice in MODELS:
        _, model = MODELS[choice]
        model.init_table()
        logger.info(f"初始化数据表: {model.get_description()}")

def show_menu():
    """显示菜单"""
    print("\n请选择要更新的数据：")
    for key, (desc, _) in MODELS.items():
        print(f"{key}. {desc}")
    print("q. 退出程序")

def main():
    logger.add("logs/stock_data_{time:YYYY-MM-DD}.log", rotation="1 day", retention="7 days")
    
    try:
        while True:
            show_menu()
            choice = input("请输入选项: ").strip()
            
            if choice.lower() == 'q':
                break
                
            if choice in MODELS:
                desc, model = MODELS[choice]
                print(f"\n开始更新{desc}...")
                
                # 在执行更新操作前初始化对应的数据表
                init_table(choice)
                
                if choice == '1':
                    res = model.update_all()
                elif choice == '2':
                    res = model.update()
                else:
                    res = model.update()
                    
                if res:
                    print(f"{desc}更新执行成功")
                else:
                    print(f"{desc}更新执行失败")
            else:
                print("无效的选项，请重新选择")

    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")

if __name__ == "__main__":
    main() 