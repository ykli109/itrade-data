import akshare as ak
import pandas as pd
from loguru import logger

class TradeDateCollector:
    def fetch_trade_dates(self):
        """获取交易日期数据"""
        try:
            return ak.tool_trade_date_hist_sina()
        except Exception as e:
            logger.error(f"获取交易日期数据失败: {str(e)}")
            return pd.DataFrame() 
        
#       trade_date
# 0     1990-12-19
# 1     1990-12-20
# 2     1990-12-21
# 3     1990-12-24
# 4     1990-12-25
# ...          ...
# 8307  2024-12-25
# 8308  2024-12-26
# 8309  2024-12-27
# 8310  2024-12-30