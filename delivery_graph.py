import sqlite3
import pandas as pd
from database.database import create_connection
import pdb
import plotly.express as px
import plotly.graph_objects as go

if __name__ == '__main__':
    conn = create_connection()

    transactions = pd.read_sql(
        sql='select uuid, date, account, parties, amount, category, subcategory, item from entry',
        con=conn,
        parse_dates={'date': '%Y-%m-%d'}
    )
    transactions['real_amount'] = transactions.apply(
        lambda row: row['amount'] / -100.0,
        axis=1
    )
    transactions['month'] = transactions.apply(
        lambda row: row['date'].strftime('%m'),
        axis=1
    )
    transactions = transactions.groupby(['month', 'item', 'category'])
    transactions = transactions['real_amount'].sum().reset_index(name ='Total Amount')

    eat_transactions = transactions.loc[transactions['category'].isin(['Eat'])]
    delivery_transactions = eat_transactions.loc[eat_transactions['item'].isin(['Delivery', 'Takeout' 'Coke'])]
    food_court_transactions = eat_transactions.loc[eat_transactions['item'].isin(['Food court', 'Cafe', 'Ice Cream', 'Bubble Tea'])]
    restaurants_transactions = eat_transactions.loc[eat_transactions['item'].isin(['Restaurant', 'Taxi'])]
    grocery_transactions = eat_transactions.loc[eat_transactions['item'].isin(['Grocery', 'Subscription'])]


    fig = go.Figure(data=[
        go.Bar(marker_color='red', name='Delivery', x=delivery_transactions['month'].tolist(), y=delivery_transactions['Total Amount'].tolist()),
        go.Bar(marker_color='blue', name='Food court', x=food_court_transactions['month'].tolist(), y=food_court_transactions['Total Amount'].tolist()),
        go.Bar(marker_color='yellow', name='Restaurant', x=restaurants_transactions['month'].tolist(), y=restaurants_transactions['Total Amount'].tolist()),
        go.Bar(marker_color='grey', name='Grocery', x=grocery_transactions['month'].tolist(), y=grocery_transactions['Total Amount'].tolist()),
    ])
    fig.update_layout(barmode='stack', title="Eat category breakdown")
    fig.show()
