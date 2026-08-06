import yfinance as yf
import numpy as np
import requests
import os

from line_flex import create_flex



# =========================
# LINE 推播
# =========================

def send_line_flex(flex):

    token = os.environ.get(
        "LINE_CHANNEL_ACCESS_TOKEN"
    )

    user_id = os.environ.get(
        "LINE_USER_ID"
    )


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

        print(e)





# =========================
# KD
# =========================

def calc_kd(df,n=9):

    low = df["Low"].rolling(n).min()

    high = df["High"].rolling(n).max()


    rsv = (
        (df["Close"]-low)
        /
        (high-low)
        *100
    )


    k = rsv.ewm(com=2).mean()

    d = k.ewm(com=2).mean()


    return k,d





# =========================
# MA
# =========================

def calc_ma(df):

    ma20 = df["Close"].rolling(20).mean()

    ma60 = df["Close"].rolling(60).mean()


    return ma20,ma60





# =========================
# 股票清單
# =========================

def load_list():

    try:

        with open(
            "list.txt",
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

def trend_state(ma20,ma60):

    if ma20 > ma60:

        return "多頭"

    else:

        return "空頭"





# =========================
# 5分制訊號
# =========================

def buy_signal(score):

    if score == 5:

        return "🟢強力買進"


    elif score == 4:

        return "🟡買進觀察"


    elif score >= 2:

        return "⚪等待"


    else:

        return "🔴不買"





# =========================
# 股票分析
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

        k_old = f(k[-2])


        d_now = f(d[-1])

        d_old = f(d[-2])





        # KD交叉

        cross = ""


        if k_old < d_old and k_now > d_now:

            cross = "黃金交叉"


        elif k_old > d_old and k_now < d_now:

            cross = "死亡交叉"





        kd = kd_state(k_now)



        trend = trend_state(

            f(ma20[-1]),

            f(ma60[-1])

        )





        # =========================
        # 5分評分
        # =========================

        score = 0



        # KD

        if kd=="極度超跌":

            score += 2


        elif kd=="低檔":

            score += 1





        # MA趨勢

        if trend=="多頭":

            score += 1





        # KD黃金交叉

        if cross=="黃金交叉":

            score += 1





        return {

            "symbol":symbol,


            "close":f(
                df["Close"].iloc[-1]
            ),


            "kd":kd,


            "trend":trend,


            "signal":buy_signal(
                score
            ),


            "score":score

        }





    except Exception as e:

        print(
            symbol,
            e
        )

        return None





# =========================
# MAIN
# =========================

def main():


    results=[]



    for s in load_list():

        print(
            "分析:",
            s
        )


        r=analyze(s)


        if r:

            results.append(r)





    # 分數排序

    results.sort(

        key=lambda x:x["score"],

        reverse=True

    )





    flex=create_flex(results)


    send_line_flex(flex)


    print("DONE")





if __name__=="__main__":

    main()
