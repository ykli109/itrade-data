import pandas as pd
from loguru import logger
from common.database import DatabaseManager
from config.settings import TABLE_NAMES

class DailyTradingProcessor:
    def __init__(self):
        self.db = DatabaseManager()
        self.table_name = TABLE_NAMES['daily_trading']

    def process_data(self, df: pd.DataFrame, stock_code: str, stock_name: str):
        """处理股票数据"""
        if df.empty:
            return df
        
        # 重命名列
        df = df.rename(columns={
            '日期': 'trade_date',
            '开盘': 'open_price',
            '最高': 'high_price',
            '最低': 'low_price',
            '收盘': 'close_price',
            '成交量': 'volume',
            '成交额': 'amount',
            '换手率': 'turnover_rate',
            '涨跌幅': 'change_percent'
        })

        # 添加股票信息
        df['stock_code'] = stock_code
        df['stock_name'] = stock_name

        # 处理日期格式
        df['trade_date'] = pd.to_datetime(df['trade_date']).dt.date

        return df

    def save_to_db(self, df: pd.DataFrame):
        """保存数据到数据库"""
        try:
            df.to_sql(
                self.table_name,
                self.db.engine,
                if_exists='append',
                index=False,
                method='multi',
                chunksize=1000
            )
            logger.info(f"成功保存 {len(df)} 条数据")
        except Exception as e:
            logger.error(f"数据保存失败: {str(e)}")
            raise 