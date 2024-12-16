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
    def get_latest_trade_date(cls, need_close: bool = False) -> str:
        """获取最近的交易日
        Args:
            need_close (bool): 是否需要收盘，如果为True，则该交易日15点前返回上一交易日，15点后返回当前交易日
        Returns:
            str: 格式为'YYYYMMDD'的日期字符串
        """
        db = DatabaseManager()
        current_time = datetime.now()
        
        # 先获取最近的交易日
        sql = f"""
            SELECT trade_date
            FROM {TradeDateSchema.name}
            WHERE trade_date <= CURDATE()
            ORDER BY trade_date DESC
            LIMIT 1
        """
        result = db.execute_sql(sql=sql).fetchone()
        
        if not result or not result[0]:
            return ''
        
        latest_trade_date = result[0]
        
        if need_close:
            # 构建最近交易日15点的时间
            close_time = datetime.combine(latest_trade_date, datetime.strptime('15:00:00', '%H:%M:%S').time())
            
            if current_time < close_time:
                # 如果当前时间小于最近交易日的15点，则返回上一个交易日
                sql = f"""
                    SELECT trade_date
                    FROM {TradeDateSchema.name}
                    WHERE trade_date < :latest_date
                    ORDER BY trade_date DESC
                    LIMIT 1
                """
                result = db.execute_sql(sql=sql, params={'latest_date': latest_trade_date}).fetchone()
                if result and result[0]:
                    return result[0].strftime('%Y%m%d')
                return ''
        
        return latest_trade_date.strftime('%Y%m%d')
    
    @classmethod
    def is_trade_date(cls, date_str: str) -> bool:
        """判断是不是交易日
        Args:
            date_str (str): 格式为'YYYYMMDD'的日期字符串
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