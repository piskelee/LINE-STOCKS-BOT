import yfinance as yf
import numpy as np
import requests
import os


# =========================
# LINE Flex Message
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
        "messages": [
            flex
        ]
    }
    try:
        r = requests.post(
            url,
            headers=headers,
            json=data
        )

        print(r.text)

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
# 股票清單
# =========================
def load_list():
    try:
        with open(
                "list.txt",
                "r",
                encoding="utf-8"
        ) as f:
            return [
                x.strip()
                for x in f
                if x.strip()
            ]
    except:
        return [
            "0050.TW",
        ]

# =========================
# float安全轉換
# =========================
def f(v):
    return float(
        np.array(v)
        .reshape(-1)[-1]
    )


# =========================
# KD狀態
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
# 分析股票
# =========================
def analyze(symbol):
    try:

        df = yf.download(
            symbol,
            period="6mo",
            interval="1d",
            progress=False,
            auto_adjust=True
        )
        if df.empty:
            return None
        k, d = calc_kd(df)
        k = k.dropna().values
        d = d.dropna().values

        if len(k) < 2:
            return None
        k_now = f(k[-1])
        k_prev = f(k[-2])
        d_now = f(d[-1])
        d_prev = f(d[-2])
        close = f(
            df["Close"].iloc[-1]
        )
        date = df.index[-1].strftime(
            "%Y-%m-%d"
        )
        # =================
        # KD交叉
        # =================

        cross = ""

        if k_prev < d_prev and k_now > d_now:
            cross = "🟢黃金交叉"

        elif k_prev > d_prev and k_now < d_now:
            cross = "🔴死亡交叉"

        # =================
        # 評分
        # =================

        score = 0

        if k_now < 20:
            score += 5

        elif k_now < 35:
            score += 3

        if cross == "🟢黃金交叉":
            score += 5

        return {

            "symbol": symbol,

            "date": date,

            "close": close,

            "k": k_now,

            "d": d_now,

            "state": kd_state(k_now),

            "cross": cross,

            "score": score

        }



    except Exception as e:

        print(
            symbol,
            e
        )

        return None


# =========================
# 建立 Flex 表格
# =========================
def create_flex(results):
    rows = [{

        "type": "box",
        "layout": "horizontal",

        "contents": [

            {
                "type": "text",
                "text": "股票",
                "weight": "bold",
                "flex": 3
            },

            {
                "type": "text",
                "text": "價格",
                "weight": "bold",
                "align": "end",
                "flex": 2
            },

            {
                "type": "text",
                "text": "K",
                "weight": "bold",
                "align": "end",
                "flex": 2
            },

            {
                "type": "text",
                "text": "D",
                "weight": "bold",
                "align": "end",
                "flex": 2
            },

            {
                "type": "text",
                "text": "分",
                "weight": "bold",
                "align": "end",
                "flex": 2
            }

        ]

    }, {
        "type": "separator"
    }]

    # 表頭

    # 資料列

    for r in results:
        rows.append({

            "type": "box",

            "layout": "horizontal",

            "contents": [

                {
                    "type": "text",
                    "text": r["symbol"],
                    "size": "sm",
                    "flex": 3
                },

                {
                    "type": "text",
                    "text": f'{r["close"]:.2f}',
                    "size": "sm",
                    "align": "end",
                    "flex": 2
                },

                {
                    "type": "text",
                    "text": f'{r["k"]:.1f}',
                    "size": "sm",
                    "align": "end",
                    "flex": 2
                },

                {
                    "type": "text",
                    "text": f'{r["d"]:.1f}',
                    "size": "sm",
                    "align": "end",
                    "flex": 2
                },

                {
                    "type": "text",
                    "text": str(r["score"]),
                    "size": "sm",
                    "weight": "bold",
                    "align": "end",
                    "flex": 2
                }

            ]

        })

    flex = {

        "type": "flex",

        "altText": "KD策略掃描",

        "contents": {

            "type": "bubble",

            "size": "giga",

            "body": {

                "type": "box",

                "layout": "vertical",

                "spacing": "md",

                "contents": [

                    {
                        "type": "text",
                        "text": "📊 KD策略掃描",
                        "size": "xl",
                        "weight": "bold"
                    },

                    {
                        "type": "text",
                        "text": "依評分排序",
                        "size": "sm"
                    },

                    {
                        "type": "separator"
                    },

                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": rows
                    }

                ]

            }

        }

    }

    return flex


# =========================
# MAIN
# =========================
def main():
    symbols = load_list()

    results = []

    for s in symbols:

        print(
            "分析:",
            s
        )

        r = analyze(s)

        if r:
            results.append(r)

    # 排序

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    flex = create_flex(results)

    send_line_flex(
        flex
    )

    print("DONE")


if __name__ == "__main__":
    main()
