import Database
from pandas import DataFrame

conn = Database.conn
cursor = Database.cursor

# The table was created by SQLiteStudio
createTable = 'CREATE TABLE IF NOT EXISTS  '\
              ' CARD ('\
              ' CODECARD INTEGER PRIMARY KEY UNIQUE NOT NULL,'\
              ' NAMECARD VARCHAR (20) NOT NULL'\
              ');'

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

    def findcode(dfcard: DataFrame, codeCard: int) -> str:
        nameCard = ''

        if int(codeCard) in dfcard.Code:
            lst = dfcard.query(f'Code == {codeCard}').values
            nameCard = lst[0][1]
        return nameCard

    def findall(dfcard: DataFrame) -> None:
        print('-' * 40)
        print(dfcard)
        print('-' * 40)

    def upload_dataframe(self) -> DataFrame:
        cursor.execute('''SELECT CODECARD, NAMECARD FROM CARD ORDER BY CODECARD''')

        np_code = []
        np_name = []

        for reg in cursor.fetchall():
            np_code.append(reg[0])
            np_name.append(reg[1])

        data_card: dict = {'Code': np_code, 'Name': np_name}

        df = DataFrame(data_card)
        dfcard = DataFrame(df, columns=['Code', 'Name'])
        return dfcard
