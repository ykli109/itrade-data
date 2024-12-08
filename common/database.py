from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
from config.settings import DB_CONFIG

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.engine = self._create_engine()
            self._initialized = True

    def _create_engine(self):
        # 检查数据库是否存在
        from sqlalchemy import inspect

        connection_str = (
            f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/"
        )
        engine = create_engine(connection_str)

        # 创建数据库
        with engine.connect() as conn:
            db_exists = conn.execute(text("SHOW DATABASES LIKE :db_name"), {"db_name": DB_CONFIG['database']}).fetchone()
            if not db_exists:
                conn.execute(text(f"CREATE DATABASE {DB_CONFIG['database']}"))
                logger.info(f"数据库 {DB_CONFIG['database']} 创建成功")

        # 重新创建连接到指定数据库的引擎
        return create_engine(f"{connection_str}{DB_CONFIG['database']}")

    def execute_sql(self, sql, params=None):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql), params or {})
                conn.commit()
                return result
        except SQLAlchemyError as e:
            logger.error(f"SQL执行失败: {str(e)}")
            raise

    def create_table(self, create_table_sql):
        try:
            self.execute_sql(create_table_sql)
            logger.info("数据表创建成功")
        except SQLAlchemyError as e:
            logger.error(f"数据表创建失败: {str(e)}")
            raise 