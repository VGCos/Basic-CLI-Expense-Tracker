# Basic-CLI-Expense-Tracker
Basic CLI expense tracker that uses FastAPI.

## General format
python args.py <command> [arguments]

---

## Add an expense
python args.py add <amount> <description>

Example:
python args.py add 10.0 food
python args.py add 12.5 "lunch with friends"

---

## List all expenses
python args.py list

Example output:
ID    Cost       Description
----------------------------------------
1     $10.00     food
2     $12.50     lunch with friends

---

## Update an expense
python args.py update <id> <amount> <description>

Example:
python args.py update 2 15.0 "dinner with friends"

---

## Delete an expense
python args.py delete <id>

Example:
python args.py delete 2

---

## Summary of expenses
python args.py summary

Example output:
{
    "count": 3,
    "mean": 12.5,
    "median": 10.0,
    "min": 5.0,
    "max": 20.0
}

---

## Notes
- Use quotes for multi-word descriptions:
  "coffee with team"
- IDs are auto-generated when adding expenses
- Data is stored in a local CSV file