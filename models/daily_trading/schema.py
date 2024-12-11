from config.settings import TABLE_NAMES

class DailyTradingSchema:
    name = TABLE_NAMES['daily_trading']
    description = "股票日线数据"
    
    @staticmethod
    def get_create_table_sql():
        return f"""
        CREATE TABLE IF NOT EXISTS {DailyTradingSchema.name} (
            id VARCHAR(50) PRIMARY KEY,
            trade_date DATE NOT NULL,
            stock_code VARCHAR(10) NOT NULL,
            stock_name VARCHAR(50) NOT NULL,
            open_price DECIMAL(10, 2),
            high_price DECIMAL(10, 2),
            low_price DECIMAL(10, 2),
            close_price DECIMAL(10, 2),
            volume BIGINT,
            amount DECIMAL(20, 2),
            amplitude DECIMAL(10, 2),
            change_percent DECIMAL(10, 2),
            change_amount DECIMAL(10, 2),
            turnover_rate DECIMAL(10, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_trade_date (trade_date),
            INDEX idx_stock_code (stock_code)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """ 