from reporter.processor import compute_refunds_and_splits



if __name__ == '__main__':
    transactions = compute_refunds_and_splits()

    groupby_month_account = transactions.groupby(['date_month','account_owner', 'split_party'])['split_cost'].sum() / 100.0
    print(groupby_month_account)