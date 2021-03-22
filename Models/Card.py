import Database
from pandas import DataFrame

conn = Database.conn
cursor = Database.cursor

# The table was created by SQLiteStudio
createTable = 'CREATE TABLE IF NOT EXISTS CARD ('\
              'ID       INT     PRIMARY KEY AUTOINCREMENT,'\
              'CODECARD INT     UNIQUE NOT NULL,'\
              'NAMECARDameCard STRING (20) NOT NULL'\
              ');'
#CREATE UNIQUE INDEX ICODECARD ON CARD (
#    CODECARD ASC
#);

cursor.execute(createTable)


class Card:
    def __init__(self: object, codeCard: int, nameCard: str):
        self.codeCard = codeCard
        self.nameCard = nameCard

    def codeCard(self: object) -> int:
        return self.codeCard

    def nameCard(self: object) -> str:
        return self.nameCard

    def insertdb(self: object) -> None:
        cursor.execute('''INSERT INTO CARD (CODECARD, NAMECARD) VALUES (?, ?)''',
                       (self.codeCard, self.nameCard))

        conn.commit()

    def updatedb(self: object) -> None:
        cursor.execute('''UPDATE CARD SET NAMECARD = ? WHERE CODECARD = ?''',
                       (self.nameCard, self.codeCard))

        conn.commit()

    def deletedb(self: object) -> None:
        cursor.execute('''DELETE FROM CARD WHERE CODECARD = ?''',
                       str(self.codeCard))

        conn.commit()

    def findcode(codecard: str) -> str:
        sql = f'SELECT NAMECARD FROM CARD WHERE CODECARD = {codecard}'
#        cursor.execute('''SELECT NAMECARD FROM CARD WHERE CODECARD = ?''',
#                       codecard)
        cursor.execute(sql)
        nameCard = ''

        for reg in cursor.fetchall():
            nameCard = reg[0]
        return nameCard

    def findall(self) -> None:
        cursor.execute('''SELECT CODECARD, NAMECARD FROM CARD ORDER BY CODECARD''')

        lstcode = []
        lstname = []

        for reg in cursor.fetchall():
            lstcode.append(reg[0])
            lstname.append(reg[1])

        dct: dict = {'Code': lstcode, 'Name': lstname}

        df = DataFrame(dct)
        frame = DataFrame(df, columns=['Code', 'Name'])
        print('-' * 40)
        print(frame)
        print('-' * 40)
