def create_flex(results):
    rows = []

    # 表頭列
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
                "text": "KD",
                "weight": "bold",
                "flex": 2,
                "align": "center"
            },
            {
                "type": "text",
                "text": "趨勢",
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
            },
            {
                "type": "text",
                "text": "分",
                "weight": "bold",
                "flex": 2,
                "align": "center"
            }
        ]
    })

    rows.append({
        "type": "separator"
    })

    # 資料內容列
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
                    "text": str(r["close"]),
                    "size": "sm",
                    "flex": 2,
                    "align": "end"
                },
                {
                    "type": "text",
                    "text": r["kd"],
                    "size": "sm",
                    "flex": 2,
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": r["trend"],
                    "size": "sm",
                    "flex": 2,
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": r["signal"],
                    "size": "sm",
                    "flex": 3,
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f'{r["score"]}/5',
                    "size": "sm",
                    "weight": "bold",
                    "flex": 2,
                    "align": "center"
                }
            ]
        })

    # 回傳 Flex Message 物件結構
    return {
        "type": "flex",
        "altText": "KD選股雷達",
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
                        "text": "📊 KD + MA + Volume 選股雷達",
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "text",
                        "text": "每日收盤技術分析",
                        "size": "sm"
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": rows
                    }
                ]
            }
        }
    }
