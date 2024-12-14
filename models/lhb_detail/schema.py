from config.settings import TABLE_NAMES

class LhbDetailSchema:
    name = TABLE_NAMES['lhb_detail']
    description = "龙虎榜"
    
    @staticmethod
    def get_create_table_sql():
        return f"""
        CREATE TABLE IF NOT EXISTS {LhbDetailSchema.name} (
            id VARCHAR(50) PRIMARY KEY,                           -- 唯一标识(日期_股票代码)
            trade_date DATE NOT NULL,                            -- 上榜日期
            stock_code VARCHAR(10) NOT NULL,                     -- 股票代码
            stock_name VARCHAR(50) NOT NULL,                     -- 股票名称
            explanation TEXT,                                    -- 解读
            close_price DECIMAL(10, 2),                         -- 收盘价
            change_percent DECIMAL(10, 2),                      -- 涨跌幅
            lhb_net_buy DECIMAL(20, 2),                        -- 龙虎榜净买额
            lhb_buy_amount DECIMAL(20, 2),                     -- 龙虎榜买入额
            lhb_sell_amount DECIMAL(20, 2),                    -- 龙虎榜卖出额
            lhb_total_amount DECIMAL(20, 2),                   -- 龙虎榜成交额
            market_total_amount DECIMAL(20, 2),                -- 市场总成交额
            net_buy_ratio DECIMAL(10, 2),                      -- 净买额占总成交比
            amount_ratio DECIMAL(10, 2),                       -- 成交额占总成交比
            turnover_rate DECIMAL(10, 2),                      -- 换手率
            circulating_market_value DECIMAL(20, 2),           -- 流通市值
            listed_reason VARCHAR(100),                        -- 上榜原因
            after_1_day DECIMAL(10, 2),                       -- 上榜后1日涨跌幅
            after_2_day DECIMAL(10, 2),                       -- 上榜后2日涨跌幅
            after_5_day DECIMAL(10, 2),                       -- 上榜后5日涨跌幅
            after_10_day DECIMAL(10, 2),                      -- 上榜后10日涨跌幅
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    -- 创建时间
            
            INDEX idx_trade_date (trade_date),                -- 交易日期索引
            INDEX idx_stock_code (stock_code)                 -- 股票代码索引
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """ 