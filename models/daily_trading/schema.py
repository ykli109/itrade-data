from config.settings import TABLE_NAMES

class DailyTradingSchema:
    name = TABLE_NAMES['daily_trading']
    description = "股票日线数据"
    
    @staticmethod
    def get_create_table_sql():
        return f"""
        CREATE TABLE IF NOT EXISTS {DailyTradingSchema.name} (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            trade_date DATE NOT NULL,
            stock_code VARCHAR(10) NOT NULL,
            stock_name VARCHAR(50) NOT NULL,
            open_price DECIMAL(10, 2),
            high_price DECIMAL(10, 2),
            low_price DECIMAL(10, 2),
            close_price DECIMAL(10, 2),
            volume BIGINT,
            amount DECIMAL(20, 2),
            turnover_rate DECIMAL(10, 2),
            change_percent DECIMAL(10, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY idx_stock_date (stock_code, trade_date)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """ 