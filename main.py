# main.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import data, chart, export_csv, seed_dt

# ---------------------------
# App colors & fonts
# ---------------------------
RIGHT_BTN_BG = "#2196F3"  # Lighter blue than sidebar
RIGHT_BTN_FG = "#ffffff"
SIDEBAR_BG = "#1E90FF"   # DodgerBlue
SIDEBAR_FG = "#ffffff"
ACCENT = "#1976D2"
FONT = ("Inter", 10)
TITLE_FONT = ("Inter", 14, "bold")

CATEGORIES = ["Food", "Transport", "Bills", "Shopping", "Entertainment", "Other"]

# ---------------------------
# Helper functions
# ---------------------------
def show_message(text, kind="info"):
    msg_var.set(text)
    if kind == "error":
        msg_label.config(fg="#d32f2f")
    else:
        msg_label.config(fg="#2e7d32")
    root.after(4000, clear_message)

def clear_message():
    msg_var.set("")

def validate_date(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True
    except Exception:
        return False

def validate_amount(s):
    try:
        float(s)
        return True
    except Exception:
        return False

# ---------------------------
# Data operations
# ---------------------------
def load_table(rows=None):
    for r in tree.get_children():
        tree.delete(r)
    if rows is None:
        rows = data.get_all_expenses()
    for row in rows:
        tree.insert("", "end", values=(row["id"], row["date"], row["amount"], row["category"], row["description"]))
    update_totals(rows)

def update_totals(rows):
    total = sum(float(r["amount"]) for r in rows)
    totals_var.set(f"Total: ₹{total:.2f}   ·   Records: {len(rows)}")

def add_action():
    date = date_var.get().strip()
    amount = amount_var.get().strip()
    category = category_var.get().strip()
    desc = desc_var.get().strip()

    if not (date and amount and category):
        show_message("Date, Amount and Category are required.", "error")
        return
    if not validate_date(date):
        show_message("Date must be YYYY-MM-DD.", "error")
        return
    if not validate_amount(amount):
        show_message("Amount must be a number.", "error")
        return
    data.add_expense(date, float(amount), category, desc)
    load_table()
    clear_form()
    show_message("Expense added successfully.")

def on_row_select(event):
    sel = tree.focus()
    if not sel:
        return
    vals = tree.item(sel, "values")
    id_var.set(vals[0])
    date_var.set(vals[1])
    amount_var.set(vals[2])
    category_var.set(vals[3])
    desc_var.set(vals[4])

def update_action():
    eid = id_var.get()
    if not eid:
        show_message("Select a record to update.", "error")
        return
    date = date_var.get().strip()
    amount = amount_var.get().strip()
    category = category_var.get().strip()
    desc = desc_var.get().strip()
    if not (date and amount and category):
        show_message("Date, Amount and Category are required.", "error")
        return
    if not validate_date(date) or not validate_amount(amount):
        show_message("Invalid date or amount.", "error")
        return
    data.update_expense(int(eid), date, float(amount), category, desc)
    load_table()
    clear_form()
    show_message("Expense updated.")

def delete_action():
    eid = id_var.get()
    if not eid:
        show_message("Select a record to delete.", "error")
        return
    if not messagebox.askyesno("Confirm", "Delete selected expense?"):
        return
    data.delete_expense(int(eid))
    load_table()
    clear_form()
    show_message("Expense deleted.")

def clear_form():
    id_var.set("")
    date_var.set(datetime.today().strftime("%Y-%m-%d"))
    amount_var.set("")
    category_var.set(CATEGORIES[0])
    desc_var.set("")

def filter_by_category_action():
    cat = category_filter_var.get()
    if cat == "All":
        load_table()
    else:
        rows = data.filter_by_category(cat)
        load_table(rows)

def filter_by_date_action():
    s = start_var.get().strip()
    e = end_var.get().strip()
    if not (s and e):
        show_message("Start and end date required.", "error")
        return
    if not (validate_date(s) and validate_date(e)):
        show_message("Dates must be YYYY-MM-DD.", "error")
        return
    rows = data.filter_by_date(s, e)
    load_table(rows)

def export_action():
    path = filedialog.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("CSV Files","*.csv")])
    if not path:
        return
    rows = data.get_all_expenses()
    export_csv.export_to_csv(path, rows)
    show_message("Exported to CSV.")

def show_chart_action():
    rows = data.get_all_expenses()
    chart.plot_category_pie(rows)

# ---------------------------
# Build UI
# ---------------------------
root = tk.Tk()
root.title("Personal Expense Tracker — Dashboard")
root.geometry("1000x620")
root.configure(bg=RIGHT_BTN_BG)

# Sidebar
sidebar = tk.Frame(root, bg=SIDEBAR_BG, width=220)
sidebar.pack(side="left", fill="y")
logo = tk.Label(sidebar, text="Expense\nTracker", bg=SIDEBAR_BG, fg=SIDEBAR_FG,
                font=("Inter", 16, "bold"), justify="center")
logo.pack(pady=20)

