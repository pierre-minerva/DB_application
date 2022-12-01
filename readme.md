### Commands:

```
python -m venv .venv
source .venv/bin/activate

pip pinstall -r requirements.txt

python create_and_insert.py
python query.py
python test.py

```
### Indexing:
Columns chosen for indexing based on the queries. Indexing was set by including index=True in the create_and_insert.py table classes. Because primary keys are automatically indexed, we left the index=True statement out. 

### Normalization:
We achieved 1NF normalization because each column only has one value per entry, all rows in a column have the same type, and all columns are unique. We do not achieve complete 2NF because we have a partial dependency in the commission column which is based on the sales price column. This however, was a requirement according to the instructions. If we do not achieve 2NF then we cannot achieve 3NF because all properties of 2NF are also included in 3NF.

### Transactions
Transactions in SQLalchemy are handled by the session.add() method followed by the session.commit() method. If there is an error when running these methods, the database rolls back to the state before they were ran. Using the get_or_create() function to individually create transactions for each row entry, we won't lose all our progress if an error occurs in a later data entry as opposed to just putting the commit() method at the end. 