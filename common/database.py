from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
from config.settings import DB_CONFIG
import pandas as pd

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

    def save_df_to_db(self, df: pd.DataFrame, table_name: str, id_column: str = 'id'):
        """保存DataFrame到数据库,自动处理重复数据
        
        Args:
            df (pd.DataFrame): 要保存的数据框
            table_name (str): 表名
            id_column (str, optional): 用于去重的ID列名. 默认为'id'
        """
        try:
            # 检查数据是否已存在
            all_ids = df[id_column].unique()
            query = f"""
                SELECT {id_column} 
                FROM {table_name} 
                WHERE {id_column} IN ({','.join(['%s'] * len(all_ids))})
            """
            params = tuple(all_ids)
            existing_data = pd.read_sql(query, self.engine, params=params)
            
            if not existing_data.empty:
                # 过滤重复数据
                df = df.merge(
                    existing_data[[id_column]], 
                    on=[id_column], 
                    how='left', 
                    indicator=True
                )
                df = df.query('_merge == "left_only"').drop('_merge', axis=1)
                logger.info(f"已过滤 {len(existing_data)} 条重复数据")

            if not df.empty:
                df.to_sql(
                    table_name,
                    self.engine,
                    if_exists='append',
                    index=False,
                    method='multi',
                    chunksize=1000
                )
                logger.info(f"成功保存 {len(df)} 条数据")
            return True
        except Exception as e:
            logger.error(f"数据保存失败: {str(e)}")
            raise

    def batch_save_df_to_db(self, df_list: list, table_name: str, id_column: str = 'id'):
        """批量保存DataFrame列表到数据库
        
        Args:
            df_list (list): DataFrame列表
            table_name (str): 表名
            id_column (str, optional): 用于去重的ID列名. 默认为'id'
        """
        try:
            if not df_list:
                return True
            
            # 合并所有数据框
            combined_df = pd.concat(df_list, ignore_index=True)
            return self.save_df_to_db(combined_df, table_name, id_column)
        except Exception as e:
            logger.error(f"批量保存数据失败: {str(e)}")
            return False 