import sqlite3

class DatabaseHandler:
    def __init__(self, databaseName):
        self.databaseName = databaseName
        self.conn = sqlite3.connect('{}.db'.format(databaseName))
        self.cursor = self.conn.cursor()
        self.createTable()

    def createTable(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS {} (platform TEXT, isim TEXT, adet REAL, değer REAL, toplam REAL)'.format(self.databaseName))
        self.conn.commit()

    def deleteData(self):
        self.cursor.execute('DELETE FROM {}'.format(self.databaseName))

    def commit(self):
        self.conn.commit()

    def fetchAllItems(self):
        self.cursor.execute('SELECT * FROM {}'.format(self.databaseName))
        return self.cursor.fetchall()

    def insertItem(self, platform, isim, adet, değer, toplam):
        self.cursor.execute('INSERT INTO {} (platform, isim, adet, değer, toplam) VALUES (?, ?, ?, ?, ?)'.format(self.databaseName),
                            (platform, isim, adet, değer, toplam))
        self.conn.commit()

    def deleteItem(self, platform, isim, adet, değer, toplam):
        self.cursor.execute('DELETE FROM {} WHERE platform=? AND isim=? AND adet=? AND değer=? AND toplam=?'.format(self.databaseName),
                            (platform, isim, adet, değer, toplam))
        self.conn.commit()

    def closeConnection(self):
        self.conn.close()