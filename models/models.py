from datetime import date
from enum import Enum
from typing import Optional, Set

class Account(Enum):
    amazon_chase="Amazon Chase"
    boa_checking="BOA Checking"
    boa_credit="BOA Credit"
    capital_one_checking="Checking Capital One"
    capital_one_saving="Saving Capital One"
    discover="Discover"
    freedom="Freedom"
    sapphire="Sapphire"
    venmo_melanie="Venmo Melanie"

class Owner(Enum):
    sadruddin="Sadruddin"
    melanie="Melanie"

accounts_and_owners = {
    Account.amazon_chase: Owner.sadruddin,
    Account.boa_checking: Owner.sadruddin,
    Account.boa_credit: Owner.sadruddin,
    Account.capital_one_checking: Owner.melanie,
    Account.capital_one_saving: Owner.melanie,
    Account.discover: Owner.melanie,
    Account.freedom: Owner.melanie,
    Account.sapphire: Owner.melanie,
    Account.venmo_melanie: Owner.melanie,
}

class Demand(Enum):
    inelastic="Inelastic"
    elastic="Elastic"
    payment="Payment"
    income="Income"
    transfer="Transfer"

demand_postive = [Demand.income, Demand.payment]
demand_negative = [Demand.inelastic, Demand.elastic]

class Category(Enum):
    aa="AA"
    cashback="Cashback"
    clothing="Clothing"
    communication="Communication"
    credit_payment="Credit Payment"
    eat="Eat"
    entertainment="Entertainment"
    family="Family"
    gift="Gift"
    health="Health"
    household="Household"
    housing="Housing"
    interest="Interest"
    other="Other"
    payment="Payment"
    personal_improvement="Personal Improvement"
    poker="Poker"
    salary="Salary"
    saving="Saving"
    social="Social"
    stock="Stock"
    travel="Travel"
    utility="Utility"
    general="日用品" #TODO - remove?

class Subcategory(Enum):
    bag="Bag"
    bill="Bill"
    clothes="Clothes"
    coffee="Coffee"
    donation="Donation"
    drink="Drink"
    experience="Experience"
    fee="Fee"
    food="Food"
    gadget="Gadget"
    game="Game"
    gym="Gym"
    household="Household" # TODO - remove?
    hygene="Hygene"
    insurance="Insurance"
    kitchen="Kitchen"
    learn="Learn"
    loan="Loan"
    lodging="Lodging"
    mental="Mental"
    monthly="Monthly" # TODO - what is this?
    music="Music"
    other="Other"
    refund="Refund"
    rent="Rent"
    skincare="Skincare"
    snack="Snack"
    subscription="Subscription"
    supplements="Supplements"
    tools="Tools"
    transportation="Transportation"
    video="Video"
    withdraw="Withdraw"

class Party(Enum):
    # The string value needs to be same as the Owner values
    sadruddin="Sadruddin"
    melanie="Melanie"

class Transaction:
    id: Optional[int]
    uuid: Optional[str]
    date: date
    account: Account
    demand: Demand
    category: Category
    subcategory: Optional[Subcategory]
    item: Optional[str]
    merchant: Optional[str]
    parties: Set[Party]
    description: str
    amount: int
    note: Optional[str]

    def __init__(self, id=None, uuid=None, date=None, account=None, demand=None, category=None, subcategory=None, item=None, merchant=None, parties=None, description=None, amount=None, note=None):
        self.id = id
        self.uuid = uuid
        self.date = date
        self.account = account
        self.demand = demand
        self.category = category
        self.subcategory = subcategory
        self.item = item
        self.merchant = merchant
        self.parties = parties
        self.description = description
        self.amount = amount
        self.note = note

    def get_account_owner(self):
        return accounts_and_owners[self.account]

    def get_decimal_amount(self):
        return self.amount / 100.0

    def validate(self):
        if amount < 0 and demand in demand_postive:
            raise Error(f"transaction ${self.uuid} has negative amount ${self.amount} for demand {self.demand}")
        if amount > 0 and demand in demand_negative:
            raise Error(f"transaction ${self.uuid} has positive amount ${self.amount} for demand {self.demand}")
        if merchant is None and demand in demand_negative:
            raise Error(f"transaction ${self.uuid} has no merchant for demand {self.demand}")
        