# Sidebar buttons
btn_cfg = {"width":18, "padx":6, "pady":6, "bd":0, "relief":"flat", "bg":SIDEBAR_FG, "fg":SIDEBAR_BG}
tk.Button(sidebar, text="Add Expense", command=add_action, **btn_cfg).pack(pady=6)
tk.Button(sidebar, text="Update Expense", command=update_action, **btn_cfg).pack(pady=6)
tk.Button(sidebar, text="Delete Expense", command=delete_action, **btn_cfg).pack(pady=6)
tk.Button(sidebar, text="Show Pie Chart", command=show_chart_action, **btn_cfg).pack(pady=6)
tk.Button(sidebar, text="Export CSV", command=export_action, **btn_cfg).pack(pady=6)

# Filters
tk.Label(sidebar, text="Filters", bg=SIDEBAR_BG, fg=SIDEBAR_FG, font=("Inter", 11, "bold")).pack(pady=(20,6))
category_filter_var = tk.StringVar(value="All")
ttk.Combobox(sidebar, values=["All"]+CATEGORIES, textvariable=category_filter_var, state="readonly").pack(pady=6)
tk.Button(sidebar, text="Apply Category", command=filter_by_category_action, **btn_cfg).pack(pady=6)

start_var = tk.StringVar()
end_var = tk.StringVar()
tk.Label(sidebar, text="Date Range (YYYY-MM-DD)", bg=SIDEBAR_BG, fg=SIDEBAR_FG).pack(pady=(10,0))
tk.Entry(sidebar, textvariable=start_var).pack(pady=4)
tk.Entry(sidebar, textvariable=end_var).pack(pady=4)
tk.Button(sidebar, text="Apply Date Filter", command=filter_by_date_action, **btn_cfg).pack(pady=6)

# Right main area
main = tk.Frame(root, bg=RIGHT_BTN_BG, padx=12, pady=12)
main.pack(side="left", fill="both", expand=True)

# Form
form = tk.Frame(main, bg=RIGHT_BTN_BG)
form.pack(fill="x", pady=(0,12))

id_var = tk.StringVar()
date_var = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))
amount_var = tk.StringVar()
category_var = tk.StringVar(value=CATEGORIES[0])
desc_var = tk.StringVar()

tk.Label(form, text="Date (YYYY-MM-DD)", bg=RIGHT_BTN_BG , font=FONT).grid(row=0, column=0, sticky="w")
tk.Entry(form, textvariable=date_var, width=18, bg="#ffffff").grid(row=1, column=0, padx=6, pady=4)

tk.Label(form, text="Amount (₹)", bg=RIGHT_BTN_BG , font=FONT).grid(row=0, column=1, sticky="w")
tk.Entry(form, textvariable=amount_var, width=18, bg="#ffffff").grid(row=1, column=1, padx=6, pady=4)

tk.Label(form, text="Category", bg=RIGHT_BTN_BG , font=FONT).grid(row=0, column=2, sticky="w")
ttk.Combobox(form, values=CATEGORIES, textvariable=category_var, state="readonly", width=16).grid(row=1, column=2, padx=6, pady=4)

tk.Label(form, text="Description", bg=RIGHT_BTN_BG , font=FONT).grid(row=0, column=3, sticky="w")
tk.Entry(form, textvariable=desc_var, width=30, bg="#ffffff").grid(row=1, column=3, padx=6, pady=4)

# Action buttons
action_frame = tk.Frame(main, bg=RIGHT_BTN_BG)
action_frame.pack(fill="x", pady=(0,10))
tk.Button(action_frame, text="Clear Form", command=clear_form, width=12, bg=RIGHT_BTN_BG, fg=RIGHT_BTN_FG).pack(side="left", padx=4)
tk.Button(action_frame, text="Add", command=add_action, width=12, bg=RIGHT_BTN_BG, fg=RIGHT_BTN_FG).pack(side="left", padx=4)
tk.Button(action_frame, text="Update", command=update_action, width=12, bg=RIGHT_BTN_BG, fg=RIGHT_BTN_FG).pack(side="left", padx=4)
tk.Button(action_frame, text="Delete", command=delete_action, width=12, bg=RIGHT_BTN_BG, fg=RIGHT_BTN_FG).pack(side="left", padx=4)


# Message + Totals
msg_var = tk.StringVar()
msg_label = tk.Label(main, textvariable=msg_var, bg=RIGHT_BTN_BG )
msg_label.pack(anchor="w", pady=(4,6))
totals_var = tk.StringVar()
totals_label = tk.Label(main, textvariable=totals_var, bg=RIGHT_BTN_BG, font=("Inter", 10, "bold"))
totals_label.pack(anchor="e", pady=(0,6))

# Table
table_frame = tk.Frame(main, bg=RIGHT_BTN_BG)
table_frame.pack(fill="both", expand=True)
cols = ("ID", "Date", "Amount", "Category", "Description")
tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=120 if c!="Description" else 300, anchor="w")

vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
tree.configure(yscroll=vsb.set, xscroll=hsb.set)
tree.grid(row=0, column=0, sticky="nsew")
vsb.grid(row=0, column=1, sticky="ns")
hsb.grid(row=1, column=0, sticky="ew")
table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)

tree.bind("<<TreeviewSelect>>", on_row_select)

# Style Treeview
style = ttk.Style()
style.theme_use('default')
style.configure("Treeview", background="#ffffff", foreground="#000000", rowheight=25, fieldbackground="#ffffff")
style.map('Treeview', background=[('selected', ACCENT)], foreground=[('selected', '#ffffff')])

# Initialize DB and seed
if data.count_rows() == 0:
    seed_dt.insert_seed_data()
load_table()

root.mainloop()