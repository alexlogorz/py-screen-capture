from copyreg import constructor
import sqlite3

class DBManager:
    
    def __init__(self, db):
        try:
            self.conn = sqlite3.connect(db, check_same_thread=False)
            self.cursor = self.conn.cursor()
            print('Connected to', db)
            self.constructTable()
        except:
            raise Exception("Error connecting to db")
    
    # insert statement
    def insertTuples(self, tuples):
        try:
            self.cursor.executemany("""
                INSERT INTO Items (Seller, Name, Price, Stamp) VALUES (?, ?, ?, ?);
            """, tuples)
            self.conn.commit()
        except Exception as err:
            print("Error while inserting:", str(err))

    # the constraint will avoid inserting redundant item data for the same seller
    def constructTable(self):
        try:
            self.cursor.execute("""
                CREATE TABLE Items (Seller TEXT, Name TEXT, Price INT, Stamp TEXT, CONSTRAINT items_pkey PRIMARY KEY (Seller, Name, Price));
            """);
            self.conn.commit()
        except Exception as err:
            print("Error while creating table:", str(err))
        
    def closeConn(self):
        self.conn.close()