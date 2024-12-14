from .collector import TradeDateCollector
from .processor import TradeDateProcessor
from .schema import TradeDateSchema
from ..base_model import BaseModel
from common.database import DatabaseManager
from datetime import datetime

# 交易日历数据模型
class TradeDate(BaseModel):
    @classmethod
    def update(cls):
        collector = TradeDateCollector()
        processor = TradeDateProcessor()

        df = collector.fetch_trade_dates()
        if not df.empty:
            processor.process_trade_dates(df)
            return True
        return False

    @classmethod
    def get_description(cls):
        return TradeDateSchema.description

    @classmethod
    def get_schema(cls):
        return TradeDateSchema 
    
    @classmethod
    def get_latest_trade_date(cls) -> str:
        """获取最近的交易日
        Returns:
            str: 格式为‘YYYYMMDD’的日期字符串
        """
        db = DatabaseManager()
        sql = f"""
            SELECT trade_date
            FROM {TradeDateSchema.name}
            WHERE trade_date <= CURDATE()
            ORDER BY trade_date DESC
            LIMIT 1
        """
        result = db.execute_sql(sql=sql).fetchone()
        if result and result[0]:
            return result[0].strftime('%Y%m%d')
        return ''
    
    @classmethod
    def is_trade_date(cls, date_str: str) -> bool:
        """判断是不是交易日
        Args:
            date_str (str): 格式为‘YYYYMMDD’的日期字符串
        Returns:
            bool: 是否为交易日
        """
        try:
            date = datetime.strptime(date_str, '%Y%m%d')
            db = DatabaseManager()

            sql = f"""
                SELECT COUNT(1)
                FROM {TradeDateSchema.name}
                WHERE trade_date = :date
            """
            result = db.execute_sql(sql=sql, params={'date': date}).fetchone()
            return result[0] > 0
        except ValueError:
            return False