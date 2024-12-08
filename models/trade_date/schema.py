from config.settings import TABLE_NAMES

class TradeDateSchema:
    name = TABLE_NAMES['trade_date']
    description = "交易日历数据"
    
    @staticmethod
    def get_create_table_sql():
        return f"""
        CREATE TABLE IF NOT EXISTS {TradeDateSchema.name} (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            trade_date DATE NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """ 