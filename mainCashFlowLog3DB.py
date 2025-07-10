import sqlite3
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

DB_NAME = "cashflow.db"

# ============================
# 資料庫初始化
# ============================
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

# ============================
# 寫入函式
# ============================
def add_monthly_income(item, amount, date, note=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO monthly_income (item, amount, date, note)
        VALUES (?, ?, ?, ?)
    ''', (item, amount, date, note))
    conn.commit()
    conn.close()


def add_fixed_expense(item, amount, date, note=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO monthly_fixed_expense (item, amount, date, note)
        VALUES (?, ?, ?, ?)
    ''', (item, amount, date, note))
    conn.commit()
    conn.close()


def add_daily_expense(date, type, item, amount, method):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO daily_expense (date, type, item, amount, method)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, type, item, amount, method))
    conn.commit()
    conn.close()

# ============================
# GUI
# ============================
def launch_gui():
    root = tk.Tk()
    root.title("CashFlowLog")

    notebook = ttk.Notebook(root)
    notebook.pack(padx=10, pady=10, fill='both', expand=True)

    # ========== 月收入頁面 ==========
    frame_income = ttk.Frame(notebook)
    notebook.add(frame_income, text="本月收入")

    income_item = ttk.Combobox(frame_income, values=["本俸", "專業加給", "其他"])
    income_item.set("本俸")
    income_date = tk.Entry(frame_income)
    income_amount = tk.Entry(frame_income)
    income_note = tk.Entry(frame_income)

    ttk.Label(frame_income, text="項目").grid(row=0, column=0)
    income_item.grid(row=0, column=1)
    ttk.Label(frame_income, text="金額").grid(row=1, column=0)
    income_amount.grid(row=1, column=1)
    ttk.Label(frame_income, text="進帳日 (YYYY-MM-DD)").grid(row=2, column=0)
    income_date.grid(row=2, column=1)
    ttk.Label(frame_income, text="備註").grid(row=3, column=0)
    income_note.grid(row=3, column=1)

    def save_income():
        add_monthly_income(income_item.get(), float(income_amount.get()), income_date.get(), income_note.get())
        messagebox.showinfo("完成", "本月收入已儲存")

    ttk.Button(frame_income, text="儲存收入", command=save_income).grid(row=4, column=0, columnspan=2, pady=5)

    # ========== 固定支出頁面 ==========
    frame_fixed = ttk.Frame(notebook)
    notebook.add(frame_fixed, text="本月固定支出")

    fixed_item = ttk.Combobox(frame_fixed, values=["健保", "公保", "年金", "上網費", "行動電話費", "貸款", "大樓管理費", "水費", "電費", "瓦斯費"])
    fixed_item.set("健保")
    fixed_date = tk.Entry(frame_fixed)
    fixed_amount = tk.Entry(frame_fixed)
    fixed_note = tk.Entry(frame_fixed)

    ttk.Label(frame_fixed, text="項目").grid(row=0, column=0)
    fixed_item.grid(row=0, column=1)
    ttk.Label(frame_fixed, text="金額").grid(row=1, column=0)
    fixed_amount.grid(row=1, column=1)
    ttk.Label(frame_fixed, text="付款日 (YYYY-MM-DD)").grid(row=2, column=0)
    fixed_date.grid(row=2, column=1)
    ttk.Label(frame_fixed, text="備註").grid(row=3, column=0)
    fixed_note.grid(row=3, column=1)

    def save_fixed():
        add_fixed_expense(fixed_item.get(), float(fixed_amount.get()), fixed_date.get(), fixed_note.get())
        messagebox.showinfo("完成", "固定支出已儲存")

    ttk.Button(frame_fixed, text="儲存支出", command=save_fixed).grid(row=4, column=0, columnspan=2, pady=5)

    # ========== 每日支出頁面 ==========
    frame_daily = ttk.Frame(notebook)
    notebook.add(frame_daily, text="每日支出紀錄")

    daily_date = tk.Entry(frame_daily)
    daily_type = ttk.Combobox(frame_daily, values=["收入", "支出"])
    daily_type.set("支出")
    daily_item = tk.Entry(frame_daily)
    daily_amount = tk.Entry(frame_daily)
    daily_method = ttk.Combobox(frame_daily, values=["現金", "信用卡", "轉帳", "Line Pay"])
    daily_method.set("現金")

    ttk.Label(frame_daily, text="日期 (YYYY-MM-DD)").grid(row=0, column=0)
    daily_date.grid(row=0, column=1)
    ttk.Label(frame_daily, text="類型").grid(row=1, column=0)
    daily_type.grid(row=1, column=1)
    ttk.Label(frame_daily, text="品項").grid(row=2, column=0)
    daily_item.grid(row=2, column=1)
    ttk.Label(frame_daily, text="金額").grid(row=3, column=0)
    daily_amount.grid(row=3, column=1)
    ttk.Label(frame_daily, text="付款方式").grid(row=4, column=0)
    daily_method.grid(row=4, column=1)

    def save_daily():
        add_daily_expense(daily_date.get(), daily_type.get(), daily_item.get(), float(daily_amount.get()), daily_method.get())
        messagebox.showinfo("完成", "每日支出已儲存")

    ttk.Button(frame_daily, text="儲存紀錄", command=save_daily).grid(row=5, column=0, columnspan=2, pady=5)

    # ========== 紀錄查詢頁面 ==========
    frame_query = ttk.Frame(notebook)
    notebook.add(frame_query, text="歷史紀錄查詢")

    result_text = tk.Text(frame_query, width=60, height=20)
    result_text.grid(row=1, column=0, columnspan=3)

    def show_all_records():
        result_text.delete(1.0, tk.END)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        result_text.insert(tk.END, "【本月收入】\n")
        for row in c.execute("SELECT date, item, amount, note FROM monthly_income ORDER BY date DESC"):
            result_text.insert(tk.END, f"{row[0]} {row[1]} {row[2]}元 {row[3]}\n")
        result_text.insert(tk.END, "\n【固定支出】\n")
        for row in c.execute("SELECT date, item, amount, note FROM monthly_fixed_expense ORDER BY date DESC"):
            result_text.insert(tk.END, f"{row[0]} {row[1]} {row[2]}元 {row[3]}\n")
        result_text.insert(tk.END, "\n【每日支出紀錄】\n")
        for row in c.execute("SELECT date, type, item, amount, method FROM daily_expense ORDER BY date DESC"):
            result_text.insert(tk.END, f"{row[0]} {row[1]} {row[2]} {row[3]}元 ({row[4]})\n")
        conn.close()

    ttk.Button(frame_query, text="顯示所有紀錄", command=show_all_records).grid(row=0, column=0, pady=5)

    root.mainloop()

# ============================
# 啟動
# ============================
if __name__ == "__main__":
    init_db()
    launch_gui()
