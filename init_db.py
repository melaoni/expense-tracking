from database.database import create_connection, create_table


sql_create_transaction_table = """CREATE TABLE IF NOT EXISTS entry (
                                    id integer PRIMARY KEY,
                                    uuid text NOT NULL UNIQUE,
                                    date text NOT NULL,
                                    account text NOT NULL,
                                    demand text NOT NULL,
                                    category text NOT NULL,
                                    subcategory text,
                                    item text,
                                    merchant text,
                                    parties text NOT NULL,
                                    description text NOT NULL,
                                    amount integer NOT NULL,
                                    note text
                                );"""

sql_create_refund_table = """CREATE TABLE IF NOT EXISTS refund (
                                entry_uuid integer NOT NULL,
                                refund_entry_uuid integer NOT NULL,
                                PRIMARY KEY (entry_uuid, refund_entry_uuid)
                            );"""


if __name__ == '__main__':
    database = r"./database/sqlite.db"
    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_transaction_table)
        create_table(conn, sql_create_refund_table)
    else:
        print("Error! cannot create the database connection.")

    conn.close()

    