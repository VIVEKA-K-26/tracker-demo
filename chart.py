# charts.py
import matplotlib.pyplot as plt
from collections import defaultdict

def plot_category_pie(rows):
    # rows: iterable of sqlite3.Row
    totals = defaultdict(float)
    for r in rows:
        # r supports dict-like access
        totals[r["category"]] += float(r["amount"])

    if not totals:
        plt.figure(figsize=(4,3))
        plt.text(0.5, 0.5, "No data to display", ha="center", va="center")
        plt.axis("off")
        plt.show()
        return

    labels = list(totals.keys())
    sizes = list(totals.values())

    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Expenses by Category")
    plt.tight_layout()
    plt.show()
