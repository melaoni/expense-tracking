from reporter.processor import compute_refunds_and_splits

import pandas as pd

if __name__ == '__main__':
    transactions = compute_refunds_and_splits()
    # with pd.option_context('display.max_rows', None):
    #     print(transactions.loc[transactions.amount > 0])

    groupby_month_account = transactions.groupby(['date_month','account_owner', 'split_party'])['split_cost'].sum() / 100.0

    groupby_month_account.columns = ['date_month', 'account_owner', 'split_party', 'amount']
    groupby_month_account = groupby_month_account[groupby_month_account < 0]
    print(groupby_month_account)

    # print(transactions)

    # may_trans = transactions.loc[(transactions['date_month'] == '2020-05') & (transactions['account_owner'] == 'Sadruddin') & (transactions['split_party'] == 'Melanie')]

    # print(may_trans)