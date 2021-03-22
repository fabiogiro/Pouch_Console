import sqlite3
from Models.Pouch import Pouch
from Models.Card import Card
from Models.Company import Company
from Utils.util import  date_valid
from View import Card, Company
from datetime import datetime
from pandas import DataFrame


def inform_date(search: bool) -> str:
    dateok: bool = False
    while not dateok:
        if search:
            dtarrived = input('Data Arrived (format(dd/mm/yyyy) (0 for Exit): ').strip()
            if dtarrived == '0':
                dateok = True
                continue
        else:
            dtarrived = input('Data Arrived (format(dd/mm/yyyy): ').strip()
        if date_valid(dtarrived):
            if datetime.strptime(dtarrived, '%d/%m/%Y').date() > datetime.now().date():
                print('\33[1;31mDate arrived is bigger than actual date\33[m')
            else:
                dateok = True
        else:
            print('\33[1;31mDate invalid\33[m')
    return dtarrived


def inform_quant() -> int:
    quantok: bool = False
    while not quantok:
        quant = input('Quant: ').strip()
        try:
            quant = int(quant)
        except:
            print('\33[1;31mQuant should be numeric\33[m')
            continue
        if quant > 0:
            quantok = True
        else:
            print('\33[1;31mQuant is zero\33[m')
    return quant


def inform_value() -> float:
    valueok: bool = False
    while not valueok:
        value = input('Value: ').strip()
        try:
            value = float(value)
        except:
            print('\33[1;31mValue should be numeric\33[m')
        if value > 0:
            valueok = True
        else:
            print('\33[1;31mValue is zero\33[m')
    return value


def insert() -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        code = input('Pouch Code (0 - exit): ').strip()

        if code == '0':
            return

        if code == '' or code is None:
            print('\33[1;31mPouch is empty\33[m')
            continue
        # verify if code pouch have only zeros
        if len(code) == code.count('0'):
            print('\33[1;31mPouch have only zeros\33[m')
            continue

        codePouchIN: str = code
        # check if codePouch exist
        codePouchOUT = Pouch.findcodepouch(codePouchIN)

        if codePouchOUT == '' or codePouchOUT == None:
            # the codePouch isn't exist
            regcard: Card = Card.validcard(0)   # SEARCH
            if int(regcard.codeCard) > 0:
                regsynd, regcomp = Company.validcompany(0)
                if int(regcomp.codeComp) > 0:
                    dtarrived = inform_date(False)
                    quant = inform_quant()
                    value = inform_value()
                    regpouch: Pouch = Pouch(codePouchIN, regcard.codeCard,
                                            regsynd.codeSynd, regcomp.codeComp,
                                            dtarrived, quant, value)
                    Pouch.insertdb(regpouch)
        else:
            print(f'\33[1;31mCode already exist\33[m')
            continue

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N]? ')


def update() -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        code = input('Pouch Code (0 - exit): ').strip()

        if code == '0':
            return

        if code == '' or code is None:
            print('\33[1;31mPouch is empty\33[m')
            continue
        # verify if code pouch have only zeros
        if len(code) == code.count('0'):
            print('\33[1;31mPouch have only zeros\33[m')
            continue

        codePouchIN: str = code
        # check if codePouch exist
        codePouchOUT = Pouch.findcode(codePouchIN)

        if codePouchOUT != '':
            # the codePouch exist
            regcard: Card = Card.validcard(0)  # SEARCH
            if int(regcard.codeCard) > 0:
                regsynd, regcomp = Company.validcompany(0)
                if int(regcomp.codeComp) > 0:
                    dtarrived = inform_date(False)
                    quant = inform_quant()
                    value = inform_value()
                    regpouch: Pouch = Pouch(codePouchIN, regcard.codeCard,
                                            regsynd.codeSynd, regcomp.codeComp,
                                            dtarrived, quant, value)
                    Pouch.updatedb(regpouch)
        else:
            print(f'\33[1;31mCode not exist\33[m')
            continue

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N]? ')


def delete() -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        code = input('Pouch Code (0 - exit): ').strip()

        if code == '0':
            return

        if code == '' or code is None:
            print('\33[1;31mPouch is empty\33[m')
            continue
        # verify if code pouch have only zeros
        if len(code) == code.count('0'):
            print('\33[1;31mPouch have only zeros\33[m')
            continue

        codePouchIN: str = code
        # check if codePouch exist
        codePouchOUT = Pouch.findcode(codePouchIN)

        if codePouchOUT != '':
            resp = ' '
            while resp.upper() not in 'YN':
                resp = input(f'Confirm the delete the {codePouchIN} [Y/N]? ')
            if resp.upper() == 'Y':
               Pouch.deletedb(codePouchIN)
        else:
            print(f'\33[1;31mPouch Code not exist {codePouchOUT}\33[m')
            continue

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N}? ')


def listall():
# list all pouchs
    Pouch.findall(0)


def searchdtarrived():
# list specific date
    resp = 'Y'
    while resp.upper() == 'Y':
        dtarrived = inform_date(True)
        if dtarrived == '0':
            return

        conn = sqlite3.connect('POUCH.db')
        cursor = conn.cursor()

        dtarrivedinv =dtarrived[6:] + '-' + dtarrived[3:5] + '-' + dtarrived[:2]

        data: cursor = Pouch.finddate(dtarrivedinv, dtarrivedinv, 0, 0, 0)

        if len(data) > 0:
            lstcodepouch = []
            lstcodecard = []
            lstcodesynd = []
            lstcodecomp = []
            lstdtarrived = []
            lstquant = []
            lstvalue = []

            for reg in data:
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
        else:
            print("\33[1;31mDon't have register\33[m")

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N]? ')


def list():
    option = ' '
    while option != '0':
        print('''Select the option search
        1 - All
        2 - Date Arrived
        0 - Exit''')
        option = input('option: ').strip()
        if option == '0':
            continue
        elif option == '1':
            listall()
        elif option == '2':
            searchdtarrived()
        else:
            print('-' * 40)
            print('\33[1;31mInvalid option\33[m')
            print('-' * 40)
    print('-' * 40)


def menu():
    option = ' '
    while option != '0':
        print('''Select the option Pouch
        1 - Insert
        2 - Update
        3 - Delete
        4 - List
        0 - Exit''')
        option = input('option: ').strip()
        if option == '0':
            continue
        elif option == '1':
            insert()
        elif option == '2':
            update()
        elif option == '3':
            delete()
        elif option == '4':
            list()
        else:
            print('-' * 40)
            print('\33[1;31mInvalid option\33[m')
            print('-' * 40)
    print('-' * 40)
