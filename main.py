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
        print("Missing LINE env")
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

    try:
        requests.post(url, headers=headers, json=data)
    except Exception as e:
        print("LINE ERROR:", e)


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
# MA
# =========================
def calc_ma(df):

    ma20 = df["Close"].rolling(20).mean()
    ma60 = df["Close"].rolling(60).mean()

    return ma20, ma60


# =========================
# 讀清單
# =========================
def load_list():
    try:
        with open("list.txt", "r", encoding="utf-8") as f:
            return [x.strip() for x in f if x.strip()]
    except:
        return ["0050.TW"]


# =========================
# 安全 float
# =========================
def f(v):
    return float(np.array(v).reshape(-1)[-1])


# =========================
# KD 狀態（純文字）
# =========================
def kd_state(k):

    if k < 20:
        return "極度超跌"
    elif k < 35:
        return "低檔"
    elif k < 60:
        return "中性"
    elif k < 80:
        return "高檔"
    else:
        return "過熱"


# =========================
# 趨勢（純文字）
# =========================
def trend_state(ma20, ma60):

    return "多頭" if ma20 > ma60 else "空頭"


# =========================
# 分析
# =========================
def analyze(symbol):

    df = yf.download(symbol, period="6mo", interval="1d", progress=False)

    if df is None or df.empty:
        return None

    k, d = calc_kd(df)
    ma20, ma60 = calc_ma(df)

    k = k.dropna().values
    d = d.dropna().values
    ma20 = ma20.dropna().values
    ma60 = ma60.dropna().values

    if len(k) < 2 or len(d) < 2:
        return None

    k_now = f(k[-1])
    k_prev = f(k[-2])

    d_now = f(d[-1])
    d_prev = f(d[-2])

    ma20_now = f(ma20[-1])
    ma60_now = f(ma60[-1])

    close = f(df["Close"].iloc[-1])
    last_date = df.index[-1].strftime("%Y-%m-%d")

    kd_txt = kd_state(k_now)
    trend_txt = trend_state(ma20_now, ma60_now)

    cross = ""
    if k_prev < d_prev and k_now > d_now:
        cross = "黃金交叉"
    elif k_prev > d_prev and k_now < d_now:
        cross = "死亡交叉"

    score = 0

    if k_now < 20:
        score += 3
    elif k_now < 35:
        score += 2

    if ma20_now > ma60_now:
        score += 2

    if cross == "黃金交叉":
        score += 3

    msg = (
        f"🏷️ {symbol}\n"
        f"📅 {last_date}\n\n"
        f"💰 收盤價：{close:.2f}\n\n"
        f"📈 KD 指標\n"
        f"K：{k_now:.2f}\n"
        f"D：{d_now:.2f}\n"
        f"狀態：{kd_txt}\n"
        f"訊號：{cross if cross else '—'}\n\n"
        f"📊 趨勢\n"
        f"MA20：{ma20_now:.2f}\n"
        f"MA60：{ma60_now:.2f}\n"
        f"方向：{trend_txt}\n\n"
        f"⭐ 評分：{score} / 10\n"
    )

    return {"msg": msg, "score": score}


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

    results.sort(key=lambda x: x["score"], reverse=True)

    msg = "KD策略掃描報告\n\n"

    for r in results:
        msg += r["msg"] + "\n----------------\n"

    send_line(msg)
    print("DONE")


if __name__ == "__main__":
    main()
