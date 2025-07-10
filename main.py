from cashflowlog import db
from cashflowlog import gui_input, gui_query
import tkinter as tk
from tkinter import ttk


def main():
    db.init_db()

    root = tk.Tk()
    root.title("CashFlowLog")

    notebook = ttk.Notebook(root)
    notebook.pack(padx=10, pady=10, fill='both', expand=True)

    gui_input.build_income_tab(notebook)
    gui_input.build_fixed_tab(notebook)
    gui_input.build_daily_tab(notebook)
    gui_query.build_query_tab(notebook)

    root.mainloop()


if __name__ == "__main__":
    main()
