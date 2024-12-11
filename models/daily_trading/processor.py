import pandas as pd
from loguru import logger
from common.database import DatabaseManager
from config.settings import TABLE_NAMES

class DailyTradingProcessor:
    def __init__(self):
        self.db = DatabaseManager()
        self.table_name = TABLE_NAMES['daily_trading']

    def process_data(self, df: pd.DataFrame, stock_name: str):
        """处理股票数据"""
        if df.empty:
            return df
        
        # 重命名列
        # '日期', '股票代码', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'
        df = df.rename(columns={
            '日期': 'trade_date',
            '股票代码': 'stock_code',  # 添加股票代码
            '开盘': 'open_price',
            '最高': 'high_price',
            '最低': 'low_price',
            '收盘': 'close_price',
            '成交量': 'volume',
            '成交额': 'amount',
            '振幅': 'amplitude',  # 添加振幅
            '涨跌幅': 'change_percent',
            '涨跌额': 'change_amount',  # 添加涨跌额
            '换手率': 'turnover_rate'
        })

        # 添加股票信息
        df['stock_name'] = stock_name

        # 处理日期格式
        df['trade_date'] = pd.to_datetime(df['trade_date']).dt.date

        # 增加一个id用来定义唯一数据（日期+股票代码）
        df['id'] = df['trade_date'].astype(str) + '_' + df['stock_code']  # 使用日期和股票代码组合生成唯一id

        return df

    def save_to_db(self, df: pd.DataFrame):
        """保存数据到数据库"""
        try:
            # 检查数据是否已存在（使用id的组合）
            all_ids = df['id'].unique()
            query = f"""
                SELECT id 
                FROM {self.table_name} 
                WHERE id IN ({','.join(['%s'] * len(all_ids))})
            """
            params = tuple(all_ids)
            existing_data = pd.read_sql(query, self.db.engine, params=params)
            
            if not existing_data.empty:
                # 使用id来过滤重复数据
                df = df.merge(
                    existing_data[['id']], 
                    on=['id'], 
                    how='left', 
                    indicator=True
                )
                df = df.query('_merge == "left_only"').drop('_merge', axis=1)
                logger.info(f"已过滤 {len(existing_data)} 条重复数据")

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

    def batch_save_to_db(self, df_list: list):
        """批量保存数据到数据库"""
        try:
            # 合并所有数据框
            if not df_list:
                return True
                
            combined_df = pd.concat(df_list, ignore_index=True)
            
            # 获取所有唯一的id
            all_ids = combined_df['id'].unique()
            
            # 检查数据是否已存在（使用id的组合）
            query = f"""
                SELECT id 
                FROM {self.table_name} 
                WHERE id IN ({','.join(['%s'] * len(all_ids))})
            """
            params = tuple(all_ids)
            existing_data = pd.read_sql(query, self.db.engine, params=params)
            
            if not existing_data.empty:
                # 使用id来过滤重复数据
                combined_df = combined_df.merge(
                    existing_data[['id']], 
                    on=['id'], 
                    how='left', 
                    indicator=True
                )
                combined_df = combined_df.query('_merge == “left_only”').drop('_merge', axis=1)
                logger.info(f"已过滤 {len(existing_data)} 条重复数据")
            
            if not combined_df.empty:
                # 批量写入数据库
                combined_df.to_sql(
                    self.table_name,
                    self.db.engine,
                    if_exists='append',
                    index=False,
                    method='multi',
                    chunksize=1000
                )
                logger.info(f"成功批量保存 {len(combined_df)} 条数据")
            
            return True
        except Exception as e:
            logger.error(f"批量保存数据失败: {str(e)}")
            return False