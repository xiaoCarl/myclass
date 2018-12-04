import sqlite3

connection = sqlite3.connect(":memory:")

with connection:
    connection.execute(
        'CREATE TABLE events(ts, msg, PRIMARY KEY(ts, msg))')

try:
    with connection:
        connection.executemany('INSERT INTO events VALUES (?, ?)', [
            (1, 'foo'),
            (2, 'bar'),
            (3, 'baz'),
        ])
except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
    print('Could not complete operation:', e)
    
# No row was inserted because transaction failed
for row in connection.execute('SELECT * FROM events'):
    print(row)
    
connection.close()
