# CashFlowLog V0.1

個人記帳應用程式，使用 Python + SQLite + Tkinter 製作，支援：
- 本月收入管理
- 本月固定支出管理
- 每日收支紀錄
- 歷史查詢與刪除

## 📦 安裝與啟動

```bash
# 建議使用 virtualenv 或 conda
pip install -r requirements.txt
python cashflowlog/main.py
```

## 📁 專案結構

```
CashFlowLog/
├── cashflowlog/
│   ├── main.py           # 主啟動程式
│   ├── db.py             # 資料庫操作
│   ├── gui_input.py      # 收入/支出 GUI
│   └── gui_query.py      # 查詢/刪除 GUI
├── cashflow.db           # 資料庫（會自動產生）
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔧 開發環境建議
- Python 3.10+
- VSCode + Python extension

## 📌 TODO
- [ ] 編輯紀錄功能
- [ ] 統計報表（月收支總結）
- [ ] 匯出 Excel / CSV

---
MIT License © 2025
