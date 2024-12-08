from .collector import DailyTradingCollector
from .processor import DailyTradingProcessor
from .schema import DailyTradingSchema
from ..base_model import BaseModel

# 股票日线数据模型
class DailyTrading(BaseModel):
    @classmethod
    def update(cls):
        collector = DailyTradingCollector()
        processor = DailyTradingProcessor()

        stock_list = collector.get_stock_list()
        if stock_list.empty:
            return False

        for _, row in stock_list.iterrows():
            df = collector.get_stock_data(row['code'])
            if not df.empty:
                processed_df = processor.process_data(df, row['code'], row['name'])
                processor.save_to_db(processed_df)
        return True

    @classmethod
    def get_description(cls):
        return DailyTradingSchema.description

    @classmethod
    def get_schema(cls):
        return DailyTradingSchema 