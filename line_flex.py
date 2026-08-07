def create_flex(results):

    rows = []

    # =========================
    # 表頭
    # =========================

    rows.append({
        "type": "box",
        "layout": "horizontal",
        "contents": [
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
                "text":"分",
                "weight":"bold",
                "align":"center",
                "flex":1
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


    # =========================
    # 股票資料
    # =========================

    for r in results:


        # 第一列
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
                    "text":str(r["close"]),
                    "size":"sm",
                    "align":"end",
                    "flex":2
                },

                {
                    "type":"text",
                    "text":str(r["score"]),
                    "size":"sm",
                    "weight":"bold",
                    "align":"center",
                    "flex":1
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


        # 第二列
        rows.append({

            "type":"box",
            "layout":"horizontal",

            "contents":[

                {
                    "type":"text",
                    "text":f'KD {r["kd"]}',
                    "size":"xs",
                    "flex":2
                },

                {
                    "type":"text",
                    "text":f'{r["trend"]}',
                    "size":"xs",
                    "flex":2
                },


                {
                    "type":"text",
                    "text":
                    f'量:{r["volume"]}',
                    "size":"xs",
                    "flex":2
                },

                {
                    "type":"text",
                    "text":
                    r["cross"] or "-",
                    "size":"xs",
                    "flex":2
                }

            ]

        })


        rows.append({
            "type":"separator"
        })


    return {

        "type":"flex",

        "altText":
        "KD選股雷達",

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
                        "text":
                        "📊 KD 選股雷達",
                        "weight":"bold",
                        "size":"xl"
                    },


                    {
                        "type":"text",
                        "text":
                        "收盤10分制分析",
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
