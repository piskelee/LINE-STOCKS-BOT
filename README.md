# 📈 KD LINE BOT（多股票監控）

一個使用 GitHub Actions 自動執行的 KD 技術指標監控系統，會在市場開盤前自動計算 KD 值並透過 LINE 推播。

---

# 🚀 功能

- 📊 計算 KD 指標（9,3）
- 🔵🟢🟡🔴 四大市場狀態判斷
- 🟢 黃金交叉提醒
- 🔴 死亡交叉提醒
- 📱 LINE 自動推播
- 📂 支援 list.txt 多股票
- ☁️ GitHub Actions 自動執行

---

# 📊 市場狀態規則

| K值 | 狀態 |
|-----|------|
| K ≤ 20 | 🔵 超跌（可能反彈） |
| 20 < K ≤ 35 | 🟢 低檔（重點區） |
| 35 < K ≤ 80 | 🟡 盤整（觀望） |
| K > 80 | 🔴 過熱（注意回檔） |

---

# 📁 專案結構

```text
kd-line-bot/
│
├── main.py
├── list.txt
├── requirements.txt
└── .github/workflows/daily.yml
