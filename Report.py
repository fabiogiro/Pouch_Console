import Database
from datetime import datetime
from Models.Pouch import Pouch
from Models.Card import Card
from Models.Company import Company
from View import Card, Company
from fpdf import FPDF
from Utils import util


def menu():
    month, year = util.valid_month_year()

    if year == 0:
        return

    regcard: Card = Card.validcard(0)  # SEARCH
    regsynd, regcomp = Company.validcompany(0)

    conn = Database.conn
    cursor = Database.cursor

    filepdf = FPDF('P', 'mm', 'A4')  # Portrait

    dtini, dtfinal = util.first_last_day(month, year)

    data: cursor = Pouch.finddate(dtini, dtfinal, regcard.codeCard, regsynd.codeSynd, regcomp.codeComp)

    if len(data) == 0:
        print("\33[1;31mDon't have register\33[m")
    else:
        filepdf.add_page()
        filepdf.set_font('Arial', '', 10)
        filepdf.cell(190, 4, 'Página ' + str(filepdf.page_no()), 0, 1, 'R')
        filepdf.set_font('Arial', 'B', 16)
        filepdf.cell(190, 4, 'Monthly Report - ' + str(month) + '/' + str(year) +
                     '          ' + datetime.strftime(datetime.today().now(),
                                                      '%m/%d/%Y %H:%M'), 0, 1, 'C')
        filepdf.set_font('Courier', '', 10)
        filepdf.cell(190, 4, ' ', 0, 1, 'R')
        # 60 = weight 20 = height by cell 0 = border 1 = break line L = align
        subtitle = '   Date    Pouch      Card       Syndicate       Company        Quant  Value'
        filepdf.set_font('Courier', '', 10)
        filepdf.cell(190, 4, subtitle, 0, 1, 'L')
        contline = 2
        for reg in data:
            dtarrived = reg[0]
            codepouch = reg[1]
            namecard = reg[2]
            namesynd = reg[3]
            namecomp = reg[4]
            quant = reg[5]
            value = reg[6]

            if contline > 59:
                filepdf.add_page()
                filepdf.set_font('Arial', '', 10)
                filepdf.cell(190, 4, 'Página ' + str(filepdf.page_no()), 0, 1, 'R')
                subtitle = 'Arrived    Pouch      Card       Syndicate       Company        Quant  Value'
                filepdf.set_font('Courier', '', 10)
                filepdf.cell(190, 4, subtitle, 0, 1, 'L')
                contline = 2

            contline += 1

            filepdf.cell(210, 4, f'{dtarrived} {codepouch:<10} {namecard:<10} '
                                 f'{namesynd:<15} {namecomp:<15} {quant:>4} {value:>6.2f}', 0, 1, 'L')
        try:
            filepdf.output(f'ReportMonthly_{year}{month:0>2}.pdf', 'F')   # D - Web   F- Local
            print('Generated Report')
        except Exception:
            print('\33[1;31mThe file pdf is open\33[m')

    return
