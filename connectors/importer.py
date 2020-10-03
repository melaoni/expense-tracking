import csv
import uuid
import pandas as pd
from typing import List
from models.models import Account, Demand, Category, Subcategory, Party, Transaction

class Importer:
    def __init__(self, file, skip_rows=0):
        # self.account = account
        self.file = file
        self.skip_rows = skip_rows
        # self.records = pd.read_csv(file)
        self.records = []
        self.columns = ['Ref', 'Date', 'Amount', 'Source', 'Description']
        self.mastersheet_entries = []

    def get_records_from_files(self):
        # self.records = pd.read_csv(self.file)  
        with open(self.file, newline='') as file:
            rows = csv.reader(file, delimiter=',')
            for i in range(0, self.skip_rows):
                row = next(rows)
                print('skipped', row)
            for row in rows:
                record = self.convert_row_to_mastersheet_entry(row)
                record = [str(uuid.uuid4())] + record
                self.records.append(record)
        

    # def print_records(self):
    #     # self.get_records_from_files()
    #     # for record in self.records:
    #     #     print(record)
    #     print(self.records)
    
    def convert_row_to_mastersheet_entry(self, row):
        return row # to be implemeneted by each importer

    def get_mastersheet_entries(self, date_range=None):
        self.get_records_from_files()
        self.mastersheet_entries = pd.DataFrame(self.records, columns=self.columns)
        return self.mastersheet_entries
        # for record in self.records:
        #     self.mastersheet_entries.append(self.convert_record_to_mastersheet_entry(record))

    # def print_mastersheet_entries(self):
    #     print(self.mastersheet_entries)