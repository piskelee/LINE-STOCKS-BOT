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

        "Authorization":f"Bearer {token}",

        "Content-Type":"application/json"

    }


    data = {

        "to":user_id,

        "messages":[flex]

    }


    requests.post(
        url,
        headers=headers,
        json=data
    )





# =========================
# KD
# =========================

def calc_kd(df,n=9):

    low=df["Low"].rolling(n).min()

    high=df["High"].rolling(n).max()


    rsv=(df["Close"]-low)/(high-low)*100


    k=rsv.ewm(com=2).mean()

    d=k.ewm(com=2).mean()


    return k,d





# =========================
# MA
# =========================

def calc_ma(df):

    return (

        df["Close"].rolling(20).mean(),

        df["Close"].rolling(60).mean()

    )





def load_list():

    with open(
        "list.txt",
        encoding="utf-8"
    ) as f:

        return [
            x.strip()
            for x in f
            if x.strip()
        ]





def f(v):

    return float(
        np.array(v)
        .reshape(-1)[-1]
    )





def kd_state(k):

    if k < 20:
        return "極度超跌"

    elif k <35:
        return "低檔"

    elif k<60:
        return "中性"

    elif k<80:
        return "高檔"

    else:
        return "過熱"





def trend_state(a,b):

    return "多頭" if a>b else "空頭"





def buy_signal(kd,trend,cross):

    if kd in ["極度超跌","低檔"] and trend=="多頭" and cross=="黃金交叉":

        return "🟢強力買進"


    elif kd in ["極度超跌","低檔"] and trend=="多頭":

        return "🟡觀察買進"


    elif kd in ["極度超跌","低檔"]:

        return "⚪等待"


    elif kd=="過熱":

        return "🔴避免追高"


    return "—"





# =========================
# 股票分析
# =========================

def analyze(symbol):

    df=yf.download(
        symbol,
        period="6mo",
        progress=False,
        auto_adjust=True
    )


    if df.empty:
        return None



    k,d=calc_kd(df)

    ma20,ma60=calc_ma(df)



    k=k.dropna().values

    d=d.dropna().values

    ma20=ma20.dropna().values

    ma60=ma60.dropna().values



    k_now=f(k[-1])

    k_old=f(k[-2])

    d_now=f(d[-1])

    d_old=f(d[-2])



    cross=""

    if k_old<d_old and k_now>d_now:

        cross="黃金交叉"


    elif k_old>d_old and k_now<d_now:

        cross="死亡交叉"




    kd=kd_state(k_now)

    trend=trend_state(
        f(ma20[-1]),
        f(ma60[-1])
    )


    score=0


    if kd=="極度超跌":
        score+=3

    elif kd=="低檔":
        score+=2


    if trend=="多頭":
        score+=2


    if cross=="黃金交叉":
        score+=3



    return {

        "symbol":symbol,

        "close":f(df["Close"].iloc[-1]),

        "kd":kd,

        "trend":trend,

        "signal":buy_signal(
            kd,
            trend,
            cross
        ),

        "score":score

    }





# =========================
# MAIN
# =========================

def main():

    results=[]


    for s in load_list():

        print("分析",s)

        r=analyze(s)

        if r:

            results.append(r)



    results.sort(
        key=lambda x:x["score"],
        reverse=True
    )


    flex=create_flex(results)


    send_line_flex(flex)



if __name__=="__main__":
    main()
