import akshare as ak
import pandas as pd
from loguru import logger
from common.database import DatabaseManager
from config.settings import TABLE_NAMES
from ..trade_date import TradeDate

class LhbCollector:
    def __init__(self):
        self.db = DatabaseManager()
        self.table_name = TABLE_NAMES['lhb_detail']

    def get_lhb_data(self, start_date: str = None, end_date: str = None, stock_name: str = None):
        """获取单个股票数据"""
        try:
            latest_trade_date = TradeDate.get_latest_trade_date()
            if not start_date:
                start_date = latest_trade_date
            if not end_date:
                end_date = latest_trade_date
            
            # print(f'获取{stock_code}{stock_name if stock_name else ""}')
            df = ak.stock_lhb_detail_em(start_date=start_date, end_date=end_date)
            return df
        except Exception as e:
            logger.error(f"获取龙虎榜数据失败: {str(e)}")
            return pd.DataFrame()
