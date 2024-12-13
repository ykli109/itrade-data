import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
from loguru import logger
from common.database import DatabaseManager
from config.settings import TABLE_NAMES

class DailyTradingCollector:
    def __init__(self):
        self.db = DatabaseManager()
        self.table_name = TABLE_NAMES['daily_trading']

    def get_stock_list(self):
        """获取A股股票列表"""
        try:
            return ak.stock_info_a_code_name()
        except Exception as e:
            logger.error(f"获取股票列表失败: {str(e)}")
            return pd.DataFrame()

    def get_stock_data(self, stock_code: str, start_date: str = None, end_date: str = None, stock_name: str = None):
        """获取单个股票数据"""
        try:
            if not start_date:
                start_date = datetime.now().strftime('%Y%m%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y%m%d')
            
            # print(f'获取{stock_code}{stock_name if stock_name else ""}')
            df = ak.stock_zh_a_hist(symbol=stock_code, start_date=start_date, end_date=end_date, adjust='qfq')
            return df
        except Exception as e:
            logger.error(f"获取股票{stock_code}数据失败: {str(e)}")
            return pd.DataFrame()
