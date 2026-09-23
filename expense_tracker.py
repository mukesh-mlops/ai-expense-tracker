import sqlite3
import csv
import os
from datetime import datetime

# ══════════════════════════════════════════════════
# P1 — AI-POWERED EXPENSE TRACKER
# github.com/mukesh-mlops/ai-expense-tracker
# Built by: S. Mukesh Kumar
# ══════════════════════════════════════════════════

DB_FILE  = "expenses.db"
CSV_FILE = "expenses_export.csv"

def get_category(description):
    """AI categorisation — keyword fallback (works without API key)
    REAL OpenAI version:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"Reply ONE word only: Food,Transport,Entertainment,Utilities,Shopping,Health,Education,Other"},
            {"role":"user","content":description}
        ],
        max_tokens=5, temperature=0
    )
    return response.choices[0].message.content.strip()
    """
    desc = description.lower()
    if any(w in desc for w in ["swiggy","zomato","food","lunch","dinner","coffee","blinkit","grocery","restaurant"]):
        return "Food"
    elif any(w in desc for w in ["ola","uber","bus","train","metro","petrol","auto","cab","rapido"]):
        return "Transport"
    elif any(w in desc for w in ["netflix","amazon prime","movie","game","spotify","hotstar","concert"]):
        return "Entertainment"
    elif any(w in desc for w in ["electricity","water","wifi","internet","rent","bill","recharge","gas"]):
        return "Utilities"
    elif any(w in desc for w in ["amazon","flipkart","clothes","shoes","mobile","laptop","meesho"]):
        return "Shopping"
    elif any(w in desc for w in ["hospital","doctor","medicine","pharmacy","apollo","clinic"]):
        return "Health"
    elif any(w in desc for w in ["book","course","college","fees","tuition","udemy","study"]):
        return "Education"
    else:
        return "Other"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.cursor().execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT    NOT NULL,
            amount      REAL    NOT NULL,
            category    TEXT    DEFAULT 'Other',
            date        TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_expense(description, amount):
    try:
        if not description.strip():
            raise ValueError("Description cannot be empty!")
        if amount <= 0:
            raise ValueError("Amount must be positive!")
        category = get_category(description)
        date     = datetime.now().strftime("%Y-%m-%d")
        conn     = sqlite3.connect(DB_FILE)
        conn.cursor().execute(
            "INSERT INTO transactions (description,amount,category,date) VALUES (?,?,?,?)",
            (description, amount, category, date)
        )
        conn.commit()
        conn.close()
        print(f"\n  Added: {description} | Rs.{amount:.2f} | Category: {category}")
    except ValueError as e:
        print(f"\n  Error: {e}")

def view_expenses():
    conn = sqlite3.connect(DB_FILE)
    rows = conn.cursor().execute(
        "SELECT id,description,amount,category,date FROM transactions ORDER BY date DESC"
    ).fetchall()
    conn.close()
    if not rows:
        print("\n  No expenses found.")
        return
    print(f"\n  {'ID':<4} {'Description':<22} {'Amount':>9} {'Category':<15} {'Date'}")
    print("  " + "─"*65)
    for r in rows:
        print(f"  {r[0]:<4} {r[1]:<22} Rs.{r[2]:>7.2f} {r[3]:<15} {r[4]}")

def monthly_report():
    conn   = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    month  = datetime.now().strftime("%Y-%m")
    rows   = cursor.execute("""
        SELECT category, COUNT(*), SUM(amount)
        FROM transactions WHERE date LIKE ?
        GROUP BY category ORDER BY SUM(amount) DESC
    """, (f"{month}%",)).fetchall()
    total  = cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE date LIKE ?",
        (f"{month}%",)
    ).fetchone()[0] or 0
    conn.close()
    if not rows:
        print(f"\n  No expenses for {month}")
        return
    print(f"\n  Monthly Report — {month}")
    print("  " + "="*50)
    for r in rows:
        bar = "█" * min(int(r[2]/100), 20)
        print(f"  {r[0]:<15} {r[1]:>3} items  Rs.{r[2]:>8.2f}  {bar}")
    print("  " + "─"*50)
    print(f"  {'TOTAL':<15}          Rs.{total:>8.2f}")

def export_csv():
    conn = sqlite3.connect(DB_FILE)
    rows = conn.cursor().execute("SELECT * FROM transactions").fetchall()
    conn.close()
    with open(CSV_FILE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ID","Description","Amount","Category","Date"])
        w.writerows(rows)
    print(f"\n  Exported {len(rows)} records to {CSV_FILE}")

def delete_expense(eid):
    conn = sqlite3.connect(DB_FILE)
    conn.cursor().execute("DELETE FROM transactions WHERE id=?", (eid,))
    conn.commit()
    conn.close()
    print(f"\n  Deleted expense ID {eid}")

def main():
    init_db()
    print("\n" + "="*50)
    print("   AI-POWERED EXPENSE TRACKER")
    print("   github.com/mukesh-mlops/ai-expense-tracker")
    print("   Built by: S. Mukesh Kumar")
    print("="*50)
    while True:
        print("\n  1 — Add expense (AI auto-categorises)")
        print("  2 — View all expenses")
        print("  3 — Monthly report")
        print("  4 — Export to CSV")
        print("  5 — Delete expense")
        print("  6 — Exit")
        choice = input("\n  Choice: ").strip()
        if choice == "1":
            desc = input("  Description : ").strip()
            try:
                amt = float(input("  Amount Rs.  : "))
                add_expense(desc, amt)
            except ValueError:
                print("  Enter valid number for amount")
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_report()
        elif choice == "4":
            export_csv()
        elif choice == "5":
            view_expenses()
            try:
                eid = int(input("\n  Enter ID to delete: "))
                delete_expense(eid)
            except ValueError:
                print("  Enter valid ID")
        elif choice == "6":
            print("\n  Expense Tracker closed!")
            break
        else:
            print("  Enter 1 to 6 only")

main()