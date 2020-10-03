from connectors import capital_one

from connectors import mastersheet


if __name__ == '__main__':
    importers = capital_one.importers

    for importer in importers:
        entries = importer.get_mastersheet_entries()
        mastersheet.insert(entries)
    
    


