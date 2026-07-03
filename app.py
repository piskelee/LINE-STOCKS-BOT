import yfinance as yf
import numpy as np


# =========================
# KD 計算
# =========================
def calc_kd(df, n=9):

    low = df["Low"].rolling(n).min()
    high = df["High"].rolling(n).max()

    rsv = (df["Close"] - low) / (high - low) * 100

    k = rsv.ewm(com=2).mean()
    d = k.ewm(com=2).mean()

    return k, d


# =========================
# 安全取值
# =========================
def safe_last(series):

    arr = np.array(series.dropna().values).flatten()

    if len(arr) < 2:
        return None, None

    return float(arr[-1]), float(arr[-2])


# =========================
# 市場狀態
# =========================
def market_state(k):

    if k <= 20:
        return "🔵 超跌（可能反彈）"
    elif k <= 35:
        return "🟢 低檔（重點區）"
    elif k <= 80:
        return "🟡 盤整（觀望）"
    else:
        return "🔴 過熱（注意回檔）"


# =========================
# 讀 LIST
# =========================
def load_list():

    for name in ["list.txt"]:

        try:
            with open(name, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()

            return [x.strip() for x in lines if x.strip()]

        except FileNotFoundError:
            continue

    return ["0050.TW"]


# =========================
# 分析單檔
# =========================
def analyze(symbol):

    print(f"下載 {symbol} ...")

    df = yf.download(symbol, period="3mo", interval="1d", progress=False)

    if df is None or df.empty:
        return f"⚠️ {symbol} 無資料\n"

    k, d = calc_kd(df)

    k_now, k_prev = safe_last(k)
    d_now, d_prev = safe_last(d)

    if None in [k_now, k_prev, d_now, d_prev]:
        return f"⚠️ {symbol} KD不足\n"

    state = market_state(k_now)

    msg = f"""📊 {symbol}

K：{k_now:.2f}
D：{d_now:.2f}
狀態：{state}
"""

    # 黃金交叉
    if k_prev < d_prev and k_now > d_now:
        msg = f"""🟢 {symbol} 黃金交叉！

K：{k_now:.2f}
D：{d_now:.2f}
狀態：{state}
"""

    # 死亡交叉
    elif k_prev > d_prev and k_now < d_now:
        msg = f"""🔴 {symbol} 死亡交叉！

K：{k_now:.2f}
D：{d_now:.2f}
狀態：{state}
"""

    return msg + "\n"


# =========================
# 主程式
# =========================
def main():

    print("=" * 50)
    print("🚀 KD BOT START")
    print("=" * 50)

    symbols = load_list()

    all_msg = "📈 KD 市場狀態報告\n\n"

    for s in symbols:
        all_msg += analyze(s)

    print(all_msg)

    print("=" * 50)
    print("✅ DONE")
    print("=" * 50)


if __name__ == "__main__":
    main()