import os
import time
from datetime import datetime, timedelta

import requests
import pandas as pd

from FinMind.data import DataLoader
from line_flex import create_flex


# =========================
# LINE PUSH
# =========================

def send_line_flex(flex):
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
        "messages": [flex]
    }

    try:
        r = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=10
        )
        print("LINE:", r.text)

    except Exception as e:
        print("LINE ERROR:", e)


# =========================
# FinMind
# =========================

api = DataLoader()


# =========================
# KD 標準算法
# =========================

def calc_kd(df, n=9):
    low = df["min"].rolling(n).min()
    high = df["max"].rolling(n).max()

    rsv = (df["close"] - low) / (high - low) * 100

    k_list = []
    d_list = []

    k = 50
    d = 50

    for value in rsv:
        if pd.isna(value):
            k_list.append(None)
            d_list.append(None)
            continue

        k = k * 2 / 3 + value / 3
        d = d * 2 / 3 + k / 3

        k_list.append(k)
        d_list.append(d)

    return (
        pd.Series(k_list, index=df.index),
        pd.Series(d_list, index=df.index)
    )


# =========================
# MA
# =========================

def calc_ma(df):
    ma20 = df["close"].rolling(20).mean()
    ma60 = df["close"].rolling(60).mean()

    return ma20, ma60


# =========================
# Volume
# =========================

def volume_signal(df):
    if len(df) < 20:
        return False

    vol20 = df["Trading_Volume"].rolling(20).mean()

    return df["Trading_Volume"].iloc[-1] > vol20.iloc[-1]


# =========================
# 股票清單
# =========================

def load_list():
    try:
        with open("list.txt", encoding="utf-8") as f:
            return [x.strip() for x in f if x.strip()]
    except:
        return ["0050"]


# =========================
# KD 狀態
# =========================

def kd_state(k):
    if k < 20:
        return "超跌"
    elif k < 35:
        return "低檔"
    elif k < 60:
        return "中性"
    elif k < 80:
        return "高檔"
    else:
        return "過熱"


# =========================
# Trend
# =========================

def trend_state(ma20, ma60):
    if ma20 > ma60:
        return "多頭"
    return "空頭"


# =========================
# Score
# =========================

def score_signal(score):
    if score >= 4:
        return "🟢買進"
    elif score == 3:
        return "🟡觀察"
    elif score >= 1:
        return "⚪等待"
    else:
        return "🔴不買"


# =========================
# Analyze
# =========================

def analyze(symbol):
    try:
        today = datetime.now()
        end_date = today.strftime("%Y-%m-%d")
        start_date = (today - timedelta(days=365)).strftime("%Y-%m-%d")

        df = api.taiwan_stock_daily(
            stock_id=symbol,
            start_date=start_date,
            end_date=end_date
        )

        if df is None or df.empty:
            return None

        df = df.sort_values("date")

        k, d = calc_kd(df)
        ma20, ma60 = calc_ma(df)

        if len(k.dropna()) < 2 or len(ma60.dropna()) < 1:
            return None

        k_now = float(k.iloc[-1])
        k_old = float(k.iloc[-2])
        d_now = float(d.iloc[-1])
        d_old = float(d.iloc[-2])

        cross = ""

        if k_old < d_old and k_now > d_now:
            cross = "黃金交叉"
        elif k_old > d_old and k_now < d_now:
            cross = "死亡交叉"

        kd = kd_state(k_now)
        trend = trend_state(float(ma20.iloc[-1]), float(ma60.iloc[-1]))
        volume = volume_signal(df)

        score = 0

        if kd == "超跌":
            score += 2
        elif kd == "低檔":
            score += 1

        if trend == "多頭":
            score += 1

        if cross == "黃金交叉":
            score += 1

        if volume:
            score += 1

        return {
            "symbol": symbol,
            "close": round(float(df["close"].iloc[-1]), 2),
            "kd": kd,
            "trend": trend,
            "cross": cross,
            "volume": "放大" if volume else "正常",
            "score": score,
            "signal": score_signal(score)
        }

    except Exception as e:
        print(symbol, e)
        return None


# =========================
# MAIN
# =========================

def main():
    results = []
    stocks = load_list()

    for symbol in stocks:
        print("分析:", symbol)
        r = analyze(symbol)

        if r:
            results.append(r)

        time.sleep(0.5)

    if results:
        results.sort(key=lambda x: x["score"], reverse=True)
        flex = create_flex(results)
        send_line_flex(flex)
    else:
        print("沒有有效資料")

    print("DONE")


if __name__ == "__main__":
    main()
