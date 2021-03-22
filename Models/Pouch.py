import Database
from pandas import DataFrame

conn = Database.conn
cursor = Database.cursor

# The table was created by SQLiteStudio
createTable = 'CREATE TABLE IF NOT EXISTS POUCH ('\
               'ID        INTEGER        PRIMARY KEY AUTOINCREMENT,'\
               'CODEPOUCH STRING (10)    UNIQUE NOT NULL,'\
               'CODECARD  INT            REFERENCES CARD (CODECARD) ON DELETE CASCADE NOT NULL,'\
               'CODESYND  INT            REFERENCES SYNDICATE (CODESYND) ON DELETE CASCADE NOT NULL,'\
               'CODECOMP  INT            NOT NULL,'\
               'DTARRIVED DATE           NOT NULL,'\
               'QUANT     INTEGER        NOT NULL,'\
               'VALUE     DOUBLE (10, 2) NOT NULL'\
               ');'
#CREATE UNIQUE INDEX Index_CODEPOUCH ON POUCH (
#    CODEPOUCH ASC
#);
#CREATE INDEX Index_DTARRIVED ON POUCH (
#    DTARRIVED ASC
#);

cursor.execute(createTable)


class Pouch:
    def __init__(self: object, codePouch: str, codeCard: int, codeSynd: int,
                 codeComp: int, dtArrived: str, quant: int, value: float):
        self.codePouch = codePouch
        self.codeCard = codeCard
        self.codeSynd = codeSynd
        self.codeComp = codeComp
        self.dtArrived = dtArrived
        self.quant = quant
        self.value = value

    def codePouch(self: object) -> str:
        return self.codePouch

    def codeCard(self: object) -> int:
        return self.codeCard

    def codeSynd(self: object) -> int:
        return self.codeSynd

    def codeComp(self: object) -> int:
        return self.codeComp

    def dtArrive(self: object) -> str:
        return self.dtArrived

    def quant(self: object) -> int:
        return self.quant

    def value(self: object) -> float:
        return self.value

    def insertdb(self: object) -> None:
        cursor.execute('''INSERT INTO POUCH (CODEPOUCH, CODECARD, CODESYND, CODECOMP, 
                        DTARRIVED, QUANT, VALUE) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (self.codePouch, self.codeCard, self.codeSynd, self.codeComp,
                        self.dtArrived, self.quant, self.value))

        conn.commit()

    def updatedb(self: object) -> None:
        cursor.execute('''UPDATE POUCH 
                          SET CODECARD = ? 
                          , CODESYND = ?
                          , CODECOMP = ? 
                          , DTARRIVED = ? 
                          , QUANT = ?
                          , VALUE = ?
                          WHERE CODEPOUCH = ?''',
                       (self.codeCard,
                        self.codeSynd,
                        self.codeComp,
                        self.dtArrived,
                        self.quant,
                        self.value,
                        self.codePouch))

        conn.commit()

    def deletedb(codePouchIN: str) -> None:
        cursor.execute('''DELETE FROM POUCH WHERE CODEPOUCH = ?''',
                       codePouchIN)

        conn.commit()

    def countcodepouch(sql: str) -> int:
        cursor.execute(sql)
        reg: cursor = cursor.fetchall()
        return reg[0]

    def findcodepouch(codePouchIN: str) -> str:
        sql = f'SELECT CODEPOUCH FROM POUCH WHERE CODEPOUCH = {codePouchIN}'

        codePouchOUT = ''

        for reg in cursor.fetchall():
            codePouchOUT = reg[0]
        return codePouchOUT

    def countcodepouchcard(codecard: str) -> int:
        sql = f'SELECT COUNT(CODEPOUCH) FROM POUCH WHERE CODECARD = {codecard}'
        cursor.execute(sql)
        reg: cursor = cursor.fetchall()
        return reg[0]

    def countcodepouchsynd(codesynd: str) -> int:
        sql = f'SELECT COUNT(CODEPOUCH) FROM POUCH WHERE CODESYND = {codesynd}'
        cursor.execute(sql)
        reg: cursor = cursor.fetchall()
        return reg[0]

    def countcodepouchcomp(codecomp: str) -> int:
        sql = f'SELECT COUNT(CODEPOUCH) FROM POUCH WHERE CODECOMP = {codecomp}'
        cursor.execute(sql)
        reg: cursor = cursor.fetchall()
        return reg[0]

    def findall(self: object) -> None:
#        cursor.execute('''SELECT POUCH.CODEPOUCH, CARD.CODECARD, CARD.NAMECARD,
#                          SYND.CODESYND, SYND.NAMESYND, COMP.CODECOMP, COMP.NAMECOMP,
#                          DTARRIVED, QUANT, VALUE
#                          FROM POUCH POUCH
#                          INNER JOIN CARD CARD ON POUCH.CODECARD = CARD.CODECARD
#                          INNER JOIN SYNDICATE SYND ON POUCH.CODESYND = SYND.CODESYND
#                          INNER JOIN COMPANY COMP ON POUCH.CODESYND = COMP.CODESYND
#                                                 AND POUCH.CODECOMP = COMP.CODECOMP
#                          ORDER BY POUCH.CODEPOUCH''')
        cursor.execute('''SELECT CODEPOUCH, CODECARD, CODESYND, CODECOMP, 
                          DTARRIVED, QUANT, VALUE 
                          FROM POUCH POUCH 
                          ORDER BY POUCH.CODEPOUCH''')

        lstcodepouch = []
        lstcodecard = []
        lstcodesynd = []
        lstcodecomp = []
        lstdtarrived = []
        lstquant = []
        lstvalue = []

        for reg in cursor.fetchall():
            lstcodepouch.append(reg[0])
            lstcodecard.append(reg[1])
            lstcodesynd.append(reg[2])
            lstcodecomp.append(reg[3])
            lstdtarrived.append(reg[4])
            lstquant.append(reg[5])
            lstvalue.append(reg[6])

        dct: dict = {'CodePouch': lstcodepouch, 'CodeCard': lstcodecard,
                     'CodeSynd': lstcodesynd, 'CodeComp': lstcodecomp,
                     'DtArriveD': lstdtarrived, 'Quant': lstquant, 'Value': lstvalue}

        df = DataFrame(dct)
        frame = DataFrame(df, columns=['CodePouch', 'CodeCard', 'CodeSynd',
                                       'CodeComp', 'DtArriveD', 'Quant', 'Value'])
        print('-' * 40)
        print(frame)
        print('-' * 40)

    def finddate(dtini: str , dtfinal: str, codecard: int, codesynd: int, codecomp: int) -> list:
        sql = f'SELECT DISTINCT(POUCH.DTARRIVED), POUCH.CODEPOUCH, CARD.NAMECARD,' \
              ' SYND.NAMESYND, COMP.NAMECOMP, POUCH.QUANT, POUCH.VALUE' \
              ' FROM POUCH AS POUCH' \
              ' INNER JOIN CARD CARD ON POUCH.CODECARD = CARD.CODECARD' \
              ' INNER JOIN SYNDICATE SYND ON POUCH.CODESYND = SYND.CODESYND' \
              ' INNER JOIN COMPANY COMP ON POUCH.CODESYND = COMP.CODESYND ' \
              ' AND POUCH.CODECOMP = COMP.CODECOMP' \
              f' WHERE POUCH.DTARRIVED BETWEEN "{str(dtini)}" AND "{str(dtfinal)}"'
        if int(codecard) > 0:
            sql = sql + f' AND POUCH.CODECARD = {codecard}'
        if int(codesynd) > 0:
            sql = sql + f' AND POUCH.CODESYND = {codesynd}'
        if int(codecomp) > 0:
            sql = sql + f' AND POUCH.CODECOMP = {codecomp}'
        sql = sql + ' ORDER BY POUCH.DTARRIVED, POUCH.CODECARD, POUCH.CODESYND'

        cursor.execute(sql)
        return cursor.fetchall()
