import Database
from pandas import DataFrame

conn = Database.conn
cursor = Database.cursor
# The table was created by SQLiteStudio
createTable = 'CREATE TABLE IF NOT EXISTS SYNDICATE ('\
              'ID       INT         PRIMARY KEY AUTOINCREMENT,'\
              'CODESYND INT         UNIQUE  NOT NULL,'\
              'NAMESYND STRING (50) NOT NULL'\
              ');'
#CREATE UNIQUE INDEX ICODESYND ON SYNDICATE (
#    CODESYND ASC
#);

cursor.execute(createTable)


class Syndicate:
    def __init__(self: object, codeSynd: int, nameSynd: str):
        self.codeSynd = codeSynd
        self.nameSynd = nameSynd

    def codeSynd(self: object) -> int:
        return self.codeSynd

    def nameSynd(self: object) -> str:
        return self.nameSynd

    def insertdb(self: object) -> None:
        cursor.execute('''INSERT INTO SYNDICATE (CODESYND, NAMESYND) VALUES (?, ?)''',
                       (self.codeSynd, self.nameSynd))

        conn.commit()

    def updatedb(self: object) -> None:
        cursor.execute('''UPDATE SYNDICATE SET NAMESYND = ? WHERE CODESYND = ?''',
                       (self.nameSynd, self.codeSynd))

        conn.commit()

    def deletedb(self: object) -> None:
        cursor.execute('''DELETE FROM SYNDICATE WHERE CODESYND = ?''',
                       str(self.codeSynd))

        conn.commit()

    def findcode(codeSynd: str) -> str:
        sql = f'SELECT NAMESYND FROM SYNDICATE WHERE CODESYND = {codeSynd}'
#        cursor.execute('''SELECT NAMESYND FROM SYNDICATE WHERE CODESYND = ?''',
#                       str(codeSynd))
        cursor.execute(sql)
        nameSynd = ''

        for reg in cursor.fetchall():
            nameSynd = reg[0]
        return nameSynd

    def findall(self: object) -> None:
        cursor.execute('''SELECT CODESYND, NAMESYND FROM SYNDICATE ORDER BY CODESYND''')

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
