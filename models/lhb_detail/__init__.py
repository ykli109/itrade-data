from .collector import LhbCollector
from .processor import LhbProcessor
from .schema import LhbDetailSchema
from ..base_model import BaseModel

# 股票日线数据模型
class Lhb(BaseModel):
    @classmethod
    def update(cls):
        collector = LhbCollector()
        processor = LhbProcessor()

        print("更新当日龙虎榜")
        df = collector.get_lhb_data()

        if not df.empty:
            processed_df = processor.process_data(df)
            success = processor.save_to_db(processed_df)
            if not success:
                return False
            return True
        else:
            return False
    
    @classmethod
    def update_all(cls):
        collector = LhbCollector()
        processor = LhbProcessor()

        print("更新历史龙虎榜")
        df = collector.get_lhb_data(start_date='20220101')
        if not df.empty:
            processed_df = processor.process_data(df)
            success = processor.save_to_db(processed_df)
            if not success:
                return False
            return True
        else:
            return False

    @classmethod
    def get_description(cls):
        return LhbDetailSchema.description

    @classmethod
    def get_schema(cls):
        return LhbDetailSchema 
    