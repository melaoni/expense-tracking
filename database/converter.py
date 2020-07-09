from datetime import date
from uuid import uuid4
from typing import Set
from models.models import Transaction, Account, Demand, Category, Subcategory, Party

party_joiner = ','

def to_db_entry(transaction: Transaction):
    entry = (
        transaction.uuid if transaction.uuid else uuid4(),
        transaction.date.isoformat(),
        transaction.account.value,
        transaction.demand.value,
        transaction.category.value,
        transaction.subcategory.value if transaction.subcategory is not None else None,
        transaction.item,
        transaction.merchant,
        party_joiner.join([party.value for party in transaction.parties]),
        transaction.description,
        transaction.amount,
        transaction.note
    )
    print(entry)
    return entry

def from_db_entry(entry):
    # print(entry)
    return Transaction(
        id=entry[0],
        uuid=entry[1],
        date=date.fromisoformat(entry[2]),
        account=Account(entry[3]),
        demand=Demand(entry[4]),
        category=Category(entry[5]),
        subcategory=Subcategory(entry[6]) if entry[6] is not None else None,
        item=entry[7],
        merchant=entry[8],
        parties=parties_to_set(entry[9]),
        description=entry[10],
        amount=entry[11],
        note=entry[12]
    )

def parties_to_set(parties: str) -> Set[Party]:
    return set([Party(party) for party in parties.split(party_joiner)])