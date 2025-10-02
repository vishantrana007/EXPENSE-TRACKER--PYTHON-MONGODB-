# =============================
# MAIN.PY - EXPENSE TRACKER
# =============================
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
import os

# -----------------------------
# 1️⃣ Load Environment Variables
# -----------------------------
load_dotenv()  # Load .env file

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "Expense_Tracker")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "Expenses")

# -----------------------------
# 2️⃣ MongoDB Setup
# -----------------------------
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# -----------------------------
# 3️⃣ Functions
# -----------------------------

# ---- Add Expense ----
def add_expense():
    title = input("Enter expense title: ").strip()

    while True:
        try:
            amount = float(input("Enter expense amount: "))
            break
        except ValueError:
            print("⚠️ Invalid input. Please enter a numeric value for amount.")

    category = input("Enter expense category: ").strip()

    while True:
        date_str = input("Enter expense date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("⚠️ Invalid date format. Please use YYYY-MM-DD.")

    expense_data = {
        "title": title,
        "amount": amount,
        "category": category,
        "date": date_str
    }

    inserted_id = collection.insert_one(expense_data).inserted_id
    print(f"✅ Expense added with ID: {inserted_id}\n")


# ---- View Expenses ----
def view_expenses():
    print("\nAll Expenses:")
    for exp in collection.find():
        print(f"{exp['_id']} | {exp['date']} | {exp['title']} | {exp['category']} | {exp['amount']}")
    print()


# ---- Update Expense ----
def update_expense():
    expense_id = input("Enter Expense ID to update: ").strip()
    if not ObjectId.is_valid(expense_id):
        print("⚠️ Invalid ID format.\n")
        return

    field = input("Which field to update (title/amount/category/date): ").lower().strip()
    if field not in ["title", "amount", "category", "date"]:
        print("⚠️ Invalid field.\n")
        return

    new_value = input("Enter new value: ").strip()
    if field == "amount":
        try:
            new_value = float(new_value)
        except ValueError:
            print("⚠️ Amount must be numeric.\n")
            return
    if field == "date":
        try:
            datetime.strptime(new_value, "%Y-%m-%d")
        except ValueError:
            print("⚠️ Invalid date format. Use YYYY-MM-DD.\n")
            return

    result = collection.update_one(
        {"_id": ObjectId(expense_id)},
        {"$set": {field: new_value}}
    )
    if result.modified_count > 0:
        print("✅ Expense updated successfully.\n")
    else:
        print("⚠️ No matching expense found.\n")


# ---- Delete Expense ----
def delete_expense():
    expense_id = input("Enter Expense ID to delete: ").strip()
    if not ObjectId.is_valid(expense_id):
        print("⚠️ Invalid ID format.\n")
        return

    result = collection.delete_one({"_id": ObjectId(expense_id)})
    if result.deleted_count > 0:
        print("✅ Expense deleted successfully.\n")
    else:
        print("⚠️ No matching expense found.\n")


# ---- Monthly Summary ----
def monthly_summary():
    try:
        month = int(input("Enter month (MM): "))
        year = int(input("Enter year (YYYY): "))
    except ValueError:
        print("⚠️ Invalid input. Month and Year must be numbers.\n")
        return

    total = 0
    print(f"\nExpenses for {month:02d}-{year}:")
    for exp in collection.find():
        try:
            exp_date = datetime.strptime(exp['date'], "%Y-%m-%d")
            if exp_date.month == month and exp_date.year == year:
                print(f"{exp['date']} | {exp['title']} | {exp['category']} | {exp['amount']}")
                total += exp['amount']
        except:
            continue
    print(f"\nTotal Expenses in {month:02d}-{year}: {total}\n")


# ---- Category-wise Report ----
def category_report():
    category_totals = {}
    for exp in collection.find():
        cat = exp['category']
        category_totals[cat] = category_totals.get(cat, 0) + exp['amount']

    print("\nSpending by Category:")
    for cat, amt in category_totals.items():
        print(f"{cat}: {amt}")
    print()


# -----------------------------
# 4️⃣ Main Menu
# -----------------------------
def main():
    while True:
        print("=== EXPENSE TRACKER MENU ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Monthly Summary")
        print("6. Category-wise Report")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            update_expense()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            monthly_summary()
        elif choice == "6":
            category_report()
        elif choice == "0":
            print("Exiting Expense Tracker. Bye!")
            break
        else:
            print("⚠️ Invalid choice. Try again.\n")


# -----------------------------
# 5️⃣ Run Program
# -----------------------------
if __name__ == "__main__":
    main()
