from FinMind.data import DataLoader
import requests
import os
from datetime import datetime, timedelta

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

        "Authorization":
            f"Bearer {token}",

        "Content-Type":
            "application/json"

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


        print(
            r.text
        )


    except Exception as e:

        print(e)




# =========================
# FinMind
# =========================

api = DataLoader()



# =========================
# KD
# =========================

def calc_kd(df, n=9):


    low = (
        df["min"]
        .rolling(n)
        .min()
    )


    high = (
        df["max"]
        .rolling(n)
        .max()
    )



    rsv = (

        (df["close"] - low)

        /

        (high-low)

        *100

    )



    k = rsv.ewm(
        com=2
    ).mean()



    d = k.ewm(
        com=2
    ).mean()



    return k,d




# =========================
# MA
# =========================

def calc_ma(df):

    ma20 = (
        df["close"]
        .rolling(20)
        .mean()
    )


    ma60 = (
        df["close"]
        .rolling(60)
        .mean()
    )


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

            "0050"

        ]





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
# 趨勢
# =========================

def trend_state(ma20, ma60):


    if ma20 > ma60:

        return "多頭"


    return "空頭"





# =========================
# 5分制
# =========================

def score_signal(score):


    if score == 5:

        return "🟢強力買進"


    elif score == 4:

        return "🟡買進觀察"


    elif score >=2:

        return "⚪等待"


    else:

        return "🔴不買"





# =========================
# 分析股票
# =========================

def analyze(symbol):


    try:


        today = datetime.now()


        end_date = today.strftime(
            "%Y-%m-%d"
        )


        start_date = (

            today - timedelta(days=180)

        ).strftime(
            "%Y-%m-%d"
        )



        df = api.taiwan_stock_daily(

            stock_id=symbol,

            start_date=start_date,

            end_date=end_date

        )



        if df.empty:

            return None



        df = df.sort_values(
            "date"
        )



        k,d = calc_kd(df)



        ma20,ma60 = calc_ma(df)



        # 避免資料不足

        if len(k.dropna()) < 2:

            return None



        k_now = float(
            k.iloc[-1]
        )

        k_old = float(
            k.iloc[-2]
        )


        d_now = float(
            d.iloc[-1]
        )

        d_old = float(
            d.iloc[-2]
        )




        # KD交叉

        cross=""


        if (

            k_old < d_old

            and

            k_now > d_now

        ):

            cross="黃金交叉"



        elif (

            k_old > d_old

            and

            k_now < d_now

        ):

            cross="死亡交叉"




        kd = kd_state(
            k_now
        )



        trend = trend_state(

            float(ma20.iloc[-1]),

            float(ma60.iloc[-1])

        )



        # =====================
        # 5分評分
        # =====================

        score=0



        # KD

        if kd=="極度超跌":

            score += 2


        elif kd=="低檔":

            score += 1




        # MA

        if trend=="多頭":

            score += 1




        # 黃金交叉

        if cross=="黃金交叉":

            score += 1




        return {


            "symbol":
                symbol,


            "close":
                round(
                    float(df["close"].iloc[-1]),
                    2
                ),


            "kd":
                kd,


            "trend":
                trend,


            "cross":
                cross,


            "score":
                score,


            "signal":
                score_signal(score)

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



    stocks = load_list()



    for symbol in stocks:


        print(
            "分析:",
            symbol
        )


        r = analyze(
            symbol
        )


        if r:

            results.append(r)



    # 分數高到低

    results.sort(

        key=lambda x:x["score"],

        reverse=True

    )



    flex = create_flex(
        results
    )


    send_line_flex(
        flex
    )


    print(
        "DONE"
    )





if __name__=="__main__":

    main()
