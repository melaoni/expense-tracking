# Env setup
* Install conda: https://docs.conda.io/en/latest/miniconda.html
* Follow instructions to install dependencies in a conda environment
https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file

# How to import master sheet data
* Run import_transactions with YYYY-MM to insert records into google mastersheet
* Update categorization and refunds in google mastersheet
* Run init_db.py
Delete database/sqlite.db first if already exist
* Run parse_and_store_records.py to load data from mastersheet
Make sure the updated version of Expense tracking file is under the parser directory
* Run monthly_report.py for the per month cost split between Melanie and Sadruddin