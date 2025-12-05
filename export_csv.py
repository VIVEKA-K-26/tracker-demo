import csv

def export_to_csv(path, rows):
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Date", "Amount", "Category", "Description"])
        for r in rows:
            writer.writerow([r["id"], r["date"], r["amount"], r["category"], r["description"]])

