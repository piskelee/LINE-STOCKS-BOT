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
        "messages": [flex]
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

    rsv = (df["Close"] - low) / (high-low) * 100

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
            "0050.TW"
        ]



# =========================
# float
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
# MA趨勢
# =========================
def trend_state(ma20, ma60):

    if ma20 > ma60:
        return "多頭"

    else:
        return "空頭"



# =========================
# 買進訊號
# =========================
def buy_signal(kd, trend, cross):

    if (
        kd in ["極度超跌", "低檔"]
        and trend == "多頭"
        and cross == "黃金交叉"
    ):
        return "🟢強力買進"


    elif (
        kd in ["極度超跌", "低檔"]
        and trend == "多頭"
    ):
        return "🟡觀察買進"


    elif kd in ["極度超跌", "低檔"]:

        return "⚪等待"


    elif kd == "過熱":

        return "🔴避免追高"


    else:

        return "—"



# =========================
# 分析
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



        k,d = calc_kd(df)

        ma20,ma60 = calc_ma(df)



        k = k.dropna().values
        d = d.dropna().values

        ma20 = ma20.dropna().values
        ma60 = ma60.dropna().values



        if len(k)<2:
            return None



        k_now = f(k[-1])
        k_prev = f(k[-2])

        d_now = f(d[-1])
        d_prev = f(d[-2])



        ma20_now = f(ma20[-1])
        ma60_now = f(ma60[-1])



        close = f(
            df["Close"].iloc[-1]
        )


        date = df.index[-1].strftime(
            "%Y-%m-%d"
        )



        kd_txt = kd_state(k_now)

        trend_txt = trend_state(
            ma20_now,
            ma60_now
        )



        cross = ""


        if k_prev < d_prev and k_now > d_now:

            cross="黃金交叉"


        elif k_prev > d_prev and k_now < d_now:

            cross="死亡交叉"



        signal = buy_signal(
            kd_txt,
            trend_txt,
            cross
        )



        # 評分

        score=0


        if kd_txt=="極度超跌":
            score += 3

        elif kd_txt=="低檔":
            score += 2


        if trend_txt=="多頭":
            score += 2


        if cross=="黃金交叉":
            score += 3



        return {

            "symbol":symbol,

            "date":date,

            "close":close,

            "kd":kd_txt,

            "trend":trend_txt,

            "signal":signal,

            "score":score

        }



    except Exception as e:

        print(symbol,e)

        return None



# =========================
# 建立 Flex
# =========================
def create_flex(results):

    rows=[]


    rows.append({

        "type":"box",
        "layout":"horizontal",

        "contents":[

            {
                "type":"text",
                "text":"股票",
                "weight":"bold",
                "flex":3
            },

            {
                "type":"text",
                "text":"價格",
                "weight":"bold",
                "align":"end",
                "flex":2
            },

            {
                "type":"text",
                "text":"KD",
                "weight":"bold",
                "align":"center",
                "flex":3
            },

            {
                "type":"text",
                "text":"MA",
                "weight":"bold",
                "align":"center",
                "flex":2
            },

            {
                "type":"text",
                "text":"訊號",
                "weight":"bold",
                "align":"center",
                "flex":3
            }

        ]
    })


    rows.append({
        "type":"separator"
    })



    for r in results:


        rows.append({

            "type":"box",

            "layout":"horizontal",

            "contents":[


                {
                    "type":"text",
                    "text":r["symbol"],
                    "size":"sm",
                    "flex":3
                },


                {
                    "type":"text",
                    "text":f'{r["close"]:.2f}',
                    "size":"sm",
                    "align":"end",
                    "flex":2
                },


                {
                    "type":"text",
                    "text":r["kd"],
                    "size":"sm",
                    "align":"center",
                    "flex":3
                },


                {
                    "type":"text",
                    "text":r["trend"],
                    "size":"sm",
                    "align":"center",
                    "flex":2
                },


                {
                    "type":"text",
                    "text":r["signal"],
                    "size":"sm",
                    "align":"center",
                    "flex":3
                }


            ]

        })



    return {

        "type":"flex",

        "altText":"KD策略掃描",

        "contents":{

            "type":"bubble",

            "size":"giga",

            "body":{

                "type":"box",

                "layout":"vertical",

                "spacing":"md",

                "contents":[


                    {
                        "type":"text",
                        "text":"📊 KD + MA選股雷達",
                        "weight":"bold",
                        "size":"xl"
                    },


                    {
                        "type":"text",
                        "text":"KD低檔 + MA趨勢 + 買進訊號",
                        "size":"sm"
                    },


                    {
                        "type":"separator"
                    },


                    {
                        "type":"box",
                        "layout":"vertical",
                        "contents":rows
                    }


                ]

            }

        }

    }



# =========================
# MAIN
# =========================
def main():

    symbols = load_list()

    results=[]


    for s in symbols:

        print("分析:",s)

        r=analyze(s)

        if r:

            results.append(r)



    results.sort(
        key=lambda x:x["score"],
        reverse=True
    )



    flex=create_flex(results)


    send_line_flex(flex)


    print("DONE")



if __name__=="__main__":

    main()
