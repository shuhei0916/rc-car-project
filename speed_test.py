import csv
import pandas as pd
import time

# サンプルCSVファイル作成
def generate_sample_csv(filename, num_rows=1000000):
    rows = [["Time", "Speed", "Direction"]] + [
        [i, i * 2, "Forward" if i % 2 == 0 else "Backward"] for i in range(num_rows)
    ]
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

# csvライブラリの読み込み時間計測
def measure_csv_read_speed(filename):
    start = time.time()
    with open(filename, mode="r") as file:
        csv_data = list(csv.reader(file))
    end = time.time()
    return end - start

# pandasの読み込み時間計測
def measure_pandas_read_speed(filename):
    start = time.time()
    pandas_data = pd.read_csv(filename)
    end = time.time()
    return end - start

# メイン処理
def main():
    filename = "data/sample_data.csv"
    print("サンプルデータを生成中...")
    generate_sample_csv(filename)
    
    print("csvライブラリでの読み込み速度計測中...")
    csv_time = measure_csv_read_speed(filename)
    print(f"csvライブラリの処理時間: {csv_time:.2f}秒")
    
    print("pandasライブラリでの読み込み速度計測中...")
    pandas_time = measure_pandas_read_speed(filename)
    print(f"pandasライブラリの処理時間: {pandas_time:.2f}秒")

if __name__ == "__main__":
    main()
