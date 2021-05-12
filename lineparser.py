import sqlite3
from csv import reader

conn = sqlite3.connect('zipdb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS ZIPS')

cur.executescript('''
CREATE TABLE ZIPS (
    location TEXT,
    ZIP TEXT,
    num INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE);
    ''')

with open('ZIPS.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        location = row[2]
        ZIP = row[4]
        cur.execute('SELECT num FROM ZIPS WHERE location = ? ', (location,))
        row = cur.fetchone()
        if row is None:
            cur.execute('''INSERT INTO ZIPS (location, ZIP)
                    VALUES (?,?)''', (location,ZIP))
        else:
            continue
conn.commit()
