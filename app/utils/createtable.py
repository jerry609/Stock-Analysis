import numpy as np
import pandas as pd
from sqlalchemy import create_engine

# 数据库连接字符串，请替换成你的实际连接信息
engine = create_engine('mysql+pymysql://root:152189@localhost/stock')

# Excel文件路径
file_path = 'D:\\Pycharm_pro\\flask_\\flaskProject1\\static\\data.xlsx'

# 读取Excel文件
df = pd.read_excel(file_path)

print("Original columns:", df.columns)
print("Number of columns:", len(df.columns))

# 定义期望的列名
expected_columns = ['stock_code', 'change_amount', 'change_rate', 'current_price', 'price_limit_up', 'price_limit_down',
                    'open_price', 'highest_price', 'lowest_price', 'previous_close', 'volume', 'turnover', 'amplitude',
                    'turnover_rate', 'pb_ratio', 'pe_ratio', 'market_cap', 'circulating_market_cap', 'total_shares', 'circulating_shares']

# 确保列名数量匹配
if len(expected_columns) != len(df.columns):
    print("Warning: Number of expected column names does not match the number of columns in the DataFrame.")
    print("Adjusting column names...")
    while len(expected_columns) < len(df.columns):
        expected_columns.append(f'extra_column_{len(expected_columns)}')
    expected_columns = expected_columns[:len(df.columns)]

df.columns = expected_columns

# 数据清洗和转换函数
def clean_percentage(x):
    return pd.to_numeric(x.replace('%', ''), errors='coerce') / 100 if isinstance(x, str) else x

def clean_volume(x):
    if isinstance(x, str):
        x = x.replace('万手', '0000').replace('手', '')
    return pd.to_numeric(x, errors='coerce')

def clean_money(x):
    if isinstance(x, str):
        x = x.replace('万元', '0000').replace('元', '').replace('亿', '00000000')
    return pd.to_numeric(x, errors='coerce')

# 应用数据清洗和转换
df['change_rate'] = df['change_rate'].apply(clean_percentage)
df['turnover_rate'] = df['turnover_rate'].apply(clean_percentage)
df['volume'] = df['volume'].apply(clean_volume)
df['turnover'] = df['turnover'].apply(clean_money)
df['market_cap'] = df['market_cap'].apply(clean_money)
df['circulating_market_cap'] = df['circulating_market_cap'].apply(clean_money)
df['total_shares'] = df['total_shares'].apply(clean_money)
df['circulating_shares'] = df['circulating_shares'].apply(clean_money)

# 将所有列转换为数值类型，非数值替换为NaN
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 替换NaN为None（SQL中的NULL）
df = df.replace({np.nan: None})

# 打印数据类型
print(df.dtypes)

# 打印前几行数据
print(df.head())

# 导入到MySQL数据库，'stock_data'是数据库中的表名
try:
    df.to_sql('stock_data', con=engine, index=False, if_exists='replace')
    print("数据导入成功")
except Exception as e:
    print(f"数据导入失败: {e}")
