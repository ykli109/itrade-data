import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_DATABASE', ''),
    'charset': 'utf8mb4'
}

# 各个数据表名称
TABLE_NAMES = {
    'daily_trading': 'stock_daily_trading',
    'trade_date': 'stock_trade_date',
} 