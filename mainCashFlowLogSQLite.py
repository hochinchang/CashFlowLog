import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

DB_NAME = "cashflow.db"

# 初始化資料庫（若無表格則建立）
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            item TEXT NOT NULL,
            amount REAL NOT NULL,
            method TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 儲存資料到資料庫
def save_to_db(date, kind, item, amount, method):
    try:
        # 驗證日期
        datetime.strptime(date, "%Y-%m-%d")

        # 驗證金額
        amount = float(amount)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (date, type, item, amount, method)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, kind, item, amount, method))
        conn.commit()
        conn.close()
        messagebox.showinfo("成功", "資料已儲存！")
    except ValueError as e:
        messagebox.showerror("錯誤", f"輸入錯誤：{e}")
    except Exception as e:
        messagebox.showerror("錯誤", str(e))

# 初始化 GUI
def launch_gui():
    root = tk.Tk()
    root.title("CashFlowLog - SQLite 記帳本")

    tk.Label(root, text="日期 (YYYY-MM-DD)").grid(row=0, column=0)
    entry_date = tk.Entry(root)
    entry_date.grid(row=0, column=1)

    tk.Label(root, text="類型").grid(row=1, column=0)
    combo_kind = ttk.Combobox(root, values=["支出", "收入"])
    combo_kind.grid(row=1, column=1)
    combo_kind.set("支出")

    tk.Label(root, text="品項").grid(row=2, column=0)
    entry_item = tk.Entry(root)
    entry_item.grid(row=2, column=1)

    tk.Label(root, text="金額").grid(row=3, column=0)
    entry_amount = tk.Entry(root)
    entry_amount.grid(row=3, column=1)

    tk.Label(root, text="付款方式").grid(row=4, column=0)
    combo_method = ttk.Combobox(root, values=["現金", "信用卡", "轉帳", "Line Pay"])
    combo_method.grid(row=4, column=1)
    combo_method.set("現金")

    def on_save():
        save_to_db(
            entry_date.get(),
            combo_kind.get(),
            entry_item.get(),
            entry_amount.get(),
            combo_method.get()
        )

    tk.Button(root, text="儲存記帳", command=on_save).grid(row=5, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    init_db()
    launch_gui()
