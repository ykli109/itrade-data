from config.settings import TABLE_NAMES

class DailyTradingSchema:
    name = TABLE_NAMES['daily_trading']
    description = "股票日线数据"
    @staticmethod
    def get_field_comments():
        return {
            'id': '唯一标识(交易日期_股票代码)',
            'trade_date': '交易日期',
            'stock_code': '股票代码',
            'stock_name': '股票名称',
            'open_price': '开盘价',
            'high_price': '最高价',
            'low_price': '最低价', 
            'close_price': '收盘价',
            'volume': '成交量',
            'amount': '成交额',
            'amplitude': '振幅',
            'change_percent': '涨跌幅',
            'change_amount': '涨跌额',
            'turnover_rate': '换手率',
            'prev_close': '前一日收盘价',
            'is_up_limit': '是否涨停',
            'is_down_limit': '是否跌停',
            'created_at': '创建时间'
        }
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
            prev_close DECIMAL(10, 2),
            is_up_limit TINYINT(1) DEFAULT 0,
            is_down_limit TINYINT(1) DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_trade_date (trade_date),
            INDEX idx_stock_code (stock_code)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """ 