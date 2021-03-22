import Database
from Models.Syndicate import Syndicate
from pandas import DataFrame

conn = Database.conn
cursor = Database.cursor
# The table was created by SQLiteStudio
createTable = 'CREATE TABLE IF NOT EXISTS COMPANY ('\
               'ID       INT         PRIMARY KEY AUTOINCREMENT,'\
               'CODESYND INT         REFERENCES SYNDICATE (CODESYND) ON DELETE CASCADE NOT NULL,'\
               'CODECOMP INT         NOT NULL,'\
               'NAMECOMP STRING (50) NOT NULL'\
               ');'

cursor.execute(createTable)


class Company(Syndicate):
    def __init__(self: object, codeSynd: int, codeComp: int, nameComp: str):
        self.codeSynd = codeSynd
        self.codeComp = codeComp
        self.nameComp = nameComp

    def codSynd(self: object) -> int:
        return self.codSynd

    def codeComp(self: object) -> int:
        return self.codeComp

    def nameComp(self: object) -> str:
        return self.nameComp

    def insertdb(self: object) -> None:
        cursor.execute('''INSERT INTO COMPANY (CODESYND, CODECOMP, NAMECOMP) VALUES (?, ?, ?)''',
                       (self.codeSynd, self.codeComp, self.nameComp))

        conn.commit()

    def updatedb(self: object) -> None:
        cursor.execute('''UPDATE COMPANY SET NAMECOMP = ? WHERE CODESYND = ? AND CODECOMP = ?''',
                       (self.nameComp, self.codeSynd, self.codeComp))

        conn.commit()

    def deletedb(self: object) -> None:
        cursor.execute('''DELETE FROM COMPANY WHERE CODESYND = ? AND CODECOMP = ?''',
                       (self.codeSynd, self.codeComp))

        conn.commit()

    def findcode(codeSynd: str, codeComp: str) -> str:
        sql = f'SELECT NAMECOMP FROM COMPANY WHERE CODESYND = {codeSynd} AND CODECOMP = {codeComp}'
#        cursor.execute('''SELECT NAMECOMP FROM COMPANY WHERE CODESYND = ? AND CODECOMP = ?''',
#                       (str(codeSynd), str(codeComp)))
        cursor.execute(sql)

        nameComp = ''

        for reg in cursor.fetchall():
            nameComp = reg[0]
        return nameComp

    def findcodesynd(codesynd: str) -> str:
        sql = f'SELECT COUNT(CODECOMP) FROM COMPANY WHERE CODESYND = {codesynd}'
        #        cursor.execute('''SELECT CODEPOUCH FROM POUCH WHERE CODESYND = ?''',
        #                       (codesynd))
        cursor.execute(sql)
        reg: cursor = cursor.fetchall()
        return reg[0]

    def findall(self: object) -> None:
        cursor.execute('''SELECT SYND.CODESYND, SYND.NAMESynd, COMP.CODECOMP, COMP.NAMECOMP 
                          FROM COMPANY COMP 
                          INNER JOIN SYNDICATE SYND ON SYND.CODESYND = COMP.CODESYND 
                          ORDER BY COMP.CODESYND, COMP.CODECOMP''')

        lstcodesynd = []
        lstnamesynd = []
        lstcodecomp = []
        lstnamecomp = []

        for reg in cursor.fetchall():
            lstcodesynd.append(reg[0])
            lstnamesynd.append(reg[1])
            lstcodecomp.append(reg[2])
            lstnamecomp.append(reg[3])

        dct: dict = {'CodeSynd': lstcodesynd, 'NameSynd': lstnamesynd,
                     'CodeComp': lstcodecomp, 'NameComp': lstnamecomp}

        df = DataFrame(dct)
        frame = DataFrame(df, columns=['CodeSynd', 'NameSynd', 'CodeComp', 'NameComp'])
        print('-' * 40)
        print(frame)
        print('-' * 40)
