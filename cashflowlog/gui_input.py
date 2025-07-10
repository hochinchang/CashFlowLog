import tkinter as tk
from tkinter import ttk, messagebox
from . import db

def build_income_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="本月收入")

    income_item = ttk.Combobox(frame, values=["本俸", "專業加給", "其他"])
    income_item.set("本俸")
    income_date = tk.Entry(frame)
    income_amount = tk.Entry(frame)
    income_note = tk.Entry(frame)

    ttk.Label(frame, text="項目").grid(row=0, column=0)
    income_item.grid(row=0, column=1)
    ttk.Label(frame, text="金額").grid(row=1, column=0)
    income_amount.grid(row=1, column=1)
    ttk.Label(frame, text="進帳日 (YYYY-MM-DD)").grid(row=2, column=0)
    income_date.grid(row=2, column=1)
    ttk.Label(frame, text="備註").grid(row=3, column=0)
    income_note.grid(row=3, column=1)

    def save():
        db.add_monthly_income(income_item.get(), float(income_amount.get()), income_date.get(), income_note.get())
        messagebox.showinfo("完成", "本月收入已儲存")

    ttk.Button(frame, text="儲存收入", command=save).grid(row=4, column=0, columnspan=2, pady=5)

def build_fixed_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="本月固定支出")

    fixed_item = ttk.Combobox(frame, values=["健保", "公保", "年金", "上網費", "行動電話費", "貸款", "大樓管理費", "水費", "電費", "瓦斯費"])
    fixed_item.set("健保")
    fixed_date = tk.Entry(frame)
    fixed_amount = tk.Entry(frame)
    fixed_note = tk.Entry(frame)

    ttk.Label(frame, text="項目").grid(row=0, column=0)
    fixed_item.grid(row=0, column=1)
    ttk.Label(frame, text="金額").grid(row=1, column=0)
    fixed_amount.grid(row=1, column=1)
    ttk.Label(frame, text="付款日 (YYYY-MM-DD)").grid(row=2, column=0)
    fixed_date.grid(row=2, column=1)
    ttk.Label(frame, text="備註").grid(row=3, column=0)
    fixed_note.grid(row=3, column=1)

    def save():
        db.add_fixed_expense(fixed_item.get(), float(fixed_amount.get()), fixed_date.get(), fixed_note.get())
        messagebox.showinfo("完成", "固定支出已儲存")

    ttk.Button(frame, text="儲存支出", command=save).grid(row=4, column=0, columnspan=2, pady=5)

def build_daily_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="每日支出紀錄")

    daily_date = tk.Entry(frame)
    daily_type = ttk.Combobox(frame, values=["收入", "支出"])
    daily_type.set("支出")
    daily_item = tk.Entry(frame)
    daily_amount = tk.Entry(frame)
    daily_method = ttk.Combobox(frame, values=["現金", "信用卡", "轉帳", "Line Pay"])
    daily_method.set("現金")

    ttk.Label(frame, text="日期 (YYYY-MM-DD)").grid(row=0, column=0)
    daily_date.grid(row=0, column=1)
    ttk.Label(frame, text="類型").grid(row=1, column=0)
    daily_type.grid(row=1, column=1)
    ttk.Label(frame, text="品項").grid(row=2, column=0)
    daily_item.grid(row=2, column=1)
    ttk.Label(frame, text="金額").grid(row=3, column=0)
    daily_amount.grid(row=3, column=1)
    ttk.Label(frame, text="付款方式").grid(row=4, column=0)
    daily_method.grid(row=4, column=1)

    def save():
        db.add_daily_expense(daily_date.get(), daily_type.get(), daily_item.get(), float(daily_amount.get()), daily_method.get())
        messagebox.showinfo("完成", "每日支出已儲存")

    ttk.Button(frame, text="儲存紀錄", command=save).grid(row=5, column=0, columnspan=2, pady=5)
