from Models.Company import Company
from Models.Syndicate import  Syndicate
from Models.Pouch import Pouch
from Utils.util import inform_code, inform_name
from View.Syndicate import validsyndicate

'''
def search_name_comp(option: int) -> object:
    regok = False
    while not regok:
        regsynd: Syndicate = search_name_synd()
        # the code informed is ok
        if int(regsynd.codeSynd) > 0:
            # Checks if the syndicate exist
            regsynd: Syndicate = Syndicate(regsynd.codeSynd, Syndicate.findcode(regsynd.codeSynd))

            if regsynd.nameSynd != '':
                regcompok = False
                while not regcompok:
                    codeComp: int = inform_code('Company')

                    if codeComp == 0:
                        return (Syndicate(0, ''), Company(0, 0, ''))
                    # Checks if the company exist
                    regcomp: Company = Company(regsynd.codeSynd, codeComp,
                                               Company.findcode(regsynd.codeSynd, codeComp).strip())
                    if option == 1:   # INSERT
                        if regcomp.nameComp == '':
                            regcompok = True
                            regok = True
                        else:
                            print(f'\33[1;31mCompany Code exist\33[m')
                    else:   # UPDATE / DELETE
                        if regcomp.nameComp != '':
                            regcompok = True
                            regok = True
                        else:
                            print(f'\33[1;31mCompany Code not exist\33[m')
            else:
                print(f'\33[1;31mSyndicate Code not exist\33[m')
#                return (Syndicate(0, ''), Company(0, 0, ''))
        else:
            regsynd: Syndicate = Syndicate(0, '')
            regcomp: Company = Company(0, 0, '')
            break

    return (regsynd, regcomp)
'''


def search_name_comp(codesynd: int) -> object:
    codeComp: int = inform_code('Company')

    if codeComp == 0:
        return Company(0, 0, '')
    # Checks if have the card is registered
    regcomp: Company = Company(codesynd, codeComp,
                               Company.findcode(codesynd, codeComp).strip())
    return regcomp


def validcompany(option: int) -> object:
    regsyndok = False
    while not regsyndok:
        regsynd: Syndicate = validsyndicate(0)   # search
        if int(regsynd.codeSynd) > 0:
            regsyndok = True
            regcompok = False
            while not regcompok:
                regcomp: Company = search_name_comp(regsynd.codeSynd)
                # the code informed is ok
                if int(regcomp.codeComp) == 0:
                    regcomp: Company = Company(0, 0, '')
                    return (regsynd, regcomp)
                if option == 1:   # INSERT
                    if regcomp.nameComp == '':
                        # the company not exist
                        regcompok = True
                    else:
                        print(f'\33[1;31mCompany Code exist\33[m')
                else:   # UPDATE / DELETE
                    if regcomp.nameComp != '':
                        # the company exist
                        regcompok = True
                    else:
                        print(f'\33[1;31mCompany Code not exist\33[m')
        else:
            regcomp: Company = Company(0, 0, '')
            break

    return (regsynd, regcomp)


def insert(option: int) -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        regsynd, regcomp = validcompany(option)
        if int(regcomp.codeComp) > 0:
            regcomp.nameComp = inform_name('Company')
            Company.insertdb(regcomp)

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N]? ')


def update(option: int) -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        regsynd, regcomp = validcompany(option)
        if int(regcomp.codeComp) > 0:
            regcomp.nameComp = inform_name('Company')
            Company.updatedb(regcomp)

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N}? ')


def delete(option: int) -> None:
    resp = 'Y'
    while resp.upper() == 'Y':
        regsynd, regcomp = validcompany(3)
        if int(regcomp.codeComp) > 0:
            countcodepouch = Pouch.countcodepouchcomp(regcomp.codeComp)

            if countcodepouch == 0:
                resp = ' '
                while resp.upper() not in 'YN':
                    resp = input(f'Confirm the delete the {regsynd.codeSynd} - '
                                 f'{regsynd.nameSynd} - {regcomp.codeComp} - '
                                 f'{regcomp.nameComp} [Y/N]? ')
                if resp.upper() == 'Y':
                   Company.deletedb(regcomp)
            else:
                print(f'\33[1;31mHave Pouch registered\33[m')

        resp = ' '
        while resp.upper() not in 'YN':
            resp = input('Do you want continue [Y/N}? ')


def list():
    # list the all syndicate/company
    Company.findall(self=object)


def menu():
    option = ' '
    while option != '0':
        print('''Select the option Company
        1 - Insert
        2 - Update
        3 - Delete
        4 - List
        0 - Exit''')
        option = input('option: ').strip()
        if option == '0':
            continue
        elif option == '1':
            insert(int(option))
        elif option == '2':
            update(int(option))
        elif option == '3':
            delete(int(option))
        elif option == '4':
            list()
        else:
            print('-' * 40)
            print('\33[1;31mInvalid option\33[m')
            print('-' * 40)
    print('-' * 40)
