import pandas as pd

def analyze_dual_strategy(file_path):
    try:
        # 读取CSV，第一行为表头 / Read CSV, first row as header
        df = pd.read_csv(file_path)
        
        # 建立中英文列名映射 / Chinese-English column mapping
        column_mapping = {
            '日期': 'Date', 
            '股票代码': 'Stock_Code', 
            '开盘': 'Open', 
            '收盘': 'Close',
            '最高': 'High', 
            '最低': 'Low', 
            '成交量': 'Volume', 
            '成交额': 'Amount',
            '振幅': 'Amplitude', 
            '涨跌幅': 'Change_Pct', 
            '涨跌额': 'Change_Amt', 
            '换手率': 'Turnover_Rate'
        }
        
        # 统一修改列名，支持原生英文文件 / Rename columns, supporting native English files
        df.rename(columns=column_mapping, inplace=True)
        
        # 提取日期、收盘价和最高价 / Extract Date, Close, and High
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        
        close_prices = df['Close'].astype(float)
        high_prices = df['High'].astype(float)
        
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