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
                "type": "text",
                "text": "股票",
                "weight": "bold",
                "flex": 3
            },
            {
                "type": "text",
                "text": "價格",
                "weight": "bold",
                "flex": 2,
                "align": "end"
            },
            {
                "type": "text",
                "text": "分數",
                "weight": "bold",
                "flex": 2,
                "align": "center"
            },
            {
                "type": "text",
                "text": "訊號",
                "weight": "bold",
                "flex": 3,
                "align": "center"
            }
        ]
    })
    rows.append({
        "type": "separator"
    })


    # =========================
    # 股票資料
    # =========================
    for r in results:
        # 第一行
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
                    "text": str(r["close"]),
                    "size": "sm",
                    "flex": 2,
                    "align": "end"
                },
                {
                    "type": "text",
                    "text": f'{r["score"]}/10',
                    "size": "sm",
                    "weight": "bold",
                    "flex": 2,
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": r["signal"],
                    "size": "sm",
                    "flex": 3,
                    "align": "center"
                }
            ]
        })



        # 第二行 技術資訊
        rows.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text":
                    f'KD:{r["kd"]}',
                    "size":"xs",
                    "flex":2
                },
                {
                    "type":"text",
                    "text":
                    f'趨勢:{r["trend"]}',
                    "size":"xs",
                    "flex":3
                },
                {
                    "type":"text",
                    "text":
                    f'MA20:{r["ma20"]}',
                    "size":"xs",
                    "flex":3
                },
                {
                    "type":"text",
                    "text":
                    f'MA60:{r["ma60"]}',
                    "size":"xs",
                    "flex":3
                }
            ]
        })
        rows.append({
            "type":"box",
            "layout":"horizontal",
            "contents":[
                {
                    "type":"text",
                    "text":
                    f'交叉:{r["cross"] or "-"}',
                    "size":"xs",
                    "flex":3
                },
                {
                    "type":"text",
                    "text":
                    f'量:{r["volume"]}',
                    "size":"xs",
                    "flex":3
                }
            ]
        })
        rows.append({
            "type":"separator"
        })
        
    # =========================
    # Flex
    # =========================
    return {
        "type":"flex",
        "altText":
        "KD選股雷達10分制",
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
                        "📊 KD + MA + Volume 選股雷達",
                        "weight":"bold",
                        "size":"xl"
                    },
                    {
                        "type":"text",
                        "text":
                        "10分制每日收盤分析",
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
