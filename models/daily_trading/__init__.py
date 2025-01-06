from .collector import DailyTradingCollector
from .processor import DailyTradingProcessor
from .schema import DailyTradingSchema
from ..base_model import BaseModel
from tqdm import tqdm
import time

# 股票日线数据模型
class DailyTrading(BaseModel):
    @classmethod
    def update(cls):
        collector = DailyTradingCollector()
        processor = DailyTradingProcessor()

        # code & name
        stock_list = collector.get_stock_list()

        if stock_list.empty:
            return False

        processed_dfs = []  # 用于存储处理后的数据框
        batch_size = 1000  # 每10个股票的数据作为一批次处理

        # 添加进度条
        with tqdm(total=len(stock_list), desc="更新当日股票数据") as pbar:
            for idx, row in stock_list.iterrows():
                df = collector.get_stock_data(stock_code=row['code'], stock_name=row['name'])
                if not df.empty:
                    processed_df = processor.process_data(df, row['name'])
                    processed_dfs.append(processed_df)

                # 当累积了batch_size个数据框或处理到最后一个股票时，进行批量保存
                if len(processed_dfs) >= batch_size or idx == len(stock_list) - 1:
                    if processed_dfs:  # 确保有数据要保存
                        success = processor.batch_save_to_db(processed_dfs)
                        if not success:
                            return False
                        processed_dfs = []  # 清空列表，准备下一批次
                
                pbar.update(1)  # 更新进度条
                pbar.set_postfix({'股票': f"{row['code']} {row['name']}"})  # 显示当前处理的股票信息

        return True
    
    @classmethod
    def update_all(cls):
        collector = DailyTradingCollector()
        processor = DailyTradingProcessor()

        # code & name
        stock_list = collector.get_stock_list()

        if stock_list.empty:
            return False

        processed_dfs = []  # 用于存储处理后的数据框
        batch_size = 100  # 每100个股票的数据作为一批次处理

        # 添加进度条
        with tqdm(total=len(stock_list), desc="更新历史股票数据") as pbar:
            for idx, row in stock_list.iterrows():
                df = collector.get_stock_data(stock_code=row['code'], start_date='20000103', end_date='20100101', stock_name=row['name'])
                if not df.empty:# 记录处理开始时间
                    processed_df = processor.process_data(df, row['name'])
                    processed_dfs.append(processed_df)

                # 当累积了batch_size个数据框或处理到最后一个股票时，进行批量保存
                if len(processed_dfs) >= batch_size or idx == len(stock_list) - 1:
                    if processed_dfs:  # 确保有数据要保存
                        success = processor.batch_save_to_db(processed_dfs)
                        if not success:
                            return False
                        processed_dfs = []  # 清空列表，准备下一批次
                
                pbar.update(1)  # 更新进度条
                pbar.set_postfix({'股票': f"{row['code']} {row['name']}"})  # 显示当前处理的股票信息

        return True

    @classmethod
    def get_description(cls):
        return DailyTradingSchema.description

    @classmethod
    def get_schema(cls):
        return DailyTradingSchema 