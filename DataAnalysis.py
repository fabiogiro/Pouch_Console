import Database
from Models.Card import Card
from Models.Syndicate import Syndicate
from View.Card import validcard
from View.Syndicate import validsyndicate
import matplotlib.pyplot as plt
from Utils import util
import numpy as np
from pandas import DataFrame

conn = Database.conn
cursor = Database.cursor


def getparameters(optiondate: int, option: int):
    resp = 'Y'
    while resp.upper() == 'Y':
        if optiondate == 1:
            month, year = util.valid_month_year()
            if year == '0':
                return

            dtini, dtfinal = util.first_last_day(month, year)

            regcard: Card = validcard(0)
            regsynd: Syndicate = validsyndicate(0)

            lstdate, lstquant, lstvalue = getdata(dtini, dtfinal, regcard.codeCard, regsynd.codeSynd, 1)

            x = lstdate

            if option == 1:
                y = lstquant
                plt.bar(x, y, label='QUANT', color='g')
            elif option == 2:
                y = lstvalue
                plt.bar(x, y, label='VALUE', color='b')

            plt.legend()
            plt.show()

        if optiondate == 2:
            year = util.valid_year()
            if year == 0:
                return
            else:
                processyear(year, option)

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N]? ')


def processyear(year: int, option: int):
    npmonth = np.zeros(12)
    npquant = np.zeros(12)
    npvalue = np.zeros(12)

    dtini = str(year) + '-01-01'
    dtfinal = str(year) + '-12-31'

    regcard: Card = validcard(0)
    regsynd: Syndicate = validsyndicate(0)

    lstdate, lstquant, lstvalue = getdata(dtini, dtfinal, regcard.codeCard, regsynd.codeSynd, 2)

    if len(lstdate) > 0:
        dct = {'month': lstdate, 'quant': lstquant, 'value': lstvalue}

        frame = DataFrame(dct)

        if option == 1:
            frame.groupby(by='month')['quant'].mean()
        else:
            frame.groupby(by='month')['value'].mean()

    #    countmonth = 0
    #    totquant = 0
    #    totvalue = 0
    #    month = 0
    #
    #    for count in range(1, len(lstdate)):
    #        monthactual = lstdate[count]
    #        if month == 0:   # first time
    #            month = monthactual
    #        if month != monthactual:
    #            npmonth[month - 1] = month
    #            npquant[month - 1] = round(totquant / countmonth)
    #            npvalue[month - 1] = round(totvalue / countmonth)
    #
    #            month = monthactual
    #
    #            countmonth = 0
    #            totquant = 0
    #            totvalue = 0
    #
    #        countmonth += 1
    #        totquant += lstquant[count]
    #        totvalue += lstvalue[count]
    #
    #    npmonth[month - 1] = month
    #    npquant[month - 1] = round(totquant / countmonth)
    #    npvalue[month - 1] = round(totvalue / countmonth)
    #
    #    x = npmonth
    #
    #    if option == 1:
    #        y = npquant
    #        plt.bar(x, y, label='QUANT', color='g')
    #    elif option == 2:
    #        y = npvalue
    #        plt.bar(x, y, label='VALUE', color='b')

        x = frame['month']

        if option == 1:
            y = frame['quant']
            plt.bar(x, y, label='QUANT', color='g')
        elif option == 2:
            y = frame['value']
            plt.bar(x, y, label='VALUE', color='b')

        plt.legend()
        plt.show()
    else:
        return "Don´t have register"


def getdata(dtini: str , dtfinal: str, codecard: int, codesynd: int, optiondate: int) -> tuple:
    sql = f'SELECT DISTINCT(DTARRIVED), AVG(QUANT) AS TOTQUANT, AVG(VALUE) AS TOTVALUE' \
          ' FROM POUCH' \
          f' WHERE DTARRIVED BETWEEN "{str(dtini)}" AND "{str(dtfinal)}"'
    if int(codecard) > 0:
        sql = sql + f' AND CODECARD = {codecard}'
    if int(codesynd) > 0:
        sql = sql + f' AND CODESYND = {codesynd}'
    sql = sql + ' GROUP BY DTARRIVED'
    sql = sql + ' ORDER BY DTARRIVED'

    cursor.execute(sql)

    lstdate = []
    lstquant = []
    lstvalue = []
    for reg in cursor.fetchall():
        if optiondate == 1:
            lstdate.append(int(reg[0][-2::]))  # day 2020-01-20  -> 20
        elif optiondate == 2:
            lstdate.append(int(reg[0][5:7]))  # month 2020-01-20  -> 01
        lstquant.append(reg[1])
        lstvalue.append(reg[2])
    return lstdate, lstquant, lstvalue


def menu():
    option = ' '
    while option != '0':
        print('''Select the option
        1 - Quant
        2 - Value
        0 - Exit''')
        option = input('option: ').strip()
        if option == '0':
            continue
        elif option == '1' or option == '2':
            print('''Select the option
            1 - Month/Year
            2 - Year
            0 - Exit''')
            optiondate = input('option: ').strip()
            if optiondate == '0':
                continue
            elif optiondate == '1' or optiondate == '2':
                getparameters(int(optiondate), int(option))
            else:
                print('\33[1;31mInvalid option\33[m')
        else:
            print('\33[1;31mInvalid option\33[m')
    print('-' * 40)
