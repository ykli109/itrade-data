from .collector import TradeDateCollector
from .processor import TradeDateProcessor
from .schema import TradeDateSchema
from ..base_model import BaseModel

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