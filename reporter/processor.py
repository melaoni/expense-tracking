import pandas as pd
from typing import Dict, Tuple
from database.database import create_connection, get_all_transactions, get_all_refunds
from models.models import Transaction, Account, accounts_and_owners, Party
from database.converter import parties_to_set

def get_refunds(conn):
    refunds = pd.read_sql(
        sql='''select r.entry_uuid as entry_uuid, e.amount as original_amount, r.refund_entry_uuid as refund_entry_uuid, e_refund.amount as refund_amount
            from refund r
            left join entry e on r.entry_uuid = e.uuid
            left join entry e_refund on r.refund_entry_uuid = e_refund.uuid ''', 
        con=conn,
    )

    refunded_amount = refunds[['entry_uuid', 'refund_amount']].groupby('entry_uuid').sum()
    original_amount = refunds[['refund_entry_uuid', 'original_amount']].groupby('refund_entry_uuid').sum()

    return refunded_amount, original_amount


def get_reconcile_amount(row, refunded_amount, original_amount):
    amount = row['amount']
    uuid = row['uuid']

    if uuid in refunded_amount.index:
        refunded = refunded_amount.loc[uuid, 'refund_amount']
        amount = amount + refunded if amount + refunded < 0 else 0  # use 0 if the refund is over-refunded
    elif uuid in original_amount.index:
        original = original_amount.loc[uuid, 'original_amount']
        amount = amount + original if amount + original > 0 else 0 # use 0 if the refund isn't enough to cover the original
    
    return amount


def split_amount_to_party(row):
    parties = { party.value for party in parties_to_set(row['parties']) }
    account_owner = accounts_and_owners[Account(row['account'])].value

    split_party = parties.difference({account_owner})
    split_amount = 0 if len(split_party) == 0 else (row['reconciled_amount'] * 1.0 / len(parties))

    return account_owner, ','.join(split_party), split_amount


def compute_refunds_and_splits():
    conn = create_connection()

    transactions = pd.read_sql(
        sql='select uuid, date, account, parties, amount, category, subcategory, item from entry',
        con=conn,
        parse_dates={'date': '%Y-%m-%d'}
    )

    transactions['date_month'] = transactions['date'].dt.strftime('%Y-%m')
    refunded_amount, original_amount = get_refunds(conn)
    transactions['reconciled_amount'] = transactions.apply(
        lambda row: get_reconcile_amount(row, refunded_amount, original_amount),
        axis=1
    )

    transactions[['account_owner', 'split_party', 'split_cost']]= transactions.apply(split_amount_to_party, axis=1, result_type='expand')

    print(transactions)
    
    reconciled_sum = transactions['reconciled_amount'].sum()
    original_sum = transactions['amount'].sum()

    if reconciled_sum != original_sum:
        raise Exception('Failed to reconcile post refund amount and original mount')

    return transactions
