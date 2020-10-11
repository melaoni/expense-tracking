from reporter.processor import compute_refunds_and_splits
import sqlite3
import pandas as pd
from database.database import create_connection
import pdb
import plotly.express as px
import plotly.graph_objects as go

if __name__ == '__main__':
    transactions = compute_refunds_and_splits()
    transactions['is_positive'] = transactions.apply(
        lambda row: row['reconciled_amount'] > 0,
        axis=1
    )
    transactions['reconciled_amount_floating_point'] = transactions.apply(
        lambda row: row['reconciled_amount'] / 100.0,
        axis=1
    )
    transactions['reconciled_amount_floating_point_after_split'] = transactions.apply(
        lambda row: (row['reconciled_amount'] - row['split_cost']) / 100.0,
        axis=1
    )
    transactions = transactions.loc[transactions['account_owner'] == 'Sadruddin']

    transactions_grouped_by_month = transactions.groupby(['date_month', 'is_positive', 'category'])
    summed_transactions = transactions_grouped_by_month['reconciled_amount_floating_point_after_split'].sum().reset_index(name ='sum')

    positive_transactions = summed_transactions.loc[summed_transactions['is_positive'] == True]
    negative_transactions = summed_transactions.loc[summed_transactions['is_positive'] == False]

    net_transactions = transactions.groupby(['date_month'])
    summed_net_transactions = net_transactions['reconciled_amount_floating_point_after_split'].sum().reset_index(name ='sum')

    negative_transactions_by_category = dict(tuple(negative_transactions.groupby('category')))
    positive_transactions_by_category = dict(tuple(positive_transactions.groupby('category')))

    bars = []
    # for category, transactions in negative_transactions_by_category.items():
    #     bars.append(
    #         go.Bar(
    #             name='{} (negative)'.format(category),
    #             x=transactions['date_month'].tolist(),
    #             y=transactions['sum'].tolist(),
    #         )
    #     )
    # for category, transactions in positive_transactions_by_category.items():
    #     bars.append(
    #         go.Bar(
    #             name='{} (positive)'.format(category),
    #             x=transactions['date_month'].tolist(),
    #             y=transactions['sum'].tolist(),
    #         )
    #     )
    bars.append(
        go.Bar(
            marker_color='yellow',
            name='Net',
            x=summed_net_transactions['date_month'].tolist(),
            y=summed_net_transactions['sum'].tolist(),
        )
    )

    # fig = go.Figure(data=[
    #     go.Bar(marker_color='red', name='Negative', x=negative_transactions['date_month'].tolist(), y=negative_transactions['sum'].tolist()),
    #     go.Bar(marker_color='green', name='Positive', x=positive_transactions['date_month'].tolist(), y=positive_transactions['sum'].tolist()),
    #     go.Bar(marker_color='yellow', name='Net', x=summed_net_transactions['date_month'].tolist(), y=summed_net_transactions['sum'].tolist()),
    # ])
    fig = go.Figure(data=bars)
    fig.update_layout(title="Total breakdown", barmode='stack')
    fig.show()

    print(summed_transactions)
