from abc import ABC, abstractmethod
from common.database import DatabaseManager

class BaseModel(ABC):
    @classmethod
    @abstractmethod
    def update(cls):
        """更新数据的抽象方法"""
        pass

    @classmethod
    @abstractmethod
    def get_description(cls):
        """获取数据表描述的抽象方法"""
        pass

    @classmethod
    def init_table(cls):
        """初始化数据表"""
        try:
            db = DatabaseManager()
            create_table_sql = cls.get_schema().get_create_table_sql()
            db.create_table(create_table_sql)
        except AttributeError:
            return False