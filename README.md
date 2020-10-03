# Env setup
* Install conda: https://docs.conda.io/en/latest/miniconda.html
* Follow instructions to install dependencies in a conda environment
https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file

# How to import master sheet data
* Run init_db.py first
Delete database/sqlite.db first if already exist
* Run parse_and_store_records.py
Make sure the updated version of Expense tracking file is under the parser directory
* Run monthly_report.py for the per month cost split between Melanie and Sadruddin