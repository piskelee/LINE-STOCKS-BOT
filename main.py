import yfinance as yf
import numpy as np
import requests
import os


# =========================
# LINE 推播
# =========================
def send_line(msg):

    token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.environ.get("LINE_USER_ID")

    if not token or not user_id:
        print("❌ Missing LINE env")
        return

    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "to": user_id,
        "messages": [{"type": "text", "text": msg[:4900]}]
    }

    requests.post(url, headers=headers, json=data)


# =========================
# KD
# =========================
def calc_kd(df, n=9):

    low = df["Low"].rolling(n).min()
    high = df["High"].rolling(n).max()

    rsv = (df["Close"] - low) / (high - low) * 100

    k = rsv.ewm(com=2).mean()
    d = k.ewm(com=2).mean()

    return k, d


# =========================
# 均線
# =========================
def calc_ma(df):

    ma20 = df["Close"].rolling(20).mean()
    ma60 = df["Close"].rolling(60).mean()

    return ma20, ma60


# =========================
# KD 狀態升級
# =========================
def kd_state(k):

    if k < 20:
        return "🔥 極度超跌（強反彈候選）"
    elif k < 35:
        return "🟢 低檔佈局區"
    elif k < 60:
        return "🟡 中性盤整"
    elif k < 80:
        return "🟠 高檔風險"
    else:
        return "🔴 極度過熱"


# =========================
# 趨勢判斷
# =========================
def trend_state(ma20, ma60):

    if ma20 > ma60:
        return "📈 多頭趨勢"
    else:
        return "📉 空頭趨勢"


# =========================
# 讀股票
# =========================
def load_list():
    try:
        with open("list.txt", "r", encoding="utf-8") as f:
            return [x.strip() for x in f if x.strip()]
    except:
        return ["0050.TW"]


# =========================
# 單檔分析（核心🔥）
# =========================
def analyze(symbol):

    df = yf.download(symbol, period="6mo", interval="1d", progress=False)

    if df is None or df.empty:
        return None

    k, d = calc_kd(df)
    ma20, ma60 = calc_ma(df)

    k_now = float(k.iloc[-1])
    d_now = float(d.iloc[-1])

    ma20_now = float(ma20.iloc[-1])
    ma60_now = float(ma60.iloc[-1])

    close = float(df["Close"].iloc[-1])
    last_date = df.index[-1].strftime("%Y-%m-%d")

    # KD狀態 + 趨勢
    kd_txt = kd_state(k_now)
    trend_txt = trend_state(ma20_now, ma60_now)

    # KD交叉
    cross = ""
    if k.iloc[-2] < d.iloc[-2] and k_now > d_now:
        cross = "🟢 黃金交叉"
    elif k.iloc[-2] > d.iloc[-2] and k_now < d_now:
        cross = "🔴 死亡交叉"

    # 🔥 分數（排序用）
    score = 0

    if k_now < 20:
        score += 3
    elif k_now < 35:
        score += 2

    if ma20_now > ma60_now:
        score += 2

    if cross == "🟢 黃金交叉":
        score += 3

    return {
        "symbol": symbol,
        "msg": f"""📊 {symbol}
🗓 {last_date}

💰 收盤：{close:.2f}
K：{k_now:.2f}
D：{d_now:.2f}

{kd_txt}
{trend_txt}
{cross}

⭐ 分數：{score}
""",
        "score": score
    }


# =========================
# 主程式
# =========================
def main():

    symbols = load_list()

    results = []

    for s in symbols:
        r = analyze(s)
        if r:
            results.append(r)

    # 🔥 排序（最重要）
    results.sort(key=lambda x: x["score"], reverse=True)

    msg = "📈 KD 策略掃描報告\n\n"

    for r in results:
        msg += r["msg"] + "\n----------------\n"

    send_line(msg)


if __name__ == "__main__":
    main()
