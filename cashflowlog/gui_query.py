import tkinter as tk
from tkinter import ttk, messagebox
from . import db

def build_query_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="歷史紀錄查詢")

    result_tree = ttk.Treeview(frame, columns=("id", "table", "date", "info"), show="headings")
    result_tree.heading("id", text="ID")
    result_tree.heading("table", text="表格")
    result_tree.heading("date", text="日期")
    result_tree.heading("info", text="內容")
    result_tree.grid(row=1, column=0, columnspan=3, sticky="nsew")

    def show_all_records():
        for i in result_tree.get_children():
            result_tree.delete(i)
        for rec in db.get_all_records():
            result_tree.insert("", "end", values=rec)

    def delete_selected():
        selected = result_tree.selection()
        if not selected:
            messagebox.showwarning("提醒", "請先選擇一筆紀錄")
            return
        record = result_tree.item(selected[0])['values']
        rid, table = record[0], record[1]
        db.delete_record(table, rid)
        show_all_records()
        messagebox.showinfo("完成", f"已刪除 {table} 的 ID {rid} 紀錄")

    ttk.Button(frame, text="顯示所有紀錄", command=show_all_records).grid(row=0, column=0, pady=5)
    ttk.Button(frame, text="刪除選取紀錄", command=delete_selected).grid(row=0, column=1, pady=5)
