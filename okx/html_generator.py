# 账户余额数据
testData = {
    'code': '0',
    'data': [{
        'adjEq': '',
        'borrowFroz': '',
        'details': [
            {
                'accAvgPx': '',
                'availBal': '0.0058828260222429',
                'availEq': '0.0058828260222429',
                'borrowFroz': '',
                'cashBal': '0.0058828260222429',
                'ccy': 'ANIME',
                'clSpotInUseAmt': '',
                'crossLiab': '',
                'disEq': '0.0001313517394246',
                'eq': '0.0058828260222429',
                'eqUsd': '0.0001641896742808',
                'fixedBal': '0',
                'frozenBal': '0',
                'imr': '0',
                'interest': '',
                'isoEq': '0',
                'isoLiab': '',
                'isoUpl': '0',
                'liab': '',
                'maxLoan': '',
                'maxSpotInUse': '',
                'mgnRatio': '',
                'mmr': '0',
                'notionalLever': '0',
                'openAvgPx': '',
                'ordFrozen': '0',
                'rewardBal': '0',
                'smtSyncEq': '0',
                'spotBal': '',
                'spotCopyTradingEq': '0',
                'spotInUseAmt': '',
                'spotIsoBal': '0',
                'spotUpl': '',
                'spotUplRatio': '',
                'stgyEq': '0',
                'totalPnl': '',
                'totalPnlRatio': '',
                'twap': '0',
                'uTime': '1738856784274',
                'upl': '0',
                'uplLiab': ''
            },
            {
                'accAvgPx': '',
                'availBal': '0.0132600830166578',
                'availEq': '0.0132600830166578',
                'borrowFroz': '',
                'cashBal': '0.0132600830166578',
                'ccy': 'DUCK',
                'clSpotInUseAmt': '',
                'crossLiab': '',
                'disEq': '0.0000346141207067',
                'eq': '0.0132600830166578',
                'eqUsd': '0.0000432676508834',
                'fixedBal': '0',
                'frozenBal': '0',
                'imr': '0',
                'interest': '',
                'isoEq': '0',
                'isoLiab': '',
                'isoUpl': '0',
                'liab': '',
                'maxLoan': '',
                'maxSpotInUse': '',
                'mgnRatio': '',
                'mmr': '0',
                'notionalLever': '0',
                'openAvgPx': '',
                'ordFrozen': '0',
                'rewardBal': '0',
                'smtSyncEq': '0',
                'spotBal': '',
                'spotCopyTradingEq': '0',
                'spotInUseAmt': '',
                'spotIsoBal': '0',
                'spotUpl': '',
                'spotUplRatio': '',
                'stgyEq': '0',
                'totalPnl': '',
                'totalPnlRatio': '',
                'twap': '0',
                'uTime': '1738771126576',
                'upl': '0',
                'uplLiab': ''
            },
            {
                'accAvgPx': '',
                'availBal': '580.7314892110919',
                'availEq': '580.7314892110919',
                'borrowFroz': '',
                'cashBal': '580.7314892110919',
                'ccy': 'USDT',
                'clSpotInUseAmt': '',
                'crossLiab': '',
                'disEq': '838.7041462400098',
                'eq': '838.720920658423',
                'eqUsd': '838.7041462400098',
                'fixedBal': '0',
                'frozenBal': '257.989431447331',
                'imr': '0',
                'interest': '',
                'isoEq': '257.989431447331',
                'isoLiab': '',
                'isoUpl': '-81.03761999999875',
                'liab': '',
                'maxLoan': '',
                'maxSpotInUse': '',
                'mgnRatio': '',
                'mmr': '0',
                'notionalLever': '0',
                'openAvgPx': '',
                'ordFrozen': '0',
                'rewardBal': '0',
                'smtSyncEq': '0',
                'spotBal': '',
                'spotCopyTradingEq': '0',
                'spotInUseAmt': '',
                'spotIsoBal': '0',
                'spotUpl': '',
                'spotUplRatio': '',
                'stgyEq': '0',
                'totalPnl': '',
                'totalPnlRatio': '',
                'twap': '0',
                'uTime': '1739402549167',
                'upl': '-81.03761999999875',
                'uplLiab': ''
            }
        ],
        'imr': '',
        'isoEq': '257.9842716587021',
        'mgnRatio': '',
        'mmr': '',
        'notionalUsd': '',
        'notionalUsdForBorrow': '',
        'notionalUsdForFutures': '',
        'notionalUsdForOption': '',
        'notionalUsdForSwap': '',
        'ordFroz': '',
        'totalEq': '838.7043536973349',
        'uTime': '1739409530255',
        'upl': ''
    }],
    'msg': ''
}

def generate_balance_html(data):
    """
    生成账户余额的HTML页面
    :param data: OKX API返回的账户余额数据
    :return: 生成的HTML内容
    """
    # HTML模板
    html_template = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>账户余额</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333;
                padding: 20px;
            }}
            h1 {{
                color: #007bff;
            }}
            .balance-container {{
                background-color: #fff;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }}
            .currency {{
                margin-bottom: 15px;
                padding: 10px;
                border-bottom: 1px solid #eee;
            }}
            .currency:last-child {{
                border-bottom: none;
            }}
            .currency h3 {{
                margin: 0 0 10px;
                color: #333;
            }}
            .currency p {{
                margin: 5px 0;
                color: #666;
            }}
            .highlight {{
                color: #28a745;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>账户余额</h1>
        <div class="balance-container">
            {currency_details}
        </div>
    </body>
    </html>
    """

    # 生成每种货币的HTML
    currency_details = ""
    if data and 'data' in data and len(data['data']) > 0 and 'details' in data['data'][0]:
        for detail in data['data'][0]['details']:
            currency_details += f"""
            <div class="currency">
                <h3>{detail['ccy']}</h3>
                <p>可用余额: <span class="highlight">{detail['availBal']}</span></p>
                <p>总余额: <span class="highlight">{detail['eq']}</span></p>
                <p>折合美元: <span class="highlight">{detail['eqUsd']}</span></p>
            </div>
            """

    # 填充HTML模板
    return html_template.format(currency_details=currency_details)

def save_balance_html(html_content, filename="account_balance.html"):
    """
    保存HTML内容到文件
    :param html_content: HTML内容
    :param filename: 保存的文件名
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"HTML文件已生成：{filename}")
        return True
    except Exception as e:
        print(f"保存HTML文件失败：{str(e)}")
        return False

# 填充HTML模板
html_content = generate_balance_html(testData)

# 保存为HTML文件
save_balance_html(html_content)