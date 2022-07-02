import sqlite3

class DBManager:
    
    def __init__(self, db):
        try:
            self.conn = sqlite3.connect(db, check_same_thread=False)
            self.cursor = self.conn.cursor()
            print('Connected!')
        except:
            raise Exception("Error connecting to db")
    
        
    def insertTuples(self, tuples):
        self.cursor.executemany("""
            INSERT INTO Items (name, price, seller, stamp) VALUES (?, ?, ?, ?) 
        """, tuples)
        self.conn.commit()
