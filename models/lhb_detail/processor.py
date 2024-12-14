import pandas as pd
from common.database import DatabaseManager
from config.settings import TABLE_NAMES
from loguru import logger

class LhbProcessor:
    def __init__(self):
        self.db = DatabaseManager()
        self.table_name = TABLE_NAMES['lhb_detail']

    def process_data(self, df: pd.DataFrame):
        """处理股票数据"""
        if df.empty:
            return df
        
        # 重命名列
        # ['序号', '代码', '名称', '上榜日', '解读', '收盘价', '涨跌幅', '龙虎榜净买额', '龙虎榜买入额',                 
        # '龙虎榜卖出额', '龙虎榜成交额', '市场总成交额', '净买额占总成交比', '成交额占总成交比', '换手率', '流通市值',
        # '上榜原因', '上榜后1日', '上榜后2日', '上榜后5日', '上榜后10日']
        df = df.rename(columns={
            '代码': 'stock_code',
            '名称': 'stock_name', 
            '上榜日': 'trade_date',
            '解读': 'explanation',
            '收盘价': 'close_price',
            '涨跌幅': 'change_percent',
            '龙虎榜净买额': 'lhb_net_buy',
            '龙虎榜买入额': 'lhb_buy_amount',
            '龙虎榜卖出额': 'lhb_sell_amount',
            '龙虎榜成交额': 'lhb_total_amount',
            '市场总成交额': 'market_total_amount',
            '净买额占总成交比': 'net_buy_ratio',
            '成交额占总成交比': 'amount_ratio',
            '换手率': 'turnover_rate',
            '流通市值': 'circulating_market_value',
            '上榜原因': 'listed_reason',
            '上榜后1日': 'after_1_day',
            '上榜后2日': 'after_2_day', 
            '上榜后5日': 'after_5_day',
            '上榜后10日': 'after_10_day'
        })
        # 删除不需要的列
        df = df.drop(columns=['序号'])

        # 增加一个id用来定义唯一数据（日期+股票代码）
        df['id'] = df['trade_date'].astype(str) + '_' + df['stock_code']  # 使用日期和股票代码组合生成唯一id
    
        # 处理日期格式
        df['trade_date'] = pd.to_datetime(df['trade_date']).dt.date


        # 如果多行有相同的id，只保留第一个
        df = df.drop_duplicates(subset='id', keep='first')
        return df

    def save_to_db(self, df: pd.DataFrame):
        """保存数据到数据库"""
        try:
            if df.empty:
                logger.warning("没有数据需要保存")
                return True
                
            return self.db.save_df_to_db(df, self.table_name)
        except Exception as e:
            logger.error(f"保存数据失败: {str(e)}")
            return False

    def batch_save_to_db(self, df_list: list):
        """批量保存数据到数据库"""
        return self.db.batch_save_df_to_db(df_list, self.table_name)