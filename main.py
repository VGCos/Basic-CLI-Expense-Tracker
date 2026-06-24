from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
import os

app = FastAPI()

class Expense(BaseModel):
    cost: float
    description: str
    

def initialize_csv():
    if not os.path.exists('expenses.csv'):
        with open('expenses.csv', 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'cost', 'description'])

def get_next_id():
    if not os.path.exists('expenses.csv'):
        initialize_csv()
        return 1
    
    next_id = 0

    with open('expenses.csv', newline='') as f:
        reader = csv.DictReader(f)

        for row in reader:
            next_id = max(next_id, int(row['id']))

    return next_id + 1


def adding_expense(next_id, cost, description):
    payload = [next_id, cost, description]
    with open('expenses.csv', mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(payload)

    return {'id': next_id, 'cost': cost, 'description': description}


def get_all_expenses():
    expenses = []
    with open('expenses.csv', mode='r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append({
                'id': int(row['id']),
                'cost': float(row['cost']),
                'description': row['description']
            })

    return expenses

def rewrite_csv(expenses):
    with open('expenses.csv', mode='w', newline='') as f:
        writer = csv.DictWriter(f, ['id', 'cost', 'description'])

        writer.writeheader()
        writer.writerows(expenses)


@app.get("/")
def read_root():
    return {"message": "Hello bozo, use /expenses at the end to do stuff"}


@app.get("/expenses")
def get_items():
    initialize_csv()
    return get_all_expenses()


@app.post("/expenses")
def post_item(expense: Expense):
    next_id = get_next_id()
    new_item = adding_expense(next_id, expense.cost, expense.description)
    return new_item


@app.put("/expenses/{expense_id}")
def update_item(expense_id: int, expense: Expense):
    expenses = get_all_expenses()
    found = False
    
    for item in expenses:
        if item['id'] == expense_id:
            item['cost'] = expense.cost
            item['description'] = expense.description
            found = True
            break
    if not found:
        raise HTTPException(404, "Expense not found")

    rewrite_csv(expenses)
    return {"message": f"Updated expense with ID {expense_id}"}


@app.delete("/expenses/{expense_id}")
def delete_item(expense_id: int):
    expenses = get_all_expenses()
    
    new_expenses = [e for e in expenses if e['id'] != expense_id]
    if len(expenses) == len(new_expenses):
        raise HTTPException(404, "Expense not found")

    rewrite_csv(new_expenses)

    return {"message": f"Deleted expense with ID {expense_id}"}


@app.get("/expenses/summary")
def summarize_items():
    expenses = get_all_expenses()
    costs = [float(e['cost']) for e in expenses]
    costs.sort()

    count = len(costs)
    median = None
    mean = None
    maxx = None
    minn = None

    if count != 0:
        if count & 1:
            median = costs[count // 2]
        else:
            median = (costs[count // 2] + costs [count // 2 - 1]) / 2
        
        mean = sum(costs) / count
        maxx = costs[-1]
        minn = costs[0]

    return {"count": count, 
            "median": median, 
            "mean": mean, 
            "max": maxx, 
            "min": minn}


