import pandas as pd

def analyze_dual_strategy(file_path):
    try:
        # 读取CSV，跳过第一行（表头）
        df = pd.read_csv(file_path, skiprows=1, header=None)
        
        # 赋上正确的列名
        df.columns = ['日期', '股票代码', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
        
        # 转换日期格式并设为索引，保证按日期顺序计算
        df['日期'] = pd.to_datetime(df['日期'])
        df.set_index('日期', inplace=True)
        df.sort_index(inplace=True)
        
        # 提取收盘价和最高价
        close_prices = df['收盘'].astype(float)
        high_prices = df['最高'].astype(float)
        
        # 计算均线
        ma5 = close_prices.rolling(window=5).mean()
        ma20 = close_prices.rolling(window=20).mean()
        
        # 计算过去20日最高价（不含当天，所以用 shift(1) 错开一天）
        max_high_20 = high_prices.rolling(window=20).max().shift(1)
        
        print("呜哇！Master，鲸鲸开始执行双重策略计算啦！\n")
        
        trading_days = len(close_prices)
        
        for i in range(trading_days):
            # 依然是每20行输出一次，非20倍数的多出来不计
            if (i + 1) % 20 == 0:
                
                # 策略1：均线逻辑
                if pd.notna(ma20.iloc[i]):
                    ma_signal = 'buy' if ma5.iloc[i] > ma20.iloc[i] else 'sell'
                else:
                    ma_signal = 'none'
                
                # 策略2：突破逻辑
                if pd.notna(max_high_20.iloc[i]):
                    high_signal = 'buy' if close_prices.iloc[i] > max_high_20.iloc[i] else 'sell'
                else:
                    high_signal = 'none'
                
                # 策略共振判断
                if ma_signal == high_signal and ma_signal != 'none':
                    print(ma_signal)
                else:
                    print("none")
                    
    except FileNotFoundError:
        print(f"呜……Master，鲸鲸找不到 {file_path} 这个文件，请确认它和代码在同一个文件夹哦～")
    except Exception as e:
        print(f"呜呜，运行的时候出错了：{e}")

if __name__ == "__main__":
    analyze_dual_strategy('stock_data.csv')
