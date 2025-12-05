import data

def insert_seed_data():
    sample = [
        ("2025-01-01", 200, "Food", "Breakfast"),
        ("2025-01-02", 850, "Travel", "Auto fare"),
        ("2025-01-03", 1200, "Shopping", "T-shirt"),
        ("2025-01-04", 400, "Food", "Snacks"),
    ]

    for date, amt, cat, desc in sample:
        data.add_expense(date, amt, cat, desc)

if __name__ == '__main__':
    data.init_db()
    insert_seed_data()
    print("Seed data inserted!")
