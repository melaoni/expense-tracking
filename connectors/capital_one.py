import csv
from datetime import date
import pandas as pd
from .importer import Importer
from models.models import Account, Demand, Category, Subcategory, Party, Transaction

checking_file = "/Users/mejiang/Downloads/2021-03-06_360Checking...0701.csv"
saving_file = "/Users/mejiang/Downloads/2021-03-06_360MoneyMarket...9367.csv"
discover_file = "/Users/mejiang/Downloads/DFS-Search-20210306.csv"
freedome_file = "/Users/mejiang/Downloads/Chase1205_Activity20210101_20210306_20210306.CSV"
sapphire_file = "/Users/mejiang/Downloads/Chase3521_Activity20210101_20210306_20210306.CSV"

# Date, Amount, Source, Description

class CapitalOneCheckingImporter(Importer):
    def __init__(self):
        Importer.__init__(self, file=checking_file, skip_rows=1, date_format='%m/%d/%y')

    def convert_row_to_mastersheet_entry(self, row):
        return [row[1], row[2], Account.capital_one_checking.value, row[4]]

class CapitalOneSavingImporter(Importer):
    def __init__(self):
        Importer.__init__(self, file=saving_file, skip_rows=1, date_format='%m/%d/%y')

    def convert_row_to_mastersheet_entry(self, row):
        return [row[1], row[2], Account.capital_one_saving.value, row[4]]

class DiscoverImporter(Importer):
    def __init__(self):
        Importer.__init__(self, file=discover_file, skip_rows=1, date_format='%m/%d/%Y')

    def convert_row_to_mastersheet_entry(self, row):
        return [row[0], -1 * float(row[3]), Account.discover.value, row[2]]

class ChaseFreedomImporter(Importer):
    def __init__(self):
        Importer.__init__(self, file=freedome_file, skip_rows=1, date_format='%m/%d/%Y')

    def convert_row_to_mastersheet_entry(self, row):
        return [row[0], row[5], Account.freedom.value, row[2]]

class ChaseSapphireImporter(Importer):
    def __init__(self):
        Importer.__init__(self, file=sapphire_file, skip_rows=1, date_format='%m/%d/%Y')

    def convert_row_to_mastersheet_entry(self, row):
        return [row[0], row[5], Account.sapphire.value, row[2]]



importers = [
    CapitalOneCheckingImporter(), 
    CapitalOneSavingImporter(),
    DiscoverImporter(),
    ChaseFreedomImporter(),
    ChaseSapphireImporter()
]
