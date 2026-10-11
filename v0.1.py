import pandas as pd

def analyze_ma(file_path):
    try:
        # 读取CSV文件，跳过第一行（表头），不设列名
        # 这样读取后，第1列索引为0，第4列索引为3
        df = pd.read_csv(file_path, skiprows=1, header=None)
        
        # 选取每行的第四个数字（索引3，即收盘价）
        # 将其转换为浮点数，方便计算
        close_prices = df.iloc[:, 3].astype(float)
        
        # 计算5日均线（MA5）和20日均线（MA20）
        ma5 = close_prices.rolling(window=5).mean()
        ma20 = close_prices.rolling(window=20).mean()
        
        total_rows = len(close_prices)
        
        print("呜哇！Master，鲸鲸开始计算啦！\n")
        
        # 遍历每一行数据，每20行输出一个信号
        for i in range(total_rows):
            # 判断是否是20的倍数（按行号从1开始算，所以i+1）
            if (i + 1) % 20 == 0:
                # 确保MA20有值（前19行MA20是NaN）
                if pd.notna(ma20.iloc[i]):
                    if ma5.iloc[i] > ma20.iloc[i]:
                        print("buy")
                    else:
                        print("sell")
                        
    except FileNotFoundError:
        print(f"呜……Master，鲸鲸找不到 {file_path} 这个文件，请确认它和代码在同一个文件夹哦～")
    except Exception as e:
        print(f"呜呜，运行的时候出错了：{e}")

if __name__ == "__main__":
    analyze_ma('stock_data.csv')