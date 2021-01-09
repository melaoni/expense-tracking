import click
import datetime
from connectors import capital_one
from connectors import mastersheet

this_month = datetime.datetime.now().strftime('%Y-%m')

@click.command()
@click.option('-m', '--month', default=this_month, help='Month of transactions to import, e.g. 2020-11')
def import_transactions(month):
    importers = capital_one.importers

    for importer in importers:
        entries = importer.get_mastersheet_entries(month=month)
        mastersheet.insert(entries)

if __name__ == '__main__':
    import_transactions()
    
    


