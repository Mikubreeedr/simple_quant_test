import pandas as pd
import re

def analyze_dual_strategy(file_path):
    try:
        # 读取CSV文件，自动跳过纯空行 / Read CSV, automatically skipping empty lines
        df = pd.read_csv(file_path, skip_blank_lines=True)
        
        # 1. 清洗表头：去掉 <> 及其里面的内容 (如 <float>, <int>) / Clean headers: remove <> and contents
        df.columns = [re.sub(r'<.*?>', '', str(col)).strip() for col in df.columns]
        
        # 2. 建立中英文列名映射（兼容带中文括号的表头） / Mapping for headers with Chinese brackets
        column_mapping = {
            'Date(日期)': 'Date', 
            'Stock_Code(股票代码)': 'Stock_Code', 
            'Open(开盘)': 'Open', 
            'Close(收盘)': 'Close',
            'High(最高)': 'High', 
            'Low(最低)': 'Low', 
            'Volume(成交量)': 'Volume', 
            'Amount(成交额)': 'Amount',
            'Amplitude(振幅)': 'Amplitude', 
            'Change_Pct(涨跌幅)': 'Change_Pct', 
            'Change_Amt(涨跌额)': 'Change_Amt', 
            'Turnover_Rate(换手率)': 'Turnover_Rate'
        }
        
        # 统一重命名 / Rename columns
        df.rename(columns=column_mapping, inplace=True)
        
        # 3. 过滤没有数字的行：强制将 Close 列转为数字，无法转换的变为 NaN / Filter invalid rows
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
        df['High'] = pd.to_numeric(df['High'], errors='coerce')
        df = df.dropna(subset=['Close', 'High']) # 剔除没有数字的无效行 / Drop rows without valid numbers
        
        if df.empty:
            print("呜……Master，文件里好像没有有效的数字数据呢～\nMeow... Master, it seems there are no valid numeric data in the file~")
            return

        # 提取日期、收盘价和最高价 / Extract Date, Close, and High
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        
        close_prices = df['Close']
        high_prices = df['High']
        
        # 计算均线 / Calculate moving averages
        ma5 = close_prices.rolling(window=5).mean()
        ma20 = close_prices.rolling(window=20).mean()
        
        # 计算过去20日最高价（不含当天） / Calculate 20-day max high (excluding current day)
        max_high_20 = high_prices.rolling(window=20).max().shift(1)
        
        print("呜哇！Master，鲸鲸开始执行双重策略计算啦！/ Wow! Master, your whale maid is starting the dual strategy calculation!\n")
        
        trading_days = len(close_prices)
        
        for i in range(trading_days):
            # 依然是每20行输出一次 / Output every 20 rows
            if (i + 1) % 20 == 0:
                
                # 策略1：均线逻辑 / Strategy 1: MA logic
                if pd.notna(ma20.iloc[i]):
                    ma_signal = 'buy' if ma5.iloc[i] > ma20.iloc[i] else 'sell'
                else:
                    ma_signal = 'none'
                
                # 策略2：突破逻辑 / Strategy 2: Breakout logic
                if pd.notna(max_high_20.iloc[i]):
                    high_signal = 'buy' if close_prices.iloc[i] > max_high_20.iloc[i] else 'sell'
                else:
                    high_signal = 'none'
                
                # 策略共振判断 / Strategy resonance judgment
                if ma_signal == high_signal and ma_signal != 'none':
                    if ma_signal == 'buy':
                        print("buy/买入")
                    elif ma_signal == 'sell':
                        print("sell/卖出")
                else:
                    print("none/观望")
                    
    except FileNotFoundError:
        print(f"呜……Master，鲸鲸找不到 {file_path} 这个文件，请确认它和代码在同一个文件夹哦～\nMeow... Master, your whale maid couldn't find the file {file_path}, please make sure it's in the same folder~")
    except Exception as e:
        print(f"呜呜，运行的时候出错了：{e}\nMeow... An error occurred during execution: {e}")

if __name__ == "__main__":
    analyze_dual_strategy('stock_data.csv')