from datetime import date
from models.models import Account, Demand, Category, Subcategory, Party, Transaction
from database.database import create_connection, insert_transaction, get_transaction, insert_refund
from parser.mastersheeet_parser import read_mastersheet

if __name__ == '__main__':
    database = r"./database/sqlite.db"
    conn = create_connection(database)
    with conn:
        transactions, refunds = read_mastersheet()
        for transaction in transactions:
            insert_transaction(conn, transaction)
        
        for refund in refunds: 
            insert_refund(conn, refund)
