from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


def date_to_str(dt: date) -> str:
    return dt.strftime('%d/%m/%Y')


def str_to_date(dt: str) -> date:
    return datetime.strptime(dt, '%d/%m/%Y')


def inform_code(obj: str) -> int:
    code = '0'
    codeok = False
    while not codeok:
        code = input(f'Code {obj} (0 - exit): ').strip()

        if code == '0':
            return 0

        try:
            code = int(code)
            codeok = True
        except:
            print(f'\33[1;31mCode {obj} should be numeric\33[m')

    return code


def inform_name(obj: str) -> str:
    name = ''
    while name == '':
        name = input('Name: ').strip()
        if name == '' or name is None:
            print(f'\33[1;31mName {obj}is empty\33[m')

    return name


def date_valid(data) -> bool:
    try:
        datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False


def valid_year() -> int:
    year = '0'
    yearok = False
    while not yearok:
        year = input('Year (0 - exit): ').strip()

        if year == '0':
            return 0
        try:
            year = int(year)
        except:
            print('\33[1;31mShould be numeric\33[m')
            continue
        if year < 2020:
            print('\33[1;31mYear less than limit\33[m')
        elif year > date.today().year:
            print('\33[1;31mYear bigger than actual year\33[m')
        else:
            yearok = True
    return year


def valid_month_year() -> tuple:
    month = '0'
    monthok = False
    while not monthok:
        month = input('Month (0 - exit): ').strip()

        if month == '0':
            return 0, 0
        try:
            month = int(month)
        except:
            print('\33[1;31mShould be numeric\33[m')
            continue
        if month >= 13:
            print('\33[1;31mInvalid month\33[m')
        else:
            monthok = True

    year = valid_year()

    return month, year


def first_last_day(month: int, year: int) -> tuple:
    # put 0 on left
    if month < 10:
        monthstr = str('0' + str(month))
    else:
        monthstr = str(month)

    dtini: str = str(year) + '-' + monthstr + '-01'
    dtfinal: str = date(year, month, 1)

    # add 1 to month
    dtfinal = dtfinal + relativedelta(months=1)
    # take the last day of the month
    dtfinal = dtfinal - timedelta(days=1)

    return dtini, dtfinal
