from loguru import logger
from common.database import DatabaseManager
from config.settings import TABLE_NAMES
import pandas as pd

class TradeDateProcessor:
    def __init__(self):
        self.db = DatabaseManager()
        self.table_name = TABLE_NAMES['trade_date']

    def process_trade_dates(self, df: pd.DataFrame):
        """处理交易日期数据并写入数据库"""
        try:
            # 确保列名与数据库表结构一致
            df.columns = ['trade_date']
            df['trade_date'] = pd.to_datetime(df['trade_date']).dt.date
            
            # 使用 SQLAlchemy 的 to_sql 方法保存数据
            df.to_sql(
                self.table_name,
                self.db.engine,
                if_exists='append',
                index=False,
                method='multi',
                chunksize=1000
            )
            logger.info(f"成功保存 {len(df)} 条交易日期数据")
            return True
        except Exception as e:
            logger.error(f"交易日期数据写入数据库失败: {str(e)}")
            return False 