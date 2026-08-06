# line_flex.py


def create_flex(results):

    rows = []


    # =========================
    # 表頭
    # =========================

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
            },

            {
                "type":"text",
                "text":"分",
                "weight":"bold",
                "align":"center",
                "flex":1
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


        rows.append({

            "type":"box",

            "layout":"horizontal",

            "contents":[


                {
                    "type":"text",
                    "text":r["symbol"].replace(".TW",""),
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
                },


                {
                    "type":"text",
                    "text":str(r["score"]),
                    "size":"sm",
                    "weight":"bold",
                    "align":"center",
                    "flex":1
                }

            ]

        })



    # =========================
    # Flex Bubble
    # =========================

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
