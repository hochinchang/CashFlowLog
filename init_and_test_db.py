import sqlite3
import os

DB_NAME = "cashflow.db"

# 初始化資料庫與三張表格
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # 1. 本月收入表
    c.execute('''
        CREATE TABLE IF NOT EXISTS monthly_income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT CHECK(item IN ('本俸', '專業加給', '其他')) NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        )
    ''')

    # 2. 本月固定支出表
    c.execute('''
        CREATE TABLE IF NOT EXISTS monthly_fixed_expense (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT CHECK(item IN (
                '健保', '公保', '年金', '上網費', '行動電話費',
                '貸款', '大樓管理費', '水費', '電費', '瓦斯費'
            )) NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        )
    ''')

    # 3. 每日支出紀錄表
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_expense (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT CHECK(type IN ('收入', '支出')) NOT NULL,
            item TEXT NOT NULL,
            amount REAL NOT NULL,
            method TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("資料庫初始化完成！")

# 寫入：本月收入
def add_monthly_income(item, amount, date, note=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO monthly_income (item, amount, date, note)
        VALUES (?, ?, ?, ?)
    ''', (item, amount, date, note))
    conn.commit()
    conn.close()
    print("✅ 已新增本月收入")

# 寫入：本月固定支出
def add_fixed_expense(item, amount, date, note=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO monthly_fixed_expense (item, amount, date, note)
        VALUES (?, ?, ?, ?)
    ''', (item, amount, date, note))
    conn.commit()
    conn.close()
    print("✅ 已新增本月固定支出")

# 寫入：每日支出紀錄
def add_daily_expense(date, type, item, amount, method):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO daily_expense (date, type, item, amount, method)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, type, item, amount, method))
    conn.commit()
    conn.close()
    print("✅ 已新增每日支出紀錄")

# ==============================
# 測試用（主程式）
# ==============================
if __name__ == "__main__":
    # 第一次執行：初始化資料庫
    init_db()

    # 測試寫入資料（可刪）
    add_monthly_income("本俸", 60000, "2025-07-01", "七月薪資")
    add_fixed_expense("健保", 1200, "2025-07-05", "自費")
    add_daily_expense("2025-07-06", "支出", "晚餐", 180, "現金")
