from fastapi import HTTPException
import argparse
import requests

parser = argparse.ArgumentParser()

sub_parser = parser.add_subparsers(dest="command", required=True)

add_parser = sub_parser.add_parser("add")
add_parser.add_argument("cost", type=float)
add_parser.add_argument("description", type=str)

list_parser = sub_parser.add_parser("list")

delete_parser = sub_parser.add_parser("delete")
delete_parser.add_argument("id", type=int)

update_parser = sub_parser.add_parser("update")
update_parser.add_argument("id", type=int)
update_parser.add_argument("cost", type=float)
update_parser.add_argument("description", type=str)

summary_parser = sub_parser.add_parser("summary")

args = parser.parse_args()
args_dict = vars(args)


url = "http://127.0.0.1:8000/expenses"

def print_expense(expense):
    print("Expense Details")
    print("-" * 20)
    print(f"ID          : {expense['id']}")
    print(f"Cost        : ${float(expense['cost']):.2f}")
    print(f"Description : {expense['description']}")

def print_all_expenses(expenses):
    print(f"{'ID':<5} {'Cost':<10} Description")
    print("-" * 40)

    for e in expenses:
        print(f"{e['id']:<5} ${float(e['cost']):<9.2f} {e['description']}")

def print_summary(summary):
    print("=== Expense Summary ===")
    print(f"Count   : {summary['count']}")
    print(f"Mean    : {summary['mean']:.2f}")
    print(f"Median  : {summary['median']:.2f}")
    print(f"Min     : {summary['min']}")
    print(f"Max     : {summary['max']}")


def add_expense(cost: float, description: str):
    payload = {"cost": cost, "description": description}
    response = requests.post(url, json=payload)

    if response.status_code == 400:
        print("400 Bad Request, expense cost cannot be negative")
        return
    
    print_expense(response.json())



def list_expenses():
    response = requests.get(url)

    response.raise_for_status()
    print_all_expenses(response.json())


def delete_expense(expense_id: int):
    full_url = f"http://127.0.0.1:8000/expenses/{expense_id}"
    response = requests.delete(full_url)

    if response.status_code == 404:
        print("404 Not Found, expense ID does not exist")
        return
    
    msg = response.json()
    print(msg['message'])

def update_expense(expense_id: int, cost: float, description: str):
    full_url = f"http://127.0.0.1:8000/expenses/{expense_id}"
    payload = {"cost": cost, "description": description}
    response = requests.put(full_url, json=payload)

    if response.status_code == 404:
        print("404 Not Found, expense ID does not exist")
        return
    elif response.status_code == 400:
        print("400 Bad Request, expense cost cannot be negative")
        return
    
    msg = response.json()
    print(msg['message'])



def summarize_expenses():
    full_url = f"http://127.0.0.1:8000/expenses/summary"
    response = requests.get(full_url)

    print_summary(response.json())



command = args_dict["command"]

match command:
    case "add":
        print("Doing add")
        cost = args_dict["cost"]
        description = args_dict["description"]

        add_expense(cost, description)

    case "list":
        print("Doing list")

        list_expenses()

    case "delete":
        print("Doing delete")
        expense_id = args_dict["id"]

        delete_expense(expense_id)

    case "update":
        print("Doing update")
        expense_id = args_dict["id"]
        cost = args_dict["cost"]
        description = args_dict["description"]

        update_expense(expense_id, cost, description)

    case "summary":
        print("Doing summary")

        summarize_expenses()
