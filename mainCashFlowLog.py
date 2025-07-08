import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P
import os

FILENAME = "記帳本.ods"

def load_or_create_ods():
    if os.path.exists(FILENAME):
        return OpenDocumentSpreadsheet(filename=FILENAME)
    else:
        return OpenDocumentSpreadsheet()

def add_header_row(table):
    header = TableRow()
    for col in ["日期", "類型", "品項", "金額", "付款方式"]:
        cell = TableCell()
        cell.addElement(P(text=col))
        header.addElement(cell)
    table.addElement(header)

def add_record(table, record):
    row = TableRow()
    for item in record:
        cell = TableCell()
        cell.addElement(P(text=item))
        row.addElement(cell)
    table.addElement(row)

def save_to_ods(date_str, kind, item, amount, method):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        month_name = f"{date.month}月"

        doc = load_or_create_ods()
        spreadsheet = doc.spreadsheet

        table = None
        for t in spreadsheet.getElementsByType(Table):
            if t.getAttribute("name") == month_name:
                table = t
                break

        if table is None:
            table = Table(name=month_name)
            add_header_row(table)
            spreadsheet.addElement(table)

        record = [date_str, kind, item, amount, method]
        add_record(table, record)

        doc.save(FILENAME)
        messagebox.showinfo("成功", f"已儲存到 {month_name} 工作表中")
    except Exception as e:
        messagebox.showerror("錯誤", str(e))

# GUI
root = tk.Tk()
root.title("簡易記帳本（含收入）")

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
    date = entry_date.get()
    kind = combo_kind.get()
    item = entry_item.get()
    amount = entry_amount.get()
    method = combo_method.get()
    save_to_ods(date, kind, item, amount, method)

btn_save = tk.Button(root, text="儲存記帳", command=on_save)
btn_save.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
