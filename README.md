# 股票数据采集系统

这是一个用于采集A股市场股票数据的自动化系统。系统使用 akshare 获取股票数据，并将数据存储到 MySQL 数据库中。

## 功能特点

- 自动获取A股所有股票的每日交易数据
- 获取A股市场的交易日历数据
- 数据自动清洗和标准化
- 支持增量更新，避免重复数据
- 模块化设计，易于扩展
- 完善的日志记录

## 环境要求

- Python 3.7+
- MySQL 5.7+

## 安装步骤

1. 克隆项目到本地
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```
3. 创建 `.env` 文件，配置数据库连接信息：
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_DATABASE=stock_data
   ```

## 使用方法

1. 确保 MySQL 服务已启动
2. 运行主程序：
   ```bash
   python main.py
   ```
3. 根据菜单提示选择要更新的数据：
   - 1: 更新股票日线数据
   - 2: 更新交易日历数据
   - q: 退出程序

## 数据库结构

### 股票日线数据表 (stock_daily_trading)

- trade_date: 交易日期
- stock_code: 股票代码
- stock_name: 股票名称
- open_price: 开盘价
- high_price: 最高价
- low_price: 最低价
- close_price: 收盘价
- volume: 成交量
- amount: 成交额
- turnover_rate: 换手率
- change_percent: 涨跌幅

### 交易日历表 (stock_trade_date)

- trade_date: 交易日期

## 项目结构

stock_data/
├── common/                 # 公共组件
│   ├── database.py        # 数据库管理
│   └── utils.py           # 工具函数
├── config/                # 配置文件
│   └── settings.py        # 系统配置
├── models/                # 数据模型
│   ├── base_model.py     # 模型基类
│   ├── daily_trading/    # 日线数据模块
│   │   ├── collector.py  # 数据采集
│   │   ├── processor.py  # 数据处理
│   │   └── schema.py     # 表结构
│   └── trade_date/       # 交易日历模块
│       ├── collector.py
│       ├── processor.py
│       └── schema.py
└── main.py               # 主程序
```

## 注意事项

1. 首次运行时会自动创建所有必要的数据表
2. 程序会自动处理重复数据，无需担心数据重复问题
3. 所有操作日志都会保存在 `logs` 目录下
4. 每个数据模块都是独立的，可以单独更新

## 扩展新功能

要添加新的数据采集功能，只需：

1. 在 `models` 目录下创建新的模块目录
2. 实现 collector、processor 和 schema 类
3. 在 `config/settings.py` 中添加新表名
4. 在 `main.py` 的 `MODELS` 字典中注册新模块