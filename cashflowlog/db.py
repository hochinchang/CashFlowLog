import sqlite3

DB_NAME = "cashflow.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS monthly_income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT CHECK(item IN ('本俸', '專業加給', '其他')) NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        )
    ''')

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

def add_monthly_income(item, amount, date, note=""):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            '''INSERT INTO monthly_income (item, amount, date, note) VALUES (?, ?, ?, ?)''',
            (item, amount, date, note)
        )

def add_fixed_expense(item, amount, date, note=""):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            '''INSERT INTO monthly_fixed_expense (item, amount, date, note) VALUES (?, ?, ?, ?)''',
            (item, amount, date, note)
        )

def add_daily_expense(date, type, item, amount, method):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            '''INSERT INTO daily_expense (date, type, item, amount, method) VALUES (?, ?, ?, ?, ?)''',
            (date, type, item, amount, method)
        )

def delete_record(table, record_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(f"DELETE FROM {table} WHERE id = ?", (record_id,))

def get_all_records():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        records = []
        for row in c.execute("SELECT id, date, item, amount, note FROM monthly_income"):
            records.append((row[0], "monthly_income", row[1], f"{row[2]} {row[3]}元 {row[4]}"))
        for row in c.execute("SELECT id, date, item, amount, note FROM monthly_fixed_expense"):
            records.append((row[0], "monthly_fixed_expense", row[1], f"{row[2]} {row[3]}元 {row[4]}"))
        for row in c.execute("SELECT id, date, type, item, amount, method FROM daily_expense"):
            records.append((row[0], "daily_expense", row[1], f"{row[2]} {row[3]} {row[4]}元 ({row[5]})"))
    return records
