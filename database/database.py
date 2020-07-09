import sqlite3
from sqlite3 import Error
from typing import Dict, Tuple, List
from models.models import Transaction
from .converter import to_db_entry, from_db_entry

def create_connection(db_file=r"./database/sqlite.db"):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_transaction(conn, transaction: Transaction):
    sql = '''INSERT INTO entry(uuid,date,account,demand,category,subcategory,item,merchant,parties,description,amount,note)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'''

    cur = conn.cursor()
    cur.execute(sql, to_db_entry(transaction))
    return cur.lastrowid

def get_transaction(conn, uuid:str) -> Transaction:
    sql = ''' SELECT id,uuid,date,account,demand,category,subcategory,item,merchant,parties,description,amount,note
              FROM entry
              WHERE uuid = ?'''

    cur = conn.cursor()
    cur.execute(sql, (uuid,))

    rows = cur.fetchall()
    
    if len(rows) > 1:
        raise Error(f"Found more than 1 record with uuid {uuid}")

    if len(rows) < 1:
        return None

    return from_db_entry(rows[0])

def get_all_transactions(conn) -> Dict[str, Transaction]:
    sql = ''' SELECT id,uuid,date,account,demand,category,subcategory,item,merchant,parties,description,amount,note
              FROM entry'''

    cur = conn.cursor()
    cur.execute(sql)

    return {row[1]:from_db_entry(row) for row in cur.fetchall()}


def insert_refund(conn, refund: Tuple[str, str]):
    sql = '''INSERT INTO refund(entry_uuid, refund_entry_uuid)
             VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, refund)
    return cur.lastrowid

# def get_refund(conn, entry_uuid:str) -> Tuple[str, str]:
#     sql = '''SELECT refund_entry_uuid FROM refund WHERE entry_uuid = ?'''
#     cur = conn.cursor()
#     cur.execute(sql, (entry_uuid,))
#    return cur.fetchall()

def get_all_refunds(conn) -> Tuple[Tuple[str,str], ...]:
    sql = '''SELECT entry_uuid, refund_entry_uuid FROM refund'''
    cur = conn.cursor()
    cur.execute(sql)

    return cur.fetchall()
    