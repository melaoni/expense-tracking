import csv
from datetime import datetime
from typing import List, Tuple, Dict
from models.models import Transaction, Account, Demand, Category, Subcategory, Party

# mastersheet_file = "./parser/Expense tracking 2020 - Master.csv"
mastersheet_file = "./parser/mastersheet.csv"

def read_mastersheet() -> Tuple[List[Transaction],List[Dict]]:
    transactions=[]
    refunds=[]

    with open(mastersheet_file, newline='') as file:
        mastersheet = csv.reader(file, delimiter=',')
        next(mastersheet) # skip total headers
        next(mastersheet) # skip total numbers
        next(mastersheet) # skip headers
        
        for row in mastersheet:
            transactions.append(to_transaction(row))
            refund = to_refund(row)
            if refund:
                refunds.append(to_refund(row))
    
    return (transactions, refunds)

def to_transaction(row) -> Transaction:
    return Transaction(
        uuid=row[0],
        date=datetime.strptime(row[1], "%m/%d/%y").date(),
        amount=float(row[3]) * 100,
        account=Account(row[4]),
        demand=Demand(row[5]),
        category=Category(row[6]),
        subcategory=Subcategory(row[7]) if row[7] else None,
        item=row[8] if row[8] else None,
        merchant=row[9],
        parties=set(list(Party)) if row[10] == "Both" else set([Party(row[10])]),
        description=row[11],
        note=row[16] if row[16] else None
    )

def to_refund(row) -> Tuple[str, str]:
    # refunded id - , refund id +
    return (row[12], row[0]) if row[12] else None
